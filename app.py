"""Flask web application for EDM Track Recognition"""

import os
import time
import tempfile
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import traceback
import urllib.parse

# Import with error handling
try:
    from src.utils.track_utils import merge_results, deduplicate_tracks
except ImportError as e:
    print(f"ERROR: Failed to import track_utils: {e}")
    raise

try:
    from src.recognizers.acrcloud import ACRCloudRecognizer
    from src.recognizers.audd import AuddRecognizer
    from src.recognizers.shazam import ShazamRecognizer
    from src.recognizers.songfinder import SongFinderRecognizer
except ImportError as e:
    print(f"ERROR: Failed to import recognizers: {e}")
    raise

try:
    from src.utils.config import Config
    from src.audio_processor import AudioProcessor
    from src.output.formatters import format_output
except ImportError as e:
    print(f"ERROR: Failed to import core modules: {e}")
    raise

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size (free tier limit)
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

# Allowed audio extensions
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'flac', 'm4a', 'ogg', 'aac'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page"""
    # Check API availability
    acrcloud = ACRCloudRecognizer()
    audd = AuddRecognizer()
    
    return render_template('index.html', 
                         acrcloud_available=acrcloud.is_available(),
                         audd_available=audd.is_available())

@app.route('/api/status')
def status():
    """API status endpoint"""
    try:
        acrcloud = ACRCloudRecognizer()
        audd = AuddRecognizer()
        shazam = ShazamRecognizer()
        songfinder = SongFinderRecognizer()
        
        return jsonify({
            'acrcloud_available': acrcloud.is_available(),
            'audd_available': audd.is_available(),
            'shazam_available': shazam.is_available(),
            'songfinder_available': songfinder.is_available(),
            'status': 'ready' if any([acrcloud.is_available(), audd.is_available(), shazam.is_available(), songfinder.is_available()]) else 'no_apis'
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'error_type': type(e).__name__,
            'status': 'error'
        }), 500

@app.route('/api/health')
def health():
    """Simple health check - no dependencies"""
    try:
        import subprocess
        # Check if FFmpeg is available
        ffmpeg_available = False
        try:
            result = subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
            ffmpeg_available = result.returncode == 0
        except:
            pass
        
        return jsonify({
            'status': 'ok',
            'ffmpeg_available': ffmpeg_available,
            'timestamp': time.time()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/recognize', methods=['POST'])
def recognize():
    """Process uploaded audio file"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Decode URL-encoded filename first
    original_filename = file.filename
    if '%' in original_filename:
        try:
            original_filename = urllib.parse.unquote(original_filename)
        except Exception as e:
            app.logger.warning(f"Failed to decode filename: {e}")
    
    # Check file extension after decoding
    if not allowed_file(original_filename):
        return jsonify({'error': f'Invalid file type. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
    
    # Get parameters
    format_type = request.form.get('format', 'json').lower()
    try:
        confidence_threshold = float(request.form.get('confidence_threshold', 0.5))
        segment_length = int(request.form.get('segment_length', 60))
        segment_overlap = int(request.form.get('segment_overlap', 20))
    except (ValueError, TypeError) as e:
        return jsonify({'error': f'Invalid parameter: {str(e)}'}), 400
    
    # Save uploaded file
    # Use secure_filename to sanitize, but handle edge cases
    try:
        filename = secure_filename(original_filename)
        if not filename or filename.strip() == '':
            # Fallback if secure_filename returns empty or invalid
            ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'mp3'
            filename = f"upload_{int(time.time())}.{ext}"
    except Exception as e:
        app.logger.warning(f"secure_filename failed: {e}, using fallback")
        ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'mp3'
        filename = f"upload_{int(time.time())}.{ext}"
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        file.save(filepath)
        
        # Check file size - limit to 50MB for free tier
        file_size = os.path.getsize(filepath)
        max_size = 50 * 1024 * 1024  # 50MB
        if file_size > max_size:
            os.unlink(filepath)
            return jsonify({
                'error': f'File too large ({file_size / 1024 / 1024:.1f}MB). Maximum size: 50MB for free tier.',
                'file_size_mb': round(file_size / 1024 / 1024, 1),
                'max_size_mb': 50,
                'hint': 'Try a smaller file or split your mix into smaller parts'
            }), 400
    except Exception as e:
        return jsonify({'error': f'Failed to save file: {str(e)}'}), 500
    
    try:
        # Check API availability first
        try:
            acrcloud = ACRCloudRecognizer()
            audd = AuddRecognizer()
            shazam = ShazamRecognizer()
            songfinder = SongFinderRecognizer()
        except Exception as e:
            return jsonify({
                'error': f'Failed to initialize API recognizers: {str(e)}',
                'error_type': type(e).__name__
            }), 500
        
        available_apis = [acrcloud, audd, shazam, songfinder]
        if not any(api.is_available() for api in available_apis):
            return jsonify({
                'error': 'No recognition APIs available. Please configure API keys in environment variables.',
                'acrcloud_configured': acrcloud.is_available(),
                'audd_configured': audd.is_available(),
                'shazam_configured': shazam.is_available(),
                'songfinder_configured': songfinder.is_available(),
                'hint': 'At least ACRCLOUD_ACCESS_KEY and ACRCLOUD_SECRET_KEY must be set'
            }), 500
        
        # Process the file
        try:
            processor = AudioProcessor(
                segment_length=segment_length,
                segment_overlap=segment_overlap
            )
        except Exception as e:
            return jsonify({
                'error': f'Failed to initialize audio processor: {str(e)}',
                'error_type': type(e).__name__,
                'hint': 'Check if librosa and soundfile are installed'
            }), 500
        
        # Get segments
        try:
            segments = processor.segment_audio(filepath)
        except Exception as e:
            return jsonify({
                'error': f'Failed to process audio file: {str(e)}',
                'error_type': type(e).__name__,
                'hint': 'File may be corrupted or unsupported format'
            }), 500
        all_tracks = []
        
        print(f"[MAIN] Processing {len(segments)} segments...")
        print(f"[MAIN] API Status - ACRCloud: {acrcloud.is_available()}, Shazam: {shazam.is_available()}, SongFinder: {songfinder.is_available()}, Audd: {audd.is_available()}")
        
        # Limit segments for very large files to prevent memory issues
        # Free tier has ~512MB RAM, so be conservative
        max_segments = 50  # Process max 50 segments (~37 minutes at 45s segments)
        if len(segments) > max_segments:
            segments = segments[:max_segments]
            print(f"[MAIN] Large file detected ({len(segments)} total segments). Processing first {max_segments} segments to prevent memory issues.")
            api_errors.append(f"File too long - processing first {max_segments} of {len(segments)} segments")
        
        # Process each segment
        segments_processed = 0
        segments_with_results = 0
        api_errors = []
        import gc  # Garbage collection
        
        for start_time, end_time in segments:
            segment_path = None
            try:
                # Extract segment
                segment_path = processor.extract_segment(
                    filepath, start_time, end_time - start_time
                )
                
                # Try recognition with multiple APIs (try all available)
                results = []
                
                # Try ACRCloud first (best for underground)
                if acrcloud.is_available():
                    try:
                        print(f"[API] Calling ACRCloud for segment {start_time}-{end_time}...")
                        result = acrcloud.recognize(segment_path, start_time, end_time - start_time)
                        if result:
                            results.append(result)
                            print(f"[API] ✓ Segment {start_time}-{end_time}: ACRCloud found {result.artist} - {result.title} (conf: {result.confidence})")
                        else:
                            print(f"[API] ✗ Segment {start_time}-{end_time}: ACRCloud found nothing")
                    except Exception as e:
                        error_msg = str(e)
                        print(f"[API] ✗ ACRCloud error for segment {start_time}-{end_time}: {error_msg}")
                        api_errors.append(f"ACRCloud error: {error_msg}")
                
                # Try Shazam (good coverage)
                if (not results or (results and results[0].confidence < confidence_threshold)) and shazam.is_available():
                    try:
                        result = shazam.recognize(segment_path, start_time, end_time - start_time)
                        if result:
                            results.append(result)
                            print(f"Segment {start_time}-{end_time}: Shazam found {result.artist} - {result.title}")
                    except Exception as e:
                        api_errors.append(f"Shazam error: {str(e)}")
                
                # Try SongFinder (underground focus)
                if (not results or (results and results[0].confidence < confidence_threshold)) and songfinder.is_available():
                    try:
                        result = songfinder.recognize(segment_path, start_time, end_time - start_time)
                        if result:
                            results.append(result)
                            print(f"Segment {start_time}-{end_time}: SongFinder found {result.artist} - {result.title}")
                    except Exception as e:
                        api_errors.append(f"SongFinder error: {str(e)}")
                
                # Try Audd.io as last fallback
                if (not results or (results and results[0].confidence < confidence_threshold)) and audd.is_available():
                    try:
                        result = audd.recognize(segment_path, start_time, end_time - start_time)
                        if result:
                            results.append(result)
                    except Exception as e:
                        api_errors.append(f"Audd error: {str(e)}")
                
                # Merge results
                track = merge_results(results, start_time, end_time, confidence_threshold)
                if track:
                    all_tracks.append(track)
                    segments_with_results += 1
                
                segments_processed += 1
                    
            except Exception as e:
                error_msg = str(e)
                print(f"Error processing segment {start_time}-{end_time}: {error_msg}")
                import traceback
                traceback.print_exc()
                api_errors.append(f"Segment {start_time}-{end_time}: {error_msg}")
            finally:
                # CRITICAL: Delete segment file immediately after processing to free memory
                if segment_path and os.path.exists(segment_path):
                    try:
                        os.unlink(segment_path)
                    except:
                        pass
                
                # Force garbage collection every 3 segments to free memory (more aggressive)
                if segments_processed % 3 == 0:
                    gc.collect()
        
        print(f"Processed {segments_processed}/{len(segments)} segments, found {segments_with_results} with tracks")
        
        # Deduplicate
        unique_tracks = deduplicate_tracks(all_tracks)
        
        # Format output
        if format_type == 'json':
            response_data = {
                'success': True,
                'tracks': unique_tracks,
                'count': len(unique_tracks),
                'segments_processed': segments_processed,
                'segments_total': len(segments),
                'segments_with_tracks': segments_with_results,
                'api_status': {
                    'acrcloud': acrcloud.is_available(),
                    'audd': audd.is_available(),
                    'shazam': shazam.is_available(),
                    'songfinder': songfinder.is_available()
                }
            }
            if api_errors:
                response_data['warnings'] = api_errors[:5]  # First 5 errors
            return jsonify(response_data)
        else:
            output_text = format_output(unique_tracks, format_type)
            if len(unique_tracks) == 0:
                output_text += f"\n\nNote: No tracks found. Processed {segments_processed}/{len(segments)} segments."
                if api_errors:
                    output_text += f"\nErrors encountered: {len(api_errors)}"
            return output_text, 200, {'Content-Type': 'text/plain; charset=utf-8'}
            
    except Exception as e:
        error_msg = str(e)
        error_traceback = traceback.format_exc()
        app.logger.error(f"ERROR in recognize(): {error_msg}")
        app.logger.error(error_traceback)
        print(f"ERROR: {error_msg}")
        print(error_traceback)
        
        # Provide more helpful error messages
        if "No module named" in error_msg:
            error_msg = f"Missing dependency: {error_msg}. Check requirements.txt"
        elif "ffmpeg" in error_msg.lower() or "ffprobe" in error_msg.lower():
            error_msg = f"FFmpeg not installed: {error_msg}. Add FFmpeg buildpack in Render settings. See FFMPEG_SETUP.md"
        elif "memory" in error_msg.lower() or "SIGKILL" in error_msg:
            error_msg = "Out of memory. File too large or FFmpeg not working. Try a smaller file or add FFmpeg buildpack."
        elif "timeout" in error_msg.lower():
            error_msg = "Request timeout. File processing took too long."
        
        return jsonify({
            'error': error_msg,
            'error_type': type(e).__name__,
            'traceback': error_traceback if app.debug else None,
            'hint': 'Check Render logs for full details'
        }), 500
    
    finally:
        # Clean up uploaded file
        try:
            os.unlink(filepath)
        except:
            pass

if __name__ == '__main__':
    # Check API keys
    is_valid, errors = Config.validate()
    if not is_valid:
        print("Warning: API keys not configured. Some features may not work.")
        print("Errors:", errors)
    
    # Enable debug in production for better error messages (can disable later)
    app.config['DEBUG'] = True
    app.run(debug=True, host='0.0.0.0', port=5000)


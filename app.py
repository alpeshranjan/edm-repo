"""Flask web application for EDM Track Recognition"""

import os
import tempfile
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import traceback

from src.cli import main as cli_main
from src.recognizers.acrcloud import ACRCloudRecognizer
from src.recognizers.audd import AuddRecognizer
from src.utils.config import Config
from src.audio_processor import AudioProcessor
from src.output.formatters import format_output

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200MB max file size
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
    acrcloud = ACRCloudRecognizer()
    audd = AuddRecognizer()
    
    return jsonify({
        'acrcloud_available': acrcloud.is_available(),
        'audd_available': audd.is_available(),
        'status': 'ready' if (acrcloud.is_available() or audd.is_available()) else 'no_apis'
    })

@app.route('/api/recognize', methods=['POST'])
def recognize():
    """Process uploaded audio file"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': f'Invalid file type. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
    
    # Get parameters
    format_type = request.form.get('format', 'json').lower()
    confidence_threshold = float(request.form.get('confidence_threshold', 0.5))
    segment_length = int(request.form.get('segment_length', 45))
    segment_overlap = int(request.form.get('segment_overlap', 15))
    
    # Save uploaded file
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    try:
        # Process the file
        processor = AudioProcessor(
            segment_length=segment_length,
            segment_overlap=segment_overlap
        )
        
        acrcloud = ACRCloudRecognizer()
        audd = AuddRecognizer()
        
        # Get segments
        segments = processor.segment_audio(filepath)
        all_tracks = []
        temp_files = []
        
        # Process each segment
        for start_time, end_time in segments:
            try:
                # Extract segment
                segment_path = processor.extract_segment(
                    filepath, start_time, end_time - start_time
                )
                temp_files.append(segment_path)
                
                # Try recognition
                results = []
                if acrcloud.is_available():
                    result = acrcloud.recognize(segment_path, start_time, end_time - start_time)
                    if result:
                        results.append(result)
                
                # Try fallback
                if (not results or results[0].confidence < confidence_threshold) and audd.is_available():
                    result = audd.recognize(segment_path, start_time, end_time - start_time)
                    if result:
                        results.append(result)
                
                # Merge results
                from src.cli import merge_results
                track = merge_results(results, start_time, end_time, confidence_threshold)
                if track:
                    all_tracks.append(track)
                    
            except Exception as e:
                print(f"Error processing segment {start_time}-{end_time}: {e}")
        
        # Clean up temp files
        for temp_file in temp_files:
            try:
                os.unlink(temp_file)
            except:
                pass
        
        # Deduplicate
        from src.cli import deduplicate_tracks
        unique_tracks = deduplicate_tracks(all_tracks)
        
        # Format output
        if format_type == 'json':
            return jsonify({
                'success': True,
                'tracks': unique_tracks,
                'count': len(unique_tracks)
            })
        else:
            output_text = format_output(unique_tracks, format_type)
            return output_text, 200, {'Content-Type': 'text/plain; charset=utf-8'}
            
    except Exception as e:
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc() if app.debug else None
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
    
    app.run(debug=True, host='0.0.0.0', port=5000)


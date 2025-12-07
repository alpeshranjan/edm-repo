document.getElementById('conf').addEventListener('input', function() {
    document.getElementById('confVal').textContent = this.value;
});

document.getElementById('uploadForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const status = document.getElementById('status');
    const results = document.getElementById('results');
    const btn = this.querySelector('button');
    
    status.style.display = 'block';
    status.textContent = 'Processing...';
    results.style.display = 'none';
    btn.disabled = true;
    
    try {
        const response = await fetch('/api/recognize', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            let errorMessage = `HTTP ${response.status}: `;
            try {
                const error = await response.json();
                errorMessage += error.error || error.message || 'Server error';
                if (error.traceback && response.status === 500) {
                    errorMessage += '\n\nDetails: ' + error.traceback.split('\n')[0];
                }
            } catch (e) {
                // If JSON parsing fails, try to get text
                try {
                    const text = await response.text();
                    errorMessage += text || 'Unknown error - check server logs';
                } catch (e2) {
                    errorMessage += 'Unknown error - check server logs';
                }
            }
            throw new Error(errorMessage);
        }
        
        const format = formData.get('format');
        const data = format === 'json' ? await response.json() : await response.text();
        
        if (format === 'json' && data.count === 0) {
            results.textContent = JSON.stringify(data, null, 2) + '\n\n⚠️ No tracks found. Check API keys or try a different file.';
        } else {
            results.textContent = format === 'json' ? JSON.stringify(data, null, 2) : data;
        }
        results.style.display = 'block';
        status.textContent = format === 'json' && data.count !== undefined ? `Done - Found ${data.count} tracks` : 'Done';
        
    } catch (error) {
        status.textContent = 'Error: ' + error.message;
        status.style.background = '#fee';
    } finally {
        btn.disabled = false;
    }
});

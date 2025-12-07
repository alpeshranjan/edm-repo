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
            const error = await response.json();
            throw new Error(error.error || 'Failed');
        }
        
        const format = formData.get('format');
        const data = format === 'json' ? await response.json() : await response.text();
        
        results.textContent = format === 'json' ? JSON.stringify(data, null, 2) : data;
        results.style.display = 'block';
        status.textContent = 'Done';
        
    } catch (error) {
        status.textContent = 'Error: ' + error.message;
        status.style.background = '#fee';
    } finally {
        btn.disabled = false;
    }
});

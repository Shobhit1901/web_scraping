const { spawn } = require('child_process');


function aggregateReviews(date) {
    return new Promise((resolve, reject) => {
        const pythonProcess = spawn('python3', ['.//services/daySummary.py', date]);

        let output = '';

        
        pythonProcess.stdout.on('data', (data) => {
            output += data.toString();
        });

        
        pythonProcess.stderr.on('data', (data) => {
            console.error(`Python Error: ${data.toString()}`);
        });

        
        pythonProcess.on('close', (code) => {
            if (code === 0) {
                resolve(output.trim());
            } else {
                reject(new Error('Failed to aggregate reviews.'));
            }
        });
    });
}

module.exports = aggregateReviews;

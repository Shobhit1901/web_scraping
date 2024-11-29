const { spawn } = require('child_process');

function runPythonScript() {
    return new Promise((resolve, reject) => {
        const pythonProcess = spawn('python', ['services/categorizeReview.py']);

        let output = '';
        pythonProcess.stdout.on('data', (data) => {
            output += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
            console.error(`Python stderr: ${data}`);
        });

        pythonProcess.on('close', (code) => {
            if (code !== 0) {
                reject(new Error(`Python script exited with code ${code}`));
            } else {
                try {
                    const reviews = JSON.parse(output);
                    resolve(reviews);
                } catch (error) {
                    reject(new Error('Error parsing JSON output from Python script.'));
                }
            }
        });
    });
}

module.exports = { runPythonScript };

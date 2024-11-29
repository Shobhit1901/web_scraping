const cron = require('node-cron');
const { runPythonScript } = require('../services/scrape');


cron.schedule('0 0 * * 0', () => {
    console.log('Running weekly scraping job...');
    runPythonScript().then((reviews) => {
        console.log('Scraped and categorized reviews:', reviews);
    }).catch((error) => {
        console.error('Error running scraping job:', error);
    });
});

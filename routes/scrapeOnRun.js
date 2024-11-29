const { runPythonScript } = require('../services/scrape'); 
const express = require('express')
const router = express.Router();
router.get('/',(req,res)=>{
    runPythonScript()
    .then((reviews) => {
        console.log('Initial scraping completed:', reviews);
        res.status(200).json({message:'Scraping is successfull'})
    })
    .catch((error) => {
        console.error('Error during initial scraping:', error);
    });
})

module.exports = router
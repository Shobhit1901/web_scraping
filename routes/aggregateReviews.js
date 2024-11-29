const express = require('express')
const aggregatedReviews = require('../utils/aggregateChildProcess')
const router = express.Router() ;

router.post('/', async (req,res)=>{
    const { date } = req.body;

    if (!date) {
        return res.status(400).json({ error: 'Date is required in the format "Month Day, Year"' });
    }

    try {
        const aggregatedReviews = await aggregateReviews(date);
        res.json({ aggregatedReviews });
    } catch (error) {
        console.error(error.message);
        res.status(500).json({ error: 'Failed to aggregate reviews.' });
    }
})

module.exports = router 
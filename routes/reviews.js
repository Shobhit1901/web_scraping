const express = require('express');
const Review = require('../models/Review');
const router = express.Router();


router.get('/', async (req, res) => {
    try {
        const review =await Review.find();

        console.log(review);
        res.json(review)
        
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

module.exports = router;

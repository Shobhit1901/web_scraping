const mongoose = require('mongoose');

const daySummary = mongoose.Schema({
     summary: String ,
     date: {
        type: Date,
        default: Date.now
     }
})

module.exports = mongoose.model('daysummary', daySummary);
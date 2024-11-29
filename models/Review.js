const mongoose = require('mongoose');
try{
    const reviewSchema = new mongoose.Schema({
        text: String,
        category: String,
        date: { type: Date, default: Date.now }
    });
    module.exports = mongoose.model('Review', reviewSchema);
} catch(err){
    console.log(err);
}




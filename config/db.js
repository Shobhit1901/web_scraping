const mongoose = require('mongoose');
require('dotenv').config();

mongoose.connect(process.env.MONGODB_URL,{
    useNewUrlParser: true,
    useUnifiedTopology: true,
})
.then(()=>{
    console.log("Database is connected")
}).catch((err)=>{
    console.log({err:`${err}`})
})

module.exports = mongoose.connection ;
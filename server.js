const express = require('express');
const connectDB = require('./config/db');
const bodyParser = require('body-parser');
const path = require('path');
require('dotenv').config();

const app = express();
connectDB();

app.use(bodyParser.json());
app.use('/api/auth', require('./routes/authRoutes'));
app.use('/api/appointment', require('./routes/appointmentRoutes'));
app.use(express.static(path.join(__dirname, 'views')));



// Route to serve login page
app.get('/login', (req, res) => {
    res.sendFile(path.join(__dirname, 'views', 'login.html'));
});

// Route to serve register page
app.get('/register', (req, res) => {
    res.sendFile(path.join(__dirname, 'views', 'register.html'));
});

// Route to serve appointment booking page
app.get('/appointment', (req, res) => {
    res.sendFile(path.join(__dirname, 'views', 'appointment.html'));
});

// // Root route redirects to login
// app.get('/', (req, res) => {
//     res.redirect('/index');
// });
//change is below 
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'views', 'index.html'));
});


const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});

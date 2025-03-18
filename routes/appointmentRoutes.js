const express = require('express');
const { bookAppointment } = require('../controllers/appointmentController');
const jwt = require('jsonwebtoken');
const router = express.Router();

const verifyToken = (req, res, next) => {
    const token = req.header('Authorization');
    if (!token) return res.status(401).json({ message: "Access denied" });

    try {
        const decoded = jwt.verify(token, process.env.JWT_SECRET);
        req.user = decoded;
        next();
    } catch (error) {
        res.status(400).json({ message: "Invalid token  You do not have an account. Please Login/ Register before booking " });
    }
};

router.post('/book', verifyToken, bookAppointment);

module.exports = router;

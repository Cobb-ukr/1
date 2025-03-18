const Appointment = require('../models/Appointment');
const nodemailer = require('nodemailer');
require('dotenv').config();

exports.bookAppointment = async (req, res) => {
    try {
        const { name, date, time, phoneNumber } = req.body;

        // Check for missing fields
        if (!name || !date || !time || !phoneNumber) {
            return res.status(400).json({ error: "All fields are required: name, date, time, and phoneNumber" });
        }

        // Create a new appointment record
        const newAppointment = new Appointment({ 
            userId: req.user.userId, name, date, time, phoneNumber 
        });
        await newAppointment.save();

        // Configure the email transporter
        const transporter = nodemailer.createTransport({
            service: 'gmail',
            host: "smtp.gmail.com",
            port: 465,
            secure: true,
            auth: {
                user: process.env.EMAIL,
                pass: process.env.EMAIL_PASSWORD
            }
        });

        // Define email options
        const mailOptions = {
            from: process.env.EMAIL,
            to: `${process.env.RECIPIENT_EMAIL}, ${req.user.email}`,
            subject: 'New Appointment Booking Confirmation',
            text: `You have a new appointment booking. \n\nAppointment Details:\nName: ${name}\nDate: ${date}\nTime: ${time}\nPhone Number: ${phoneNumber}\n\nThank you!`
        };

        // Send the email
        transporter.sendMail(mailOptions, (error, info) => {
            if (error) {
                console.log("Email error message: ", error.message); // Print email error message
                return res.status(500).json({ 
                    error: "Failed to send email",
                    details: error.message || error
                });
            } else {
                res.status(201).json({ message: "Appointment booked and email sent" });
            }
        });
    } catch (error) {
        console.log("Booking error message: ", error.message); // Print booking error message

        // Check for specific Mongoose validation errors
        if (error.name === 'ValidationError') {
            const validationErrors = Object.values(error.errors).map(err => err.message);
            console.log("Validation errors: ", validationErrors); // Print validation error messages
            return res.status(400).json({
                error: "Validation failed",
                details: validationErrors
            });
        }

        // Return other errors to the user
        console.log("General error message: ", error.message); // Print general error message
        res.status(500).json({ 
            error: "Failed to book appointment",
            details: error.message || error
        });
    }
};

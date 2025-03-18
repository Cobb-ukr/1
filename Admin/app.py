from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import ObjectId, errors
from datetime import datetime, timedelta
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os

from flask import Flask, jsonify, request

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb+srv://dentist:host@cluster0.l6uus.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["test"]
users_collection = db["users"]
appointments_collection = db["appointments"]

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/appointments/<status>')
def index(status):
    users = list(users_collection.find())
    if status == "Others":
        appointments = list(appointments_collection.find({"status": {"$nin": ["Completed", "In Progress"]}}))
    else:
        appointments = list(appointments_collection.find({"status": status}))
    return render_template("index.html", users=users, appointments=appointments, status=status)

@app.route('/delete_appointment/<appointment_id>', methods=['POST', 'GET'])
def delete_appointment(appointment_id):
    try:
        result = appointments_collection.delete_one({"_id": ObjectId(appointment_id)})
        if result.deleted_count > 0:
            return jsonify({"success": True, "message": "Appointment deleted successfully!"})
        else:
            return jsonify({"success": False, "message": "Appointment not found."})
    except Exception as e:
        return jsonify({"success": False, "message": f"Error deleting appointment: {str(e)}"})

@app.route('/mark_completed/<appointment_id>')
def mark_completed(appointment_id):
    appointments_collection.update_one({"_id": ObjectId(appointment_id)}, {"$set": {"status": "Completed"}})
    return redirect(url_for("index", status="In Progress"))

@app.route('/mark_in_progress/<appointment_id>')
def mark_in_progress(appointment_id):
    appointments_collection.update_one({"_id": ObjectId(appointment_id)}, {"$set": {"status": "In Progress"}})
    return redirect(url_for("index", status="Completed"))

@app.route('/change/<appointment_id>', methods=['GET', 'POST'])
def change_appointment(appointment_id):
    if request.method == 'POST':
        new_date = request.form['date']
        new_time = request.form['time']
        appointments_collection.update_one({"_id": ObjectId(appointment_id)}, 
                                           {"$set": {"date": new_date, "time": new_time}})
        return redirect(url_for("index", status="In Progress"))
    appointment = appointments_collection.find_one({"_id": ObjectId(appointment_id)})
    return render_template("change.html", appointment=appointment)

@app.route('/notes/<appointment_id>', methods=['GET', 'POST'])
def notes(appointment_id):
    appointment = appointments_collection.find_one({"_id": ObjectId(appointment_id)})
    if not appointment:
        return "Appointment not found", 404
    
    if request.method == 'POST':
        doctor_name = request.form.get('doctor_name', '').strip()
        point = request.form.get('point', '').strip()
        date_of_visit = request.form.get('subpoint', '').strip()
        
        new_note = {
            "doctor_name": doctor_name,
            "point": point,
            "Last_visit": date_of_visit
        }
        
        appointments_collection.update_one(
            {"_id": ObjectId(appointment_id)}, 
            {"$push": {"notes": new_note}}
        )
        return redirect(url_for("notes", appointment_id=appointment_id))
    
    return render_template("notes.html", appointment=appointment, notes=appointment.get("notes", []))

# Reminder Function
@app.route('/send_reminder/<appointment_id>', methods=['POST'])
def send_reminder(appointment_id):
    try:
        appointment = appointments_collection.find_one({"_id": ObjectId(appointment_id)})

        if not appointment:
            return jsonify({"success": False, "message": "Appointment not found."})

        if "userId" not in appointment:
            return jsonify({"success": False, "message": "User ID missing from appointment."})

        user = users_collection.find_one({"_id": ObjectId(appointment["userId"])})
        
        if not user or "email" not in user:
            return jsonify({"success": False, "message": "User email not found."})

        recipient_email = user["email"]
        subject = "Appointment Reminder"
        body = f"Reminder: You have an appointment on {appointment['date']} at {appointment['time']}."

        sender_email = "t32094532@gmail.com"
        sender_password = "nulhemighuxtygwy"

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = recipient_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())

        return jsonify({"success": True, "message": "Reminder email sent successfully!"})

    except Exception as e:
        return jsonify({"success": False, "message": f"Error sending email: {str(e)}"})


if __name__ == "__main__":
    app.run(debug=True)

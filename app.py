import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Hides TensorFlow info logs

import cv2
import json
# ... rest of your imports
import base64
import numpy as np
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, Response, flash, send_file
import pandas as pd
from config import Config
from database import (init_db, verify_admin, add_student, get_all_students, 
                      get_attendance_records, get_dashboard_stats)
from models.face_recognition import extract_embedding, generate_frames

app = Flask(__name__)
app.config.from_object(Config)

# Ensure directories exist
os.makedirs(Config.DATASET_DIR, exist_ok=True)
os.makedirs(Config.REPORTS_DIR, exist_ok=True)

# Initialize Database
init_db()

# --- Auth & Dashboard ---
@app.route('/')
def index():
    if 'admin_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if verify_admin(username, password):
            session['admin_id'] = username
            return redirect(url_for('dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin_id', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('login'))
    total_students, present_today, total_records = get_dashboard_stats()
    return render_template('dashboard.html', 
                           total_students=total_students, 
                           present_today=present_today, 
                           total_records=total_records)

# --- Student Registration ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'admin_id' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        name = request.form['name']
        department = request.form['department']
        semester = request.form['semester']
        image_data = request.form.get('image_data')
        
        if not image_data:
            flash('Please capture at least one face image.', 'warning')
            return redirect(url_for('register'))

        # Decode and save the base64 image
        header, encoded = image_data.split(",", 1)
        image_bytes = base64.b64decode(encoded)
        
        filename = f"{name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        image_path = os.path.join(Config.DATASET_DIR, filename)
        
        with open(image_path, "wb") as f:
            f.write(image_bytes)

        # Extract embedding
        embedding = extract_embedding(image_path)
        if embedding is None:
            os.remove(image_path)
            flash('No face detected. Please ensure your face is clearly visible.', 'danger')
            return redirect(url_for('register'))

        # Save to DB
        embedding_json = json.dumps(embedding)
        add_student(name, department, semester, embedding_json, image_path)
        
        flash(f'Student {name} registered successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('register.html')

# --- Face Recognition & Attendance ---
@app.route('/recognize')
def recognize():
    if 'admin_id' not in session:
        return redirect(url_for('login'))
    return render_template('recognize.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# --- Attendance History & Reports ---
@app.route('/history')
def history():
    if 'admin_id' not in session:
        return redirect(url_for('login'))
        
    search_query = request.args.get('search', '')
    date_filter = request.args.get('date', '')
    records = get_attendance_records(search_query, date_filter)
    return render_template('history.html', records=records, search=search_query, date_filter=date_filter)

@app.route('/export_csv')
def export_csv():
    if 'admin_id' not in session:
        return redirect(url_for('login'))
        
    search_query = request.args.get('search', '')
    date_filter = request.args.get('date', '')
    records = get_attendance_records(search_query, date_filter)
    
    data = []
    for r in records:
        data.append({
            'Name': r['Name'],
            'Department': r['Department'],
            'Semester': r['Semester'],
            'Date': r['Date'],
            'Time': r['Time'],
            'Status': r['Status']
        })
        
    df = pd.DataFrame(data)
    filename = os.path.join(Config.REPORTS_DIR, f"attendance_report_{datetime.now().strftime('%Y%m%d')}.csv")
    df.to_csv(filename, index=False)
    
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
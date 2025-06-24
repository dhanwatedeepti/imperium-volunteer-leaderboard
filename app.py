from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__, template_folder="templates")
CORS(app)

EXCEL_PATH = "data.xlsx"
SCORES_SHEET = "scores"
ATTENDANCE_SHEET = "attendance"

EMAIL_ADDRESS = "dhanwatedeepti2@gmail.com"
EMAIL_PASSWORD = "bauz wpui vkiy cewp"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scores")
def get_scores():
    try:
        df = pd.read_excel(EXCEL_PATH, sheet_name=SCORES_SHEET)
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/attendance/<name>")
def get_attendance(name):
    try:
        df = pd.read_excel(EXCEL_PATH, sheet_name=ATTENDANCE_SHEET)
        df.columns = df.columns.astype(str)  # ensure column names are strings
        name = name.strip().lower()

        # Find the row that matches the name (case insensitive)
        row = df[df['Name'].str.strip().str.lower() == name]

        if not row.empty:
            attendance_values = row.iloc[0, 1:]  # skip the 'Name' column
            attended = attendance_values.sum()
            total = attendance_values.count()
        else:
            attended = 0
            total = 0

        return jsonify({"attended": int(attended), "total": int(total)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/contact", methods=["POST"])
def contact():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    print("Received contact form:", data)  # Log the received form data

    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg['Subject'] = f"New message from {name}"
    msg.attach(MIMEText(f"From: {name}\nEmail: {email}\n\nMessage:\n{message}", 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Email sent successfully.")  # Confirmation log
        return jsonify({"status": "sent"})
    except Exception as e:
        print("Error sending email:", str(e))  # Show exact error in terminal
        return jsonify({"error": str(e)}), 500
#if __name__ == "__main__":
 #   app.run(debug=True)
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


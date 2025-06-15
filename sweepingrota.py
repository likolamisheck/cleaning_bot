from flask import Flask, render_template_string, send_file
import qrcode
import datetime
import io
import os

app = Flask(__name__)

# Rota list
rota = [
    "Likola Misheck",
    "Kasakula George",
    "Musaka Milimo",
    "Temba Leadway"
]

# Weekly rotation based on start date (starting every Sunday)
def get_person_on_duty():
    today = datetime.date.today()
    start_date = datetime.date(2024, 6, 16)  # starting anchor Sunday
    delta_weeks = ((today - start_date).days) // 7
    index = delta_weeks % len(rota)
    return rota[index]

# Home page
@app.route('/')
def home():
    person = get_person_on_duty()
    return render_template_string("""
        <html>
        <head>
            <title>Weekly Duty Rota</title>
            <style>
                body {
                    background: linear-gradient(to right, #4facfe, #00f2fe);
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }
                .canvas {
                    background-color: rgba(255, 255, 255, 0.95);
                    padding: 50px;
                    border-radius: 20px;
                    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
                    text-align: center;
                }
                h1 {
                    color: #222;
                    margin-bottom: 30px;
                    font-size: 36px;
                }
                p {
                    font-size: 28px;
                    font-weight: bold;
                    color: #007BFF;
                }
            </style>
        </head>
        <body>
            <div class="canvas">
                <h1>Weekly Duty Rota</h1>
                <p>The person on duty is: {{ person }}</p>
            </div>
        </body>
        </html>
    """, person=person)

# QR code route
@app.route('/qrcode')
def generate_qrcode():
    link = os.getenv("SERVER_URL", "http://127.0.0.1:5000/")
    qr = qrcode.make(link)
    img_io = io.BytesIO()
    qr.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

# Start server
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

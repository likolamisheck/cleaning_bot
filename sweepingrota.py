from flask import Flask, render_template_string, send_file, request
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
@app.route('/', methods=['GET', 'HEAD'])
def home():
    person = get_person_on_duty()

    if request.method == 'HEAD':
        return '', 200

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Weekly Duty Rota</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background: linear-gradient(to right, #4facfe, #00f2fe);
                height: 100vh;
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .card {
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            }
            .card-title {
                font-size: 2rem;
                font-weight: bold;
            }
            .person-name {
                font-size: 1.8rem;
                color: #007BFF;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="card text-center">
            <h1 class="card-title">Weekly Duty Rota</h1>
            <p class="person-name">The person on duty is:<br> {{ person }}</p>
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

# Start server (for local testing)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


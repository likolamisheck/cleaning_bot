from flask import Flask, render_template_string, send_file, request
import qrcode
import datetime
import io
import os

app = Flask(__name__)

rota = [
    "Likola Misheck",
    "Kasakula George",
    "Musaka Milimo",
    "Temba Leadway"
]

def get_person_on_duty(week_offset=0):
    today = datetime.date.today()
    start_date = datetime.date(2024, 6, 16)  # starting anchor Sunday
    delta_weeks = ((today - start_date).days) // 7 + week_offset
    index = delta_weeks % len(rota)
    return rota[index]

def get_days_until_next_sunday():
    today = datetime.date.today()
    days_until_sunday = (6 - today.weekday()) % 7
    return days_until_sunday if days_until_sunday != 0 else 7

@app.route('/', methods=['GET', 'HEAD'])
def home():
    person = get_person_on_duty()
    next_person = get_person_on_duty(week_offset=1)
    days_left = get_days_until_next_sunday()

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
        <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/727/727245.png" type="image/png">
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
                background-color: white;
                text-align: center;
                animation: fadeIn 1.5s ease;
            }
            .logo {
                width: 80px;
                margin-bottom: 20px;
                animation: popIn 1s ease;
            }
            .card-title {
                font-size: 2rem;
                font-weight: bold;
            }
            .person-name {
                font-size: 1.8rem;
                color: #007BFF;
                margin-top: 20px;
                animation: slideIn 1.2s ease forwards;
                opacity: 0;
            }
            .next-person {
                margin-top: 10px;
                font-size: 1.3rem;
                color: #555;
            }
            .countdown {
                margin-top: 20px;
                font-size: 1.2rem;
                color: #333;
            }

            @keyframes slideIn {
                from { transform: translateY(20px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }

            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }

            @keyframes popIn {
                from { transform: scale(0); opacity: 0; }
                to { transform: scale(1); opacity: 1; }
            }

            @media (prefers-color-scheme: dark) {
                body {
                    background: linear-gradient(to right, #141e30, #243b55);
                }
                .card {
                    background-color: #1e1e1e;
                    box-shadow: 0 4px 20px rgba(255, 255, 255, 0.1);
                }
                .card-title { color: #ffffff; }
                .person-name { color: #4fa3ff; }
                .next-person { color: #aaa; }
                .countdown { color: #ccc; }
            }
        </style>
    </head>
    <body>
        <div class="card">
            <img src="https://cdn-icons-png.flaticon.com/512/727/727245.png" class="logo" alt="Logo">
            <h1 class="card-title">Weekly Duty Rota</h1>
            <p class="person-name">The person on duty is:<br><strong>{{ person }}</strong></p>
            <div class="next-person">Next week: {{ next_person }}</div>
            <div class="countdown">{{ days_left }} day{{ 's' if days_left != 1 else '' }} left until next rotation</div>
        </div>
    </body>
    </html>
    """, person=person, next_person=next_person, days_left=days_left)

@app.route('/qrcode')
def generate_qrcode():
    link = os.getenv("SERVER_URL", "http://127.0.0.1:5000/")
    qr = qrcode.make(link)
    img_io = io.BytesIO()
    qr.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

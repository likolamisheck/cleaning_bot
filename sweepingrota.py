from flask import Flask, render_template_string, send_file, request, url_for
import qrcode
import datetime
import io
import os

app = Flask(__name__)

# Your exact rota - 100% correct filenames matching your static/photos folder
rota = [
    {"name": "Likola Misheck", "photo": "likola.jpg"},
    {"name": "Kasakula George", "photo": "george.jpg"},
    {"name": "Musaka Milimo", "photo": "milimo.jpg"},
    {"name": "Temba Leadway", "photo": "temba.jpg"},
]

# Safety fallback if somehow file is missing
def safe_photo(photo_filename):
    photo_path = os.path.join(app.static_folder, 'photos', photo_filename)
    if os.path.isfile(photo_path):
        return photo_filename
    else:
        return "default.png"  # you can put any default placeholder image later

def get_person_on_duty(week_offset=0):
    today = datetime.date.today()
    start_date = datetime.date(2024, 6, 16)
    delta_weeks = ((today - start_date).days) // 7 + week_offset
    index = delta_weeks % len(rota)
    person = rota[index].copy()
    person['photo'] = safe_photo(person['photo'])
    return person

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
        <style>
            body {
                background: url('{{ url_for('static', filename='photos/city.png') }}') no-repeat center center fixed;
                background-size: cover;
                height: 100vh;
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                font-family: 'Segoe UI', sans-serif;
            }
            .card {
                padding: 40px;
                border-radius: 20px;
                background: rgba(255, 255, 255, 0.9);
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
                text-align: center;
                max-width: 420px;
            }
            .profile-pic {
                width: 140px;
                height: 140px;
                border-radius: 50%;
                object-fit: cover;
                margin-bottom: 10px;
                border: 4px solid #007BFF;
            }
            .next-profile-pic {
                width: 100px;
                height: 100px;
                border-radius: 50%;
                object-fit: cover;
                margin-bottom: 10px;
                border: 3px solid #28a745;
            }
            .card-title { font-size: 2rem; font-weight: bold; color: #333; }
            .person-name { font-size: 1.6rem; font-weight: 600; color: #007BFF; }
            .next-person-name { font-size: 1.5rem; font-weight: 600; color: #28a745; }
            .countdown { margin-top: 15px; font-size: 1.2rem; color: #333; }
            .progress-container { background: #e0e0e0; border-radius: 10px; margin-top: 10px; height: 15px; overflow: hidden; }
            .progress-bar { height: 100%; background-color: #007BFF; transition: width 0.5s ease; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1 class="card-title">Weekly Duty Rota</h1>

            <div>
                <img src="{{ url_for('static', filename='photos/' + person.photo) }}" class="profile-pic">
                <div class="person-name">The person on duty is:<br>{{ person.name }}</div>
            </div>

            <div style="margin-top: 20px;">
                <div>Next person:</div>
                <img src="{{ url_for('static', filename='photos/' + next_person.photo) }}" class="next-profile-pic">
                <div class="next-person-name">{{ next_person.name }}</div>
            </div>

            <div class="countdown">{{ days_left }} day{{ 's' if days_left != 1 else '' }} left until next rotation</div>

            <div class="progress-container">
                <div class="progress-bar" style="width: {{ (7 - days_left) * 100 / 7 }}%;"></div>
            </div>
        </div>
    </body>
    </html>
    """, person=person, next_person=next_person, days_left=days_left)

@app.route('/qrcode')
def generate_qrcode():
    link = os.getenv("SERVER_URL", "https://cleaning-bot-gl2r.onrender.com/")
    qr = qrcode.make(link)
    img_io = io.BytesIO()
    qr.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

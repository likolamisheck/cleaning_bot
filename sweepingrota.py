from flask import Flask, render_template_string, send_file
import qrcode
import datetime
import io
import os

app = Flask(__name__)

# Your list of people on the rota
rota = [
    "Likola Misheck",
    "Kasakula George",
    "Musaka Milimo",
    "Temba Leadway"
]

# Weekly rotation logic
def get_person_on_duty():
    today = datetime.date.today()
    index = (today.toordinal() // 7) % len(rota)
    return rota[index]

# Home route
@app.route('/')
def home():
    person = get_person_on_duty()
    return render_template_string("""
        <h1>Weekly Duty Rota</h1>
        <p><strong>{{ person }}</strong> is on duty this week.</p>
    """, person=person)

# QR code route
@app.route('/qrcode')
def generate_qrcode():
    # Get the server URL from environment variable (useful after deployment)
    link = os.getenv("SERVER_URL", "http://127.0.0.1:5000/")
    qr = qrcode.make(link)
    img_io = io.BytesIO()
    qr.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

# Running locally
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

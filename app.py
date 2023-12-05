from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import vonage
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'  # Use SQLite for simplicity
db = SQLAlchemy(app)

VONAGE_API_KEY = 'a69c0882'
VONAGE_API_SECRET = '4FCLX4nXmxq6KqQA'

client = vonage.Client(key=VONAGE_API_KEY, secret=VONAGE_API_SECRET)
sms = vonage.Sms(client)

class User(db.Model):
    username = db.Column(db.String(80), nullable=False, primary_key=True)
    password = db.Column(db.String(200), nullable=False)
    mobile = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(10), nullable=False)

otp_data = {}

def generate_otp():
    return str(random.randint(1000, 9999))

valid_username = ["user","abc","bcd"]
valid_password = ["password","abc","bcd"]

@app.route('/')
def index():
    return render_template('signup.html')

@app.route('/loginp')
def loginp():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        mobile = request.form['mob']
        email = request.form['mail']
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            return "User already exists. Please log in."

        new_user = User(username=username, password=password, mobile=mobile, email=email)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        global username1
        username1 = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username1).first()
        if user.password==password:
            global user_phone_number
            user_phone_number = user.mobile
            
            # Generate a new OTP
            otp = generate_otp()
            
            # Store the OTP in the dictionary, associated with the user's phone number
            otp_data[user_phone_number] = otp

            # Send the OTP via SMS
            message = f'Your OTP code is: {otp}'
            response = sms.send_message({
                'from': 'YourApp',
                'to': user_phone_number,
                'text': message,
            })

            if response["messages"][0]["status"] == "0":
                return redirect(url_for('verify'))
            else:
                print(f"Message failed with error: {response['messages'][0]['error-text']}")
        return 'Invalid login credentials'
    return render_template('login.html')

@app.route('/verify')
def verify():
    return render_template('otp_ver.html')
    

@app.route('/verify_otp', methods=['POST','GET'])
def verify_otp():
    user_entered_otp = request.form.get('otp')

    stored_otp = otp_data.get(user_phone_number)

    if stored_otp == user_entered_otp:
        return 'OTP is valid. You can proceed.'
    else:
        return 'Invalid OTP. Please try again.'

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()
    print(otp_data)

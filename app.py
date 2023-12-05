from flask import Flask, request, render_template, redirect, url_for
import vonage
import random
import datetime

app = Flask(__name__)

VONAGE_API_KEY = 'a69c0882'
VONAGE_API_SECRET = '4FCLX4nXmxq6KqQA'

client = vonage.Client(key=VONAGE_API_KEY, secret=VONAGE_API_SECRET)
sms = vonage.Sms(client)

otp_data = {}

def generate_otp():
    return str(random.randint(1000, 9999))

valid_username = ["user","abc","bcd"]
valid_password = ["password","abc","bcd"]

@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in valid_username:
            i=valid_username.index(username)
            if valid_password[i]==password:
                return redirect(url_for('otp_verification'))
        return 'Invalid login credentials'
    return render_template('login.html')
    
@app.route('/otp_verification')
def otp_verification():
    return render_template('otp_gen.html')

@app.route('/verify')
def verify():
    return render_template('otp_ver.html')

@app.route('/send_otp', methods=['POST'])
def send_otp():
    global user_phone_number
    user_phone_number = request.form.get('phone_number')
    
    # Generate a new OTP
    otp = generate_otp()
    
    # Store the OTP in the dictionary, associated with the user's phone number
    otp_data[user_phone_number] = otp
    global create_time
    create_time=datetime.datetime.now()

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

@app.route('/verify_otp', methods=['POST','GET'])
def verify_otp():
    user_entered_otp = request.form.get('otp')
    ver_time=datetime.datetime.now()
    time_difference = ver_time - create_time
    time_difference_minutes = time_difference.total_seconds() / 60

    stored_otp = otp_data.get(user_phone_number)

    if stored_otp == user_entered_otp and time_difference_minutes<=1:
        return 'OTP is valid. You can proceed.'
    else:
        return 'Invalid OTP. Please try again.'

if __name__ == '__main__':
    app.run()
    print(otp_data)

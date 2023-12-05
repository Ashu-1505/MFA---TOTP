# MFA---TOTP

In our mini-project we have implemented multifactor authentication for a web application created using Python Flask. The application opens with a sign-up page. If the user already has an account they can directly go to Log-in page. 
After the user enters the sign-up details, the details gets stored in the SQLAlchemy database. If the log-in credentials entered by the user is correct, the applications send an OTP to the mobile number entered by the user, then the OTP validation takes place. 
This is a time-based OTP protocol where the time is recorded at the time of generation and at the time of verification. If the time difference is more than 1 minute the OTP will be invalid.
For sending the OTP to the mobile number, we are using Vonage - a third party SMS messenger. For that we are importing Vonage as a module.

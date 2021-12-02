from flask import Flask,render_template,request
from flask_mail import Mail, Message



app = Flask(__name__)
mail=Mail(app)
app.config['MAIL_SERVER']='mail.aadhyahomoeoclinic.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'no-reply@aadhyahomoeoclinic.com'
app.config['MAIL_PASSWORD'] = 'Pi9Mh9srfh.a'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)






@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        print(e)

@app.route('/aboutus')
def aboutus():
    try:
        return render_template('about.html')
    except Exception as e:
        print(e)

@app.route('/contactus')
def contactus():
    try:
        return render_template('contact-us.html')
    except Exception as e:
        print(e)

@app.route('/treatments')
def treatment():
    try:
        return render_template('departments-2.html')
    except Exception as e:
        print(e)

@app.route('/appointment' ,methods=['GET','POST'])
def appointment():
    try:
        if request.method=='POST':
            name = request.form['name']
            email = request.form['email']
            mobno = request.form['mobno']
            problem = request.form['treatment_name']
            
            msg = Message('Aadhya Online Consultancy', sender = 'no-reply@aadhyahomoeoclinic.com', recipients = ['info@aadhyahomoeoclinic.com',str(email)])
            msg.body = "Name: "+ name + "\nEmail: "+ email +"\nPhone Number: "+mobno+"\nConsulting For: "+problem
            mail.send(msg)
        return render_template('appointment.html')
    except Exception as e:
        print(e)








if __name__ == '__main__':
    app.run(debug=True)
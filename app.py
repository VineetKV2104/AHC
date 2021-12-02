from operator import add
from flask import Flask,render_template,request,redirect,session
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session




app = Flask(__name__)

mail=Mail(app)
app.config['MAIL_SERVER']='mail.aadhyahomoeoclinic.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'no-reply@aadhyahomoeoclinic.com'
app.config['MAIL_PASSWORD'] = 'Pi9Mh9srfh.a'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ahc.sqlite3'
app.config['STATIC_FOLDER'] = "static"
db = SQLAlchemy(app)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

class admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(100), nullable=False)
    Password = db.Column(db.String(100), nullable=False)
    

class Appointments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    number = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    problem = db.Column(db.String(100), nullable=False)
    paid = db.Column(db.Integer)
    

####### Auth ########


@app.route('/login',methods=['GET','POST'])
def login():
    try:
        if request.method=='POST':
            if request.form['uname'] == '' or request.form['pass']=='':
                return redirect("/login")
            creds = admin.query.filter_by(Username = request.form['uname'],Password=request.form['pass']).first()
            print(creds)
            if creds == None:
                return redirect("/login")
            else:
                session["name"] = request.form['uname']
                return redirect("/admin")
            
        return render_template("login.html")
    except Exception as e:
        print(e)
    
@app.route("/logout",methods=['GET','POST'])
def logout():
    try:
        session.clear()
        return redirect("/login")
    except Exception as e:
        print(e)

@app.route('/admin')
def Admin():
    try:
        if not session.get("name"):
            # if not there in the session then redirect to the login page
            return redirect("/login")
        appointments = Appointments.query.all()
        return render_template('admin.html',appointments=appointments)
    except Exception as e:
        print(e)

@app.route('/paid')
def paid():
    try:
        if not session.get("name"):
            # if not there in the session then redirect to the login page
            return redirect("/login")
        flag = request.args['id']
        appointments = Appointments.query.filter_by(id=flag).first()
        appointments.paid = 1
        db.session.commit()
        return redirect("/admin")
    except Exception as e:
        print(e)

@app.route('/unpaid')
def unpaid():
    try:
        if not session.get("name"):
            # if not there in the session then redirect to the login page
            return redirect("/login")
        flag = request.args['id']
        appointments = Appointments.query.filter_by(id=flag).first()
        appointments.paid = 0
        db.session.commit()
        return redirect("/admin")
    except Exception as e:
        print(e)


#####################

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
            
            add_appointment = Appointments(name=name,number=mobno,email=email,problem=problem,paid=0)
            db.session.add(add_appointment)
            db.session.commit()

            msg = Message('Aadhya Online Consultancy', sender = 'no-reply@aadhyahomoeoclinic.com', recipients = ['info@aadhyahomoeoclinic.com',str(email)])
            msg.body = "Name: "+ name + "\nEmail: "+ email +"\nPhone Number: "+mobno+"\nConsulting For: "+problem
            mail.send(msg)
            return render_template('appointment.html',success_message=1)
        return render_template('appointment.html',success_message=0)
    except Exception as e:
        print(e)



if __name__ == '__main__':
    app.run(debug=True)
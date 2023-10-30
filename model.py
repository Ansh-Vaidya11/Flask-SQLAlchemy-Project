from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:test@123@127.0.0.1/Final'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class College(db.Model):
    CollegeName = db.Column(db.String(200), primary_key=True)
    CollegeTotalStudents = db.Column(db.Integer, nullable=True)  

class Buildings(db.Model):
    BuildingID = db.Column(db.Integer, primary_key=True)
    BuildingName = db.Column(db.String(200), nullable=False)
    CollegeName = db.Column(db.String(200), nullable=False, index=True) 

class Classrooms(db.Model):
    RoomNumber = db.Column(db.Integer, primary_key=True)
    HasProjector = db.Column(db.String(200), nullable=False)
    BuildingID = db.Column(db.Integer, nullable=False, index=True) 

class Textbook(db.Model):
    TextbookISBN = db.Column(db.String(200), primary_key=True) 
    TextbookTitle = db.Column(db.String(200), nullable=False)
    TextbookAuthor = db.Column(db.String(200), nullable=False)

class Course(db.Model):
    CourseID = db.Column(db.Integer, primary_key=True)
    CourseName = db.Column(db.String(200), nullable=False)
    TextbookISBN = db.Column(db.String(200), nullable=False, index=True) 

class Person(db.Model):
    PersonID = db.Column(db.Integer, primary_key=True)
    PersonPhoneNumber = db.Column(db.String(200), nullable=False)
    PersonName = db.Column(db.String(200), nullable=False)

class Faculty(db.Model):
    FacultyID = db.Column(db.Integer, primary_key=True)
    FacultyTitle = db.Column(db.String(200), nullable=False)
    FacultySalary = db.Column(db.Integer, nullable=False)
    FacultyName = db.Column(db.String(200), nullable=False)
    PersonID = db.Column(db.Integer, nullable=False, index=True)  

class Interns(db.Model):
    InternID = db.Column(db.Integer, primary_key=True)
    PersonID = db.Column(db.Integer, nullable=False, index=True)  
    InternHourlyWage = db.Column(db.Float(precision=10, asdecimal=True), nullable=False) 

class Section(db.Model):
    SectionID = db.Column(db.Integer, primary_key=True)
    SectionDate = db.Column(db.DateTime, default=datetime.utcnow)
    RoomNumber = db.Column(db.Integer, nullable=False, index=True)  
    CourseID = db.Column(db.Integer, nullable=False, index=True) 
    BuildingID = db.Column(db.Integer, nullable=False, index=True)  
    PersonID = db.Column(db.Integer, nullable=False, index=True)  

class Student(db.Model):
    StudentID = db.Column(db.Integer, primary_key=True)
    StudentGPA = db.Column(db.Float(precision=10, asdecimal=True), nullable=False) 
    StudentName = db.Column(db.String(200), nullable=False)
    PersonID = db.Column(db.Integer, nullable=False, index=True)

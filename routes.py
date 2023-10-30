from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:test1234@localhost/Final'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Person(db.Model):
    __tablename__ = 'Person'
    PersonID = db.Column(db.Integer, primary_key=True)
    PersonPhoneNumber = db.Column(db.String(200), nullable=False)
    PersonName = db.Column(db.String(200), nullable=False)
    faculty = db.relationship('Faculty', back_populates='person')
    student = db.relationship('Student', back_populates='person')
    interns = db.relationship('Interns', back_populates='person')
    section = db.relationship('Section', back_populates='person')

class Faculty(db.Model):
    __tablename__ = 'Faculty'
    FacultyID = db.Column(db.Integer, primary_key=True)
    FacultyTitle = db.Column(db.String(200), nullable=False)
    FacultySalary = db.Column(db.Integer, nullable=False)
    FacultyName = db.Column(db.String(200), nullable=False)
    PersonID = db.Column(db.Integer, db.ForeignKey('Person.PersonID'), nullable=False)
    person = db.relationship('Person', back_populates='faculty')

class College(db.Model):
    __tablename__ = 'College'
    CollegeName = db.Column(db.String(200), primary_key=True)
    CollegeTotalStudents = db.Column(db.Integer, nullable=True)
    buildings = db.relationship('Buildings', back_populates='college')

class Buildings(db.Model):
    __tablename__ = 'Buildings'
    BuildingID = db.Column(db.Integer, primary_key=True)
    BuildingName = db.Column(db.String(200), nullable=False)
    CollegeName = db.Column(db.String(200), db.ForeignKey('College.CollegeName'), nullable=False)
    college = db.relationship('College', back_populates='buildings')
    classrooms = db.relationship('Classrooms', back_populates='buildings')
    section = db.relationship('Section', back_populates='buildings')

class Classrooms(db.Model):
    __tablename__ = 'Classrooms'
    RoomNumber = db.Column(db.Integer, primary_key=True)
    HasProjector = db.Column(db.String(200), nullable=False)
    BuildingID = db.Column(db.Integer, db.ForeignKey('Buildings.BuildingID'), nullable=False)
    buildings = db.relationship('Buildings', back_populates='classrooms')
    section = db.relationship('Section', back_populates='classrooms')

class Textbook(db.Model):
    __tablename__ = 'Textbook'
    TextbookISBN = db.Column(db.String(200), primary_key=True)
    TextbookTitle = db.Column(db.String(200), nullable=False)
    TextbookAuthor = db.Column(db.String(200), nullable=False)
    course = db.relationship('Course', back_populates='textbook')

class Student(db.Model):
    __tablename__ = 'Student'
    StudentID = db.Column(db.Integer, primary_key=True)
    StudentGPA = db.Column(db.Float(precision=10, asdecimal=True), nullable=False)
    StudentName = db.Column(db.String(200), nullable=False)
    PersonID = db.Column(db.Integer, db.ForeignKey('Person.PersonID'), nullable=False)
    person = db.relationship('Person', back_populates='student')

class Course(db.Model):
    __tablename__ = 'Course'
    CourseID = db.Column(db.Integer, primary_key=True)
    CourseName = db.Column(db.String(200), nullable=False)
    TextbookISBN = db.Column(db.String(200), db.ForeignKey('Textbook.TextbookISBN'), nullable=False)
    textbook = db.relationship('Textbook', back_populates='course')
    section = db.relationship('Section', back_populates='course')

class Section(db.Model):
    __tablename__ = 'Section'
    SectionID = db.Column(db.Integer, primary_key=True)
    SectionDate = db.Column(db.DateTime, default=datetime.utcnow)
    RoomNumber = db.Column(db.Integer, db.ForeignKey('Classrooms.RoomNumber'), nullable=False)
    CourseID = db.Column(db.Integer, db.ForeignKey('Course.CourseID'), nullable=False)
    BuildingID = db.Column(db.Integer, db.ForeignKey('Buildings.BuildingID'), nullable=False)
    PersonID = db.Column(db.Integer, db.ForeignKey('Person.PersonID'), nullable=False)
    classrooms = db.relationship('Classrooms', back_populates='section')
    course = db.relationship('Course', back_populates='section')
    buildings = db.relationship('Buildings', back_populates='section')
    person = db.relationship('Person', back_populates='section')

class Interns(db.Model):
    __tablename__ = 'Interns'
    InternID = db.Column(db.Integer, primary_key=True)
    PersonID = db.Column(db.Integer, db.ForeignKey('Person.PersonID'), nullable=False)
    person = db.relationship('Person', back_populates='interns')
    InternHourlyWage = db.Column(db.Float(precision=10, asdecimal=True), nullable=False)

@app.route('/get-college-details', methods=['GET'])
def college_details():
    college_data = db.session.query(College).join(Buildings).join(Classrooms).all()
    college_list = []

    for college in college_data:
        buildings_list = list()

        for item in college.buildings:
            a = dict()
            a[item.BuildingName] = list()

            for room in item.classrooms:
                b = dict()
                # b = {room.RoomNumber: {'HasProjector': room.HasProjector}}
                b['HasProjector'] = room.HasProjector
                b['RoomNumber'] = room.RoomNumber
                a[item.BuildingName].append(b)
                # a[item.BuildingName].append(room.__dict__)

            buildings_list.append(a)

        college_dict = {
            'CollegeName': college.CollegeName,
            'Buildings': buildings_list
        }
        college_list.append(college_dict)

    return jsonify(college_list)

@app.route('/get-student-details', methods=['GET'])
def student_details():
    student_data = db.session.query(Student).all()
    student_list = []

    for student in student_data:
        student_dict = {
            'StudentID': student.StudentID,
            'StudentName': student.StudentName,
            'StudentGPA': student.StudentGPA
        }
        student_list.append(student_dict)

    return jsonify(student_list)

@app.route('/get-course-details', methods=['GET'])
def course_details():
    course_data = db.session.query(Course, Textbook).join(Textbook, Course.TextbookISBN == Textbook.TextbookISBN).all()
    course_list = []

    for course, textbook in course_data:
        course_dict = {
            'CourseID': course.CourseID,
            'CourseName': course.CourseName,
            'TextbookISBN': textbook.TextbookISBN,
            'TextbookTitle': textbook.TextbookTitle,
            'TextbookAuthor': textbook.TextbookAuthor
        }
        course_list.append(course_dict)

    return jsonify(course_list)

@app.route('/get-faculty-details', methods=['GET'])
def faculty_details():
    faculty_data = db.session.query(Faculty, Person).join(Person, Faculty.PersonID == Person.PersonID).all()
    faculty_list = []

    for faculty, person in faculty_data:
        faculty_dict = {
            'FacultyID': faculty.FacultyID,
            'FacultyTitle': faculty.FacultyTitle,
            'FacultySalary': faculty.FacultySalary,
            'FacultyName': faculty.FacultyName,
            'PersonID': person.PersonID,
            'PersonName': person.PersonName,
            'PersonPhoneNumber': person.PersonPhoneNumber
        }
        faculty_list.append(faculty_dict)

    return jsonify(faculty_list)

if __name__ == "__main__":
    app.run(debug=True)

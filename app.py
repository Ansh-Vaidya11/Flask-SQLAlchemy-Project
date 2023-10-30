from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.id}>' 

@app.route('/add-task', methods=['POST'])
def index():
    task_content = request.json
    new_task = Todo(content=task_content['Task'])

    try:
        db.session.add(new_task)
        db.session.commit()
        return 'Your Task has been added'
    except:
        return 'There was an error adding your task'

@app.route('/delete-task/<int:id>', methods=['POST'])
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return 'Your Task has been deleted'
    except:
        return 'There was an error deleting your task'
    
@app.route('/update-task/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error updating your task'
    
    else:
        return render_template('update.html', task=task)
    
@app.route('/list-tasks', methods=['GET'])
def list_tasks():
   tasks = Todo.query.all()
   tasks_list = []

   for task in tasks:
       tasks_dict = {
           'Name': task.content,
           'Date': task.date_created,
           'ID': task.id
       }
       tasks_list.append(tasks_dict)

   return jsonify(tasks_list)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app)

class todo(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    description=db.Column(db.String(500),nullable=False)
    completed=db.Column(db.Boolean, default=False)
    datetime=db.Column(db.DateTime, default=datetime.utcnow)
    

    def __repr__(self):
        return '<Task %r>' % self.id
    
with app.app_context():
    db.create_all()

@app.route('/', methods=['POST','GET'])
def add_task():
    if request.method == 'POST':
        task_title=request.form.get('title')
        task_content=request.form.get('description')

        Todo=todo(title=task_title,description=task_content)
        db.session.add(Todo)
        db.session.commit()
    
    todos= todo.query.all()
    
    return render_template("index.html",todos=todos)


@app.route('/delete/<int:id>')
def delete(id):
    todos= todo.query.filter_by(id=id).first()
    db.session.delete(todos)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
    if request.method == 'POST':
        todos= todo.query.filter_by(id=id).first()
        task_title=request.form.get('title')
        task_content=request.form.get('description')
        todos.title=task_title
        todos.description=task_content
        db.session.add(todos)
        db.session.commit() 
        return redirect('/') 
    
    todos= todo.query.filter_by(id=id).first()
    return render_template("update.html",todos=todos)

if __name__=="__main__":
    app.run(debug=True, port=8000)
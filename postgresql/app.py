from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
# from flask_restful import Resource, Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:11231@localhost:5432/postgresql'

db = SQLAlchemy(app)

class Task(db.Model):
    # __table__='tasks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    done =db.Column(db.Boolean, default=True)

with app.app_context():
    db.create_all()

@app.route('/tasks')
def get_tasks():
    tasks = Task.query.all()
    task_list = [
        {
            'id': task.id,
            'title': task.title,
            'done':task.done
        } for task in tasks
    ]
    return jsonify({"tasks":task_list})

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    print(data)
    new_task = Task(
        title = data['title'],
        done = data['done']
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message':'Task created'}), 201


@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    print (task)
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    return jsonify({'id': task.id, 'title': task.title, 'done': task.done})

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)
    print(task)
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    data = request.json
    print(task)
    task.title = data['title']
    task.done = data['done']
    db.session.commit()
    return jsonify({'message': 'Task updated successfully'})

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'})

if __name__ == '__main__':
    app.run()     
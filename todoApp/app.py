from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://aashishraj:123@localhost:5432/todoapp'
db=SQLAlchemy(app)
migrate = Migrate(app, db)

# class Todo(db.Model):
#     __tablename__ = 'todos'
#     id = db.Column(db.Integer, primary_key=True)
#     description = db.Column(db.String(), nullable=False)
#     completed = db.Column(db.Boolean, nullable=False, default=False)
#     list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)
#
# class TodoList(db.Model):
#     __tablename__ = 'todolists'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(), nullable=False)
#     todos = db.relationship('Todo', backref='list', lazy=True)
#
# def __repr__(self):
#     return f'<To  do ID: {self.id}, Description: {self.description}>'
#
# # @app.route('/')
# # def index():
# #     return render_template('index.html', data=Todo.query.order_by('id').all())
# @app.route('/')
# def index():
#     return redirect(url_for('get_list_todos', list_id=1))
#
# @app.route('/todos/create', methods=['POST'])
# def create_todo():
#     # description = request.form.get('description', '')
#     # todo = Todo(description=description)
#     # db.session.add(todo)
#     # db.session.commit()
#     # return redirect(url_for('index'))
#     error = False
#     body = {}
#     # try:
#     #     description = request.get_json()['description']
#     #     todo = Todo(description=description)
#     #     db.session.add(todo)
#     #     db.session.commit()
#     #     # return jsonify({
#     #     #     'id': todo.id,
#     #     #     'description': todo.description
#     #     # })
#     #     body['description'] = todo.description
#     #     body['id'] = todo.id
#     # except:
#     #     error=True
#     #     db.session.rollback()
#     # finally:
#     #     db.session.close()
#     # if error:
#     #     abort (500)
#     # else:
#     #     return jsonify(body)
#     try:
#         description = request.get_json()['description']
#         todo = Todo(description=description, completed=False)
#         db.session.add(todo)
#         db.session.commit()
#         body['id'] = todo.id
#         body['completed'] = todo.completed
#         body['description'] = todo.description
#     except:
#         error = True
#         db.session.rollback()
#         print(sys.exc_info())
#     finally:
#         db.session.close()
#     if error:
#         abort (400)
#     else:
#         return jsonify(body)
#
# @app.route('/todos/<todo_id>/set-completed', methods=['POST'])
# def set_completed_todo(todo_id):
#     try:
#         completed = request.get_json()['completed']
#         print('completed', completed)
#         todo = Todo.query.get(todo_id)
#         todo.completed = completed
#         db.session.commit()
#     except:
#         db.session.rollback()
#     finally:
#         db.session.close()
#     return redirect(url_for('index'))
#
# @app.route('/todos/<todo_id>', methods=['DELETE'])
# def delete_todo(todo_id):
#     try:
#         Todo.query.filter_by(id=todo_id).delete()
#         db.session.commit()
#     except:
#         db.session.rollback()
#     finally:
#         db.session.close()
#     return jsonify({ 'success': True })
#
# @app.route('/lists/<list_id>')
# def get_list_todos(list_id):
#     return render_template('index.html',
#                            lists=TodoList.query.all(),
#                            active_list=TodoList.query.get(list_id),
#                            todos=Todo.query.filter_by(list_id=list_id).order_by('id').all()
#                            )
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref='list', lazy=True)

@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        list_id = request.get_json()['list_id']
        todo = Todo(description=description)
        active_list = TodoList.query.get(list_id)
        todo.list = active_list
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if not error:
        return jsonify(body)
    else:
        abort(500)

@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    try:
        Todo.query.filter_by(id=todo_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({ 'success': True })

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:
        completed = request.get_json()['completed']
        print('completed', completed)
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    # return render_template('index.html',
    #                        lists=TodoList.query.all(),
    #                        active_list=TodoList.query.get(list_id),
    #                        todos=Todo.query.filter_by(list_id=list_id).order_by('id').all()
    #                        )
    lists = TodoList.query.all()
    active_list = TodoList.query.get(list_id)
    todos = Todo.query.filter_by(list_id=list_id).order_by('id').all()

    return render_template('index.html', todos=todos, lists=lists, active_list=active_list)

@app.route('/lists/create', methods=['POST'])
def create_list():
    error = False
    body = {}
    try:
        name = request.get_json()['name']
        todolist = TodoList(name=name)
        db.session.add(todolist)
        db.session.commit()
        body['id'] = todolist.id
        body['name'] = todolist.name
    except():
        db.session.rollback()
        error = True
        print(sys.exc_info)
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify(body)

@app.route('/lists/<list_id>/delete', methods=['DELETE'])
def delete_list(list_id):
    error = False
    try:
        list = TodoList.query.get(list_id)
        for todo in list.todos:
            db.session.delete(todo)

        db.session.delete(list)
        db.session.commit()
    except():
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify({'success': True})


@app.route('/lists/<list_id>/set-completed', methods=['POST'])
def set_completed_list(list_id):
    error = False

    try:
        list = TodoList.query.get(list_id)

        for todo in list.todos:
            todo.completed = True

        db.session.commit()
    except:
        db.session.rollback()

        error = True
    finally:
        db.session.close()

    if error:
        abort(500)
    else:
        return '', 200
@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id=1))

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)

from flask import Flask, request, send_from_directory
from flask_restful import Resource, Api
from datetime import datetime
import logging
import os
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
api = Api(app)

"""set up rotating logger"""
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('todos.log')
file_handler.setFormatter(formatter)
rotate_handler = RotatingFileHandler(
    'todos.log', maxBytes=2000, backupCount=10
)

logger.addHandler(file_handler)
logger.addHandler(rotate_handler)

# dict containing all single todo dicts
TODOS = {}


class all_todos(Resource):
    """
    get/post to dict containing smaller dicts that contain single todos
    """

    def get(self):
        if len(TODOS) == 0:
            logger.debug("There are currently no todos")
            return "There are currently no todos"
        else:
            logger.info("todos GET request success")
            return TODOS

    def post(self):
        date = datetime.now()
        date_created = (str(date.month) + "/" + str(date.day) +
                        "/" + str(date.year))

        if len(TODOS) == 0:
            todo_id = "1"
        else:
            todo_id = str(int(max(TODOS.keys()).lstrip('todo')) + 1)

        try:
            TODOS[todo_id] = {'Title': request.form['Title'],
                              'Created on': date_created,
                              'Last Updated date': date_created,
                              'Due Date': request.form['Due'],
                              'Completed': request.form['Completed'],
                              'Completion Date': request.form['Completion Date']
                              }
            logger.info("todos POST request success")
            return TODOS
        except Exception as e:
            logger.error(e)


class Todo_item(Resource):
    """
    get/put(update)/delete a single todo item
    """

    def get(self, todo_id):
        try:
            logger.info("single todo GET success")
            return {todo_id: TODOS[todo_id]}
        except Exception as e:
            logger.error(e)
            return "single todo GET fail - no todo item with that id"

    def put(self, todo_id):
        try:
            date = datetime.now()
            update_date = (str(date.month) + "/" +
                           str(date.day) + "/" + str(date.year))

            TODOS[todo_id] = {'Title': request.form['Title'],
                              'Created on': TODOS[todo_id]['Created on'],
                              'Last Updated date': update_date,
                              'Due Date': request.form['Due'],
                              'Completed': request.form['Completed']
                              }

            if request.form['Completed'] == 'True':
                TODOS[todo_id]['Completion Date'] = update_date
            else:
                TODOS[todo_id]['Completion Date'] = 'Todo item is incomplete'

            logger.info("single todo PUT success - updated")
            return {todo_id: TODOS[todo_id]}
        except Exception as e:
            logger.error(e)

    def delete(self, todo_id):
        try:
            del TODOS[todo_id]
            logger.info("single todo DELETE success")
            return TODOS
        except Exception as e:
            logger.error(e)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico')


api.add_resource(all_todos, '/')
api.add_resource(Todo_item, '/<string:todo_id>')


if __name__ == '__main__':
    app.run(debug=True)

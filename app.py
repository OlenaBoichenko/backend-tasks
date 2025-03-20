import sys

from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# tasks - массив для хранения задач в памяти
# Каждая задача представлена полями: id, title, description, deadline
# Для уникальности задач идентификатор - next_id, который увеличивается на единицу при добавлении новой задачи

tasks = []
next_id = 1

def validate_deadline(deadline_str):
    #Проверка соответствия дедлайна формату 'DD-MM-YYYY'
    try:
        datetime.strptime(deadline_str, '%d-%m-%Y')
        return True
    except ValueError:
        return False
    
#Эндпоинт для добавления задачи
@app.route('/tasks', methods=['POST'])
def add_task():
    global next_id
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    deadline = data.get("deadline")
    if not title or not description or not deadline:
        return jsonify({"error": "Все поля (title, description, deadline) обязательны."}), 400
    if not validate_deadline(deadline):
        return jsonify({"error": "Дедлайн должен быть в формате DD-MM-YYYY."}), 400

    task = {
        "id": next_id,
        "title": title,
        "description": description,
        "deadline": deadline
    }
    tasks.append(task)
    next_id += 1
    return jsonify(task), 201

#Эндпоинт для получения всех задач
@app.route('/tasks', methods=['GET'])
def get_tasks():
    # Сортировка задач по дедлайну: ближайшие даты первыми
    sorted_tasks = sorted(tasks, key=lambda t: datetime.strptime(t["deadline"], '%d-%m-%Y'))
    return jsonify(sorted_tasks), 200

#Эндпоинт для удаления задачи
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(new_tasks) == len(tasks):
        return jsonify({"error": "Задача не найдена."}), 404
    tasks = new_tasks
    return jsonify({"message": f"Задача с ID {task_id} удалена."}), 200

if __name__ == '__main__':
    app.run(debug=True)

"""
Улучшение проекта для продакшена:
 1) заменила бы хранение данных в памяти на полноценную базу данных (например, MySQL) для обеспечения сохранности и масштабируемости данных. 
 2) добавила бы авторизацию пользователей с разными ролями.
 3) использовала бы миграции для управления схемой базы данных. 
 4) настроила бы централизованное логирование и обработку ошибок, чтобы легче было отслеживать и исправлять проблемы. 
 5) проект можно контейнеризировать и настроить CI/CD для автоматического развёртывания и масштабирования.
"""

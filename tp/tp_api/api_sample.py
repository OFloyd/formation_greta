# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from flask import Flask, jsonify, request

app = Flask(__name__)

# Définition de quelques données pour notre API
students = [
    {
        'id': 1,
        'name': 'Alice',
        'age': 20
    },
    {
        'id': 2,
        'name': 'Bob',
        'age': 22
    },
    {
        'id': 3,
        'name': 'Charlie',
        'age': 21
    }
]

# Route pour récupérer tous les étudiants
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students)

# Route pour récupérer un étudiant en particulier
@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    student = [student for student in students if student['id'] == id]
    return jsonify(student)

# Route pour créer un nouvel étudiant
@app.route('/students', methods=['POST'])
def create_student():
    student = {
        'id': request.json['id'],
        'name': request.json['name'],
        'age': request.json['age']
    }
    students.append(student)
    return jsonify(student)

# Route pour mettre à jour un étudiant existant
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    student = [student for student in students if student['id'] == id]
    student[0]['name'] = request.json.get('name', student[0]['name'])
    student[0]['age'] = request.json.get('age', student[0]['age'])
    return jsonify(student[0])

# Route pour supprimer un étudiant existant
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = [student for student in students if student['id'] == id]
    students.remove(student[0])
    return jsonify({'result': True})

# Lancement de l'application Flask
if __name__ == '__main__':
    app.run(debug=True)
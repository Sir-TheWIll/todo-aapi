from flask import Flask, request, jsonify, render_template
import json
import os
from datetime import datetime

app = Flask(__name__)

# File to store todos
TODOS_FILE = 'todos.json'

def load_todos():
    """Load todos from JSON file"""
    if os.path.exists(TODOS_FILE):
        with open(TODOS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_todos(todos):
    """Save todos to JSON file"""
    with open(TODOS_FILE, 'w') as f:
        json.dump(todos, f, indent=2)

@app.route('/')
def home():
    # Serve a web UI when the client accepts HTML, otherwise return JSON API info
    if request.accept_mimetypes.accept_html:
        return render_template('index.html')

    return jsonify({
        'message': 'Todo List API - Docker Project',
        'version': '1.0',
        'endpoints': {
            'GET /': 'API information',
            'GET /todos': 'Get all todos',
            'GET /todos/<id>': 'Get a specific todo',
            'POST /todos': 'Create a new todo',
            'PUT /todos/<id>': 'Update a todo',
            'DELETE /todos/<id>': 'Delete a todo',
            'GET /health': 'Health check'
        },
        'example': {
            'POST /todos': {
                'title': 'Learn Docker',
                'description': 'Complete Docker course',
                'completed': False
            }
        }
    })

@app.route('/health')
def health():
    todos = load_todos()
    return jsonify({
        'status': 'healthy',
        'service': 'todo-api',
        'total_todos': len(todos),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/todos', methods=['GET'])
def get_todos():
    """Get all todos"""
    todos = load_todos()
    return jsonify({
        'todos': todos,
        'count': len(todos)
    })

@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    """Get a specific todo by ID"""
    todos = load_todos()
    
    for todo in todos:
        if todo['id'] == todo_id:
            return jsonify(todo)
    
    return jsonify({'error': 'Todo not found'}), 404

@app.route('/todos', methods=['POST'])
def create_todo():
    """Create a new todo"""
    try:
        data = request.json
        
        if not data or 'title' not in data:
            return jsonify({'error': 'Title is required'}), 400
        
        todos = load_todos()
        
        # Generate new ID
        new_id = max([t['id'] for t in todos], default=0) + 1
        
        new_todo = {
            'id': new_id,
            'title': data['title'],
            'description': data.get('description', ''),
            'completed': data.get('completed', False),
            'created_at': datetime.now().isoformat()
        }
        
        todos.append(new_todo)
        save_todos(todos)
        
        return jsonify(new_todo), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """Update a todo"""
    try:
        data = request.json
        todos = load_todos()
        
        for i, todo in enumerate(todos):
            if todo['id'] == todo_id:
                if 'title' in data:
                    todos[i]['title'] = data['title']
                if 'description' in data:
                    todos[i]['description'] = data['description']
                if 'completed' in data:
                    todos[i]['completed'] = data['completed']
                
                todos[i]['updated_at'] = datetime.now().isoformat()
                save_todos(todos)
                return jsonify(todos[i])
        
        return jsonify({'error': 'Todo not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Delete a todo"""
    todos = load_todos()
    
    for i, todo in enumerate(todos):
        if todo['id'] == todo_id:
            deleted_todo = todos.pop(i)
            save_todos(todos)
            return jsonify({
                'message': 'Todo deleted successfully',
                'todo': deleted_todo
            })
    
    return jsonify({'error': 'Todo not found'}), 404

if __name__ == '__main__':
    import socket

    port = int(os.getenv('PORT', 5000))
    try:
        app.run(host='0.0.0.0', port=port, debug=True)
    except OSError as e:
        # Handle common 'address already in use' errors by falling back to a free port
        if getattr(e, 'errno', None) == 48 or 'Address already in use' in str(e):
            print(f"Port {port} already in use. Selecting an available port...")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('', 0))
            new_port = s.getsockname()[1]
            s.close()
            print(f"Retrying on port {new_port}")
            app.run(host='0.0.0.0', port=new_port, debug=True)
        else:
            raise
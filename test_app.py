import os
import tempfile

import pytest

import app as app_module
from app import app, init_db


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp(suffix='.db')

    app_module.DB_PATH = db_path
    app.config['TESTING'] = True

    init_db()

    with app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(db_path)


def test_get_todos_empty(client):
    response = client.get('/todos')
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_todo(client):
    response = client.post('/todos', json={
        'title': 'Test 1',
        'description': 'Description Test 1',
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['id'] == 1
    assert data['title'] == 'Test 1'
    assert data['description'] == 'Description Test 1'
    assert data['done'] is False


def test_create_todo_missing_title(client):
    response = client.post('/todos', json={'description': 'Test sans titre'})
    assert response.status_code == 400
    assert 'error' in response.get_json()


def test_get_todo_by_id(client):
    client.post('/todos', json={'title': 'Task 1'})
    response = client.get('/todos/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == 1
    assert data['title'] == 'Task 1'


def test_get_todo_not_found(client):
    response = client.get('/todos/9')
    assert response.status_code == 404
    assert 'error' in response.get_json()


def test_update_todo(client):
    client.post('/todos', json={'title': 'Task'})
    response = client.put('/todos/1', json={
        'title': 'Task updated',
        'description': 'updated description',
        'done': True
    })
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Todo updated'

    updated = client.get('/todos/1').get_json()
    assert updated['title'] == 'Task updated'
    assert updated['done'] is True


def test_update_todo_not_found(client):
    response = client.put('/todos/9', json={
        'title': 'Inexistant',
        'description': '',
        'done': False
    })
    assert response.status_code == 404
    assert 'error' in response.get_json()


def test_delete_todo(client):
    client.post('/todos', json={'title': 'Task to delete'})
    response = client.delete('/todos/1')
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Todo deleted'

    assert client.get('/todos/1').status_code == 404


def test_delete_todo_not_found(client):
    response = client.delete('/todos/9')
    assert response.status_code == 404
    assert 'error' in response.get_json()

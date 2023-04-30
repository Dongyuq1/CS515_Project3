import random
import string
from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)
posts = []
users = []

def generate_key(length=12):
    """Generate a unique key."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def get_post_by_id(id):
    """Return the post with the given ID, or None if not found."""
    for post in posts:
        if post['id'] == id:
            return post
    return None

def get_user_by_id(id):
    """Return the user with the given ID, or None if not found."""
    for user in users:
        if user['id'] == id:
            return user
    return None

def get_user_by_unique_key(unique_key):
    """Return the user with the given unique_key, or None if not found."""
    for user in users:
        if user['unique_key'] == unique_key:
            return user
    return None

@app.route('/user', methods=['POST'])
def create_user():
    """Create a new user with a unique ID, key, and unique_key."""
    if not request.is_json:
        return jsonify({'err': 'Request body must be JSON'}), 400

    unique_key = request.json.get('unique_key')
    if not unique_key or not isinstance(unique_key, str) or get_user_by_unique_key(unique_key):
        return jsonify({'err': 'Request body must contain a unique "unique_key" field with a string value'}), 400

    non_unique_key = request.json.get('non_unique_key', '')

    id = len(users) + 1
    while get_user_by_id(id):
        id += 1

    key = generate_key()
    user = {'id': id, 'key': key, 'unique_key': unique_key, 'non_unique_key': non_unique_key}
    users.append(user)

    return jsonify({'id': id, 'key': key, 'unique_key': unique_key, 'non_unique_key': non_unique_key}), 201

@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    """Retrieve the user with the given ID."""
    user = get_user_by_id(id)
    if not user:
        return jsonify({'err': 'User not found'}), 404

    return jsonify({'id': user['id'], 'unique_key': user['unique_key'], 'non_unique_key': user['non_unique_key']}), 200

@app.route('/user/<int:id>/edit', methods=['POST'])
def edit_user(id):
    """Edit the user with the given ID."""
    user = get_user_by_id(id)
    if not user:
        return jsonify({'err': 'User not found'}), 404

    if not request.is_json:
        return jsonify({'err': 'Request body must be JSON'}), 400

    user_key = request.json.get('key')
    if not user_key or user_key != user['key']:
        return jsonify({'err': 'Forbidden'}), 403

    non_unique_key = request.json.get('non_unique_key')
    if non_unique_key:
        user['non_unique_key'] = non_unique_key

    return jsonify({'id': user['id'], 'unique_key': user['unique_key'], 'non_unique_key': user['non_unique_key']}), 200

@app.route('/post', methods=['POST'])
def create_post():
    """Create a new post with a unique ID, key, and timestamp."""
    if not request.is_json:
        return jsonify({'err': 'Request body must be JSON'}), 400

    msg = request.json.get('msg')
    if not msg or not isinstance(msg, str):
        return jsonify({'err': 'Request body must contain a "msg" field with a string value'}), 400

    user_id = request.json.get('user_id')
    user_key = request.json.get('user_key')
    user = None
    if user_id:
        user = get_user_by_id(user_id)
        if not user or user['key'] != user_key:
            return jsonify({'err': 'Invalid user credentials'}), 403

    id = len(posts) + 1
    while get_post_by_id(id):
        id += 1

    key = generate_key()
    timestamp = datetime.utcnow().isoformat()
    reply_to = request.json.get('reply_to', None)

    post = {'id': id, 'key': key, 'timestamp': timestamp, 'msg': msg, 'user_id': user_id, 'reply_to': reply_to}
    posts.append(post)

    return jsonify({'id': id, 'key': key, 'timestamp': timestamp, 'user_id': user_id, 'reply_to': reply_to}), 201


@app.route('/post/<int:id>', methods=['GET'])
def read_post(id):
    """Retrieve the post with the given ID."""
    post = get_post_by_id(id)
    if not post:
        return jsonify({'err': 'Post not found'}), 404

    user_id = post.get('user_id')
    user = get_user_by_id(user_id) if user_id else None
    user_unique_key = user['unique_key'] if user else None

    return jsonify(
        {'id': post['id'], 'timestamp': post['timestamp'], 'msg': post['msg'], 'user_unique_key': user_unique_key,
         'reply_to': post['reply_to']}), 200


@app.route('/post/<int:id>/delete', methods=['POST'])
def delete_post(id):
    """Delete the post with the given ID."""
    post = get_post_by_id(id)
    if not post:
        return jsonify({'err': 'Post not found'}), 404

    if not request.is_json:
        return jsonify({'err': 'Request body must be JSON'}), 400

    key = request.json.get('key')
    if post['key'] != key:
        user_id = request.json.get('user_id')
        user_key = request.json.get('user_key')
        user = get_user_by_id(user_id) if user_id else None
        if not user or user['key'] != user_key or user['id'] != post['user_id']:
            return jsonify({'err': 'Forbidden'}), 403

    posts.remove(post)

    return jsonify({'id': post['id'], 'key': post['key'], 'timestamp': post['timestamp']}), 200


if __name__ == '__main__':
    app.run(debug=True)


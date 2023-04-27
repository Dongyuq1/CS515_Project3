from flask import Flask, jsonify, request
import random
import string
from datetime import datetime

app = Flask(__name__)
posts = []

def generate_key(length=12):
    """Generate a unique key for the post."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def get_post_by_id(id):
    """Return the post with the given ID, or None if not found."""
    for post in posts:
        if post['id'] == id:
            return post
    return None

@app.route('/post', methods=['POST'])
def create_post():
    """Create a new post with a unique ID, key, and timestamp."""
    if not request.is_json:
        return jsonify({'err': 'Request body must be JSON'}), 400

    msg = request.json.get('msg')
    if not msg or not isinstance(msg, str):
        return jsonify({'err': 'Request body must contain a "msg" field with a string value'}), 400

    id = len(posts) + 1
    while get_post_by_id(id):
        id += 1

    key = generate_key()
    timestamp = datetime.utcnow().isoformat()

    post = {'id': id, 'key': key, 'timestamp': timestamp, 'msg': msg}
    posts.append(post)

    return jsonify({'id': id, 'key': key, 'timestamp': timestamp}), 201

@app.route('/post/<int:id>', methods=['GET'])
def read_post(id):
    """Retrieve the post with the given ID."""
    post = get_post_by_id(id)
    if not post:
        return jsonify({'err': 'Post not found'}), 404

    return jsonify({'id': post['id'], 'timestamp': post['timestamp'], 'msg': post['msg']}), 200

@app.route('/post/<int:id>/delete/<string:key>', methods=['DELETE'])
def delete_post(id, key):
    """Delete the post with the given ID and key."""
    post = get_post_by_id(id)
    if not post:
        return jsonify({'err': 'Post not found'}), 404

    if post['key'] != key:
        return jsonify({'err': 'Forbidden'}), 403

    posts.remove(post)

    return jsonify({'id': post['id'], 'key': post['key'], 'timestamp': post['timestamp']}), 200

if __name__ == '__main__':
    app.run(debug=True)

import random
import string
from datetime import datetime
from threading import Lock
from flask import Flask, jsonify, request

app = Flask(__name__)
posts = []
lock = Lock()



def generate_key(length=12):
    """Generate a unique key for the post."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))


def find_post_by_id(post_id):
    """Return the post with the given ID, or None if not found."""
<<<<<<<<< Temporary merge branch 1
    for post in posts:
        if post['id'] == post_id:
            return post
    return None
=========
    with lock:
        for post in posts:
            if post['id'] == post_id:
                return post
        return None

>>>>>>>>> Temporary merge branch 2


@app.route('/post', methods=['POST'])
def create_post():
    """Create a new post with a unique ID, key, and timestamp."""
    if not request.is_json:
        return jsonify({'err': 'Request body must be JSON'}), 400

    message = request.json.get('msg')
    if not message or not isinstance(message, str):
        return jsonify({'err': 'Request body must contain a "msg" field with a string value'}), 400

<<<<<<<<< Temporary merge branch 1
    post_id = len(posts) + 1
    while find_post_by_id(post_id):
        post_id += 1
=========
    with lock:
        post_id = len(posts) + 1
        while find_post_by_id(post_id):
            post_id += 1
>>>>>>>>> Temporary merge branch 2

        key = generate_key()
        timestamp = datetime.utcnow().isoformat()

<<<<<<<<< Temporary merge branch 1
    post = {'id': post_id, 'key': key, 'timestamp': timestamp, 'msg': message}
    posts.append(post)
=========
        post = {'id': post_id, 'key': key, 'timestamp': timestamp, 'msg': message}
        posts.append(post)
>>>>>>>>> Temporary merge branch 2

    return jsonify({'id': post_id, 'key': key, 'timestamp': timestamp}), 201


@app.route('/post/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Retrieve the post with the given ID."""
    post = find_post_by_id(post_id)
    if not post:
        return jsonify({'err': 'Post not found'}), 404

    return jsonify({'id': post['id'], 'timestamp': post['timestamp'], 'msg': post['msg']}), 200


@app.route('/post/<int:post_id>/delete/<string:key>', methods=['DELETE'])
def delete_post(post_id, key):
    """Delete the post with the given ID and key."""
<<<<<<<<< Temporary merge branch 1
    post = find_post_by_id(post_id)
    if not post:
        return jsonify({'err': 'Post not found'}), 404
=========
    with lock:
        post = find_post_by_id(post_id)
        if not post:
            return jsonify({'err': 'Post not found'}), 404
>>>>>>>>> Temporary merge branch 2

        if post['key'] != key:
            return jsonify({'err': 'Forbidden'}), 403

        posts.remove(post)

    return jsonify({'id': post['id'], 'key': post['key'], 'timestamp': post['timestamp']}), 200


if __name__ == '__main__':
    app.run(debug=True)
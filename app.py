import random
import string
from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)
posts = []
users = []


def generate_key(length=12):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))


def find_post_by_id(post_id):
    for post in posts:
        if post['id'] == post_id:
            return post
    return None


def find_user_by_id(user_id):
    for user in users:
        if user['id'] == user_id:
            return user
    return None


def create_user(username, real_name=None, avatar=None):
    user_key = generate_key()
    user_id = len(users) + 1
    user = {'id': user_id, 'username': username, 'key': user_key, 'real_name': real_name, 'avatar': avatar}
    users.append(user)
    return user


@app.route('/user', methods=['POST'])
def create_user_route():
    if not request.is_json:
        return jsonify({'err': 'Request body must be JSON'}), 400

    username = request.json.get('username')
    if not username or not isinstance(username, str):
        return jsonify({'err': 'Request body must contain a "username" field with a string value'}), 400

    user = create_user(username)
    return jsonify({'id': user['id'], 'username': user['username'], 'key': user['key']}), 201


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = find_user_by_id(user_id)
    if not user:
        return jsonify({'err': 'User not found'}), 404

    return jsonify({'id': user['id'], 'username': user['username'], 'real_name': user['real_name'], 'avatar': user['avatar']}), 200


@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if not request.is_json:
        return jsonify({'err': 'Request body must be JSON'}), 400

    user = find_user_by_id(user_id)
    if not user:
        return jsonify({'err': 'User not found'}), 404

    user_key = request.json.get('key')
    if user['key'] != user_key:
        return jsonify({'err': 'Forbidden'}), 403

    real_name = request.json.get('real_name')
    avatar = request.json.get('avatar')

    if real_name:
        user['real_name'] = real_name
    if avatar:
        user['avatar'] = avatar

    return jsonify({'id': user['id'], 'username': user['username'], 'real_name': user['real_name'], 'avatar': user['avatar']}), 200


@app.route('/post', methods=['POST'])
def create_post():
    if not request.is_json:
        return jsonify({'err': 'Request body must be JSON'}), 400

    message = request.json.get('msg')
    if not message or not isinstance(message, str):
        return jsonify({'err': 'Request body must contain a "msg" field with a string value'}), 400

    user_id = request.json.get('user_id')
    user_key = request.json.get('user_key')
    if user_id and user_key:
        user = find_user_by_id(user_id)
        if not user or user['key'] != user_key:
            return jsonify({'err': 'Invalid user ID or key'}), 400

        parent_id = request.json.get('parent_id')
        if parent_id:
            parent_post = find_post_by_id(parent_id)
            if not parent_post:
                return jsonify({'err': 'Parent post not found'}), 400

        post_id = len(posts) + 1
        while find_post_by_id(post_id):
            post_id += 1

        key = generate_key()
        timestamp = datetime.utcnow().isoformat()

        post = {'id': post_id, 'key': key, 'timestamp': timestamp, 'msg': message, 'user_id': user_id,
                'parent_id': parent_id}
        posts.append(post)

        return jsonify({'id': post_id, 'key': key, 'timestamp': timestamp}), 201

    @app.route('/post/<int:post_id>', methods=['GET'])
    def get_post(post_id):
        post = find_post_by_id(post_id)
        if not post:
            return jsonify({'err': 'Post not found'}), 404

        children = [child_post['id'] for child_post in posts if child_post.get('parent_id') == post_id]

        return jsonify(
            {'id': post['id'], 'timestamp': post['timestamp'], 'msg': post['msg'], 'parent_id': post.get('parent_id'),
             'children': children}), 200

    @app.route('/post/<int:post_id>/delete/<string:key>', methods=['DELETE'])
    def delete_post(post_id, key):
        post = find_post_by_id(post_id)
        if not post:
            return jsonify({'err': 'Post not found'}), 404

        if post['key'] != key:
            user = find_user_by_id(post.get('user_id'))
            if not user or user['key'] != key:
                return jsonify({'err': 'Forbidden'}), 403

        posts.remove(post)

        return jsonify({'id': post['id'], 'key': post['key'], 'timestamp': post['timestamp']}), 200

    @app.route('/posts', methods=['GET'])
    def get_posts_in_range():
        start_date_str = request.args.get('start')
        end_date_str = request.args.get('end')

        if start_date_str:
            start_date = datetime.fromisoformat(start_date_str)
        else:
            start_date = None

        if end_date_str:
            end_date = datetime.fromisoformat(end_date_str)
        else:
            end_date = None

        filtered_posts = []
        for post in posts:
            post_date = datetime.fromisoformat(post['timestamp'])
            if (not start_date or post_date >= start_date) and (not end_date or post_date <= end_date):
                filtered_posts.append(post)

        return jsonify(filtered_posts), 200

    @app.route('/user/<int:user_id>/posts', methods=['GET'])
    def get_posts_by_user(user_id):
        if not find_user_by_id(user_id):
            return jsonify({'err': 'User not found'}), 404

        filtered_posts = [post for post in posts if post.get('user_id') == user_id]

        return jsonify(filtered_posts), 200

    if __name__ == '__main__':
        app.run(debug=True)


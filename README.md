## Names and Stevens Login
Yuqi Dong ydong28@stevens.edu
Jia Gao jgao32@stevens.edu
Chih-Chao Wang cwang126@stevens.edu

## Github Repo
[Repo](https://github.com/Dongyuq1/CS515_Project3)

## Estimate of hours
Around 3 days were spent on this project.
## How we tested our code
Initially, We started with curl testing and developing. such as,


`Create user (/user POST)`


curl -X POST -H "Content-Type: application/json" -d '{"username": "testuser"}' http://127.0.0.1:5000/user


`Get user (/user/<user_id> GET)`


curl http://127.0.0.1:5000/user/1


`Update user (/user/<user_id> PUT)`


curl -X PUT -H "Content-Type: application/json" -d '{"key": "<user_key>", "real_name": "Tom", "avatar": "https://stevens.com/avatar.jpg' http://127.0.0.1:5000/user/1


`Create post (/post POST)`


curl -X POST -H "Content-Type: application/json" -d '{"msg": "Hello world!", "user_id": 1, "user_key": "<user_key>"}' http://127.0.0.1:5000/post


`Get post (/post/<post_id> GET)`


curl http://127.0.0.1:5000/post/1


`Delete post (/post/<post_id>/delete/<key> DELETE)`


curl -X DELETE http://127.0.0.1:5000/post/1/delete/<post_key>


`Get posts in range (/posts GET)`


curl 'http://127.0.0.1:5000/posts?start=2023-05-01T00:00:00&end=2023-05-01T23:59:59'


`Get posts by user (/user/<user_id>/posts GET)`


curl http://127.0.0.1:5000/user/1/posts


Then we tried to use Postman to test out API.
## Bugs and Issues that could not be resolved
No

## An example of difficult issue how I resolved
In our threading reply extension, we always encountered deadlocks, causing us to spend a considerable amount of time addressing the issue. However, through collaboration and research, we were able to overcome the problem and find a solution.
## Extensions
- User and user keys
- User Profiels(needs user)
- Threaded replies
- Date- and time-based range queries
- User-based range queries (needs user)

### User and user keys
#### Create a user
- Path: /user [**POST**]
- Request:
``` Json
{
    "username": "{{user_1}}"
}
```
- Response:
``` Json
{
    "id": 1,
    "key": "9GAg8FWxHwx5",
    "username": "testuser1"
}
```
### User Profiels(needs user)
#### Find User
- Path: /user/{{user_id1}} [**GET**]
- Response:
``` Json
{
    "avatar": null,
    "id": 1,
    "real_name": null,
    "username": "testuser1"
}
```
### Threaded replies
- Path: /post [**POST**]
- Request:
``` Json
{
    "user_id": {{user_id2}},
    "user_key": "{{user_key2}}",
    "msg": "This is a reply by user 2",
    "parent_id": {{post_id1}}
}

{
    "id": 4,
    "key": "MUS9KBfkwTUD",
    "timestamp": "2023-05-02T02:25:15.527251"
}
```

- Path: /post/{{post_id1}} [**GET**]
- Request:
``` Json
{
    "children": [
        4,
    ],
    "id": 1,
    "msg": "This is a post!",
    "parent_id": null,
    "timestamp": "2023-05-02T02:22:36.543712"
}
```

### Date- and time-based range queries
- Path: /posts?start={{post_timestamp1}}&end={{post_timestamp_copy7}} [**GET**]
- Query Parameters: start, end
- Response:
``` Json
[
    {
        "children": [
            3,
            4
        ],
        "id": 1,
        "key": "W39Izr6CtUTB",
        "msg": "This is a post!",
        "parent_id": null,
        "timestamp": "2023-05-02T02:22:36.543712",
        "user_id": 1
    },
    {
        "children": [],
        "id": 3,
        "key": "fOQzv7pLD4GP",
        "msg": "This is a reply by user 2",
        "parent_id": 1,
        "timestamp": "2023-05-02T02:23:38.798414",
        "user_id": 2
    },
    {
        "children": [],
        "id": 4,
        "key": "MUS9KBfkwTUD",
        "msg": "This is a reply by user 2",
        "parent_id": 1,
        "timestamp": "2023-05-02T02:25:15.527251",
        "user_id": 2
    },
    {
        "children": [],
        "id": 5,
        "key": "Ap0qBso5Xb7i",
        "msg": "This is a post!",
        "parent_id": null,
        "timestamp": "2023-05-02T02:34:53.987937",
        "user_id": 1
    },
    {
        "children": [],
        "id": 6,
        "key": "F2O3Km5GIYJt",
        "msg": "This is a post!",
        "parent_id": null,
        "timestamp": "2023-05-02T02:34:56.222056",
        "user_id": 1
    },
    {
        "children": [],
        "id": 7,
        "key": "QKS3HyHIndNC",
        "msg": "This is a post!",
        "parent_id": null,
        "timestamp": "2023-05-02T02:34:58.502899",
        "user_id": 1
    },
    {
        "children": [],
        "id": 8,
        "key": "8LRb2VvOeTFb",
        "msg": "This is a post!",
        "parent_id": null,
        "timestamp": "2023-05-02T02:35:00.439270",
        "user_id": 1
    },
    {
        "children": [],
        "id": 9,
        "key": "y9G4JHJBO3lU",
        "msg": "This is a post!",
        "parent_id": null,
        "timestamp": "2023-05-02T02:35:02.720217",
        "user_id": 1
    },
    {
        "children": [],
        "id": 10,
        "key": "erf1oTSiELv5",
        "msg": "This is a post!",
        "parent_id": null,
        "timestamp": "2023-05-02T02:35:05.732301",
        "user_id": 1
    },
    {
        "children": [],
        "id": 11,
        "key": "Ntju4keTFXXI",
        "msg": "This is a post!",
        "parent_id": null,
        "timestamp": "2023-05-02T02:35:08.237389",
        "user_id": 1
    }
]
``` 

### User-based range queries (needs user)
- Path: /user/{{user_id1}}/posts [**GET**]
- Response:
``` Json
[
    {
        "children": [
            3,
            4
        ],
        "id": 1,
        "key": "W39Izr6CtUTB",
        "msg": "This is a post!",
        "parent_id": null,
        "timestamp": "2023-05-02T02:22:36.543712",
        "user_id": 1
    },
    {
        "children": [],
        "id": 5,
        "key": "Ap0qBso5Xb7i",
        "msg": "This is a post!",
        "parent_id": null,
        "timestamp": "2023-05-02T02:34:53.987937",
        "user_id": 1
    },
    {
        "children": [],
        "id": 6,
        "key": "F2O3Km5GIYJt",
        "msg": "This is a post!",
        "parent_id": null,
        "timestamp": "2023-05-02T02:34:56.222056",
        "user_id": 1
    },
    {
        "children": [],
        "id": 7,
        "key": "QKS3HyHIndNC",
        "msg": "This is a post!",
        "parent_id": null,
        "timestamp": "2023-05-02T02:34:58.502899",
        "user_id": 1
    },
    {
        "children": [],
        "id": 8,
        "key": "8LRb2VvOeTFb",
        "msg": "This is a post!",
        "parent_id": null,
        "timestamp": "2023-05-02T02:35:00.439270",
        "user_id": 1
    },
    {
        "children": [],
        "id": 9,
        "key": "y9G4JHJBO3lU",
        "msg": "This is a post!",
        "parent_id": null,
        "timestamp": "2023-05-02T02:35:02.720217",
        "user_id": 1
    },
    {
        "children": [],
        "id": 10,
        "key": "erf1oTSiELv5",
        "msg": "This is a post!",
        "parent_id": null,
        "timestamp": "2023-05-02T02:35:05.732301",
        "user_id": 1
    },
    {
        "children": [],
        "id": 11,
        "key": "Ntju4keTFXXI",
        "msg": "This is a post!",
        "parent_id": null,
        "timestamp": "2023-05-02T02:35:08.237389",
        "user_id": 1
    }
]
```

To test our endpoints, we write the following tests:
`POST` /user/ User 1 Creation

`GET` /user/{{user_id1}} Get User 1 Metadata

`PUT` /user/{{user_id1}} Edit User 1 Metadata

`GET` /user/{{user_id1}} Get User 1 Metadata again

`POST` /post Create a Post by User 1

`GET` /post/{{post_id1}} Read the Post by User 1

`POST` /user/ User 2 Creation

`GET` /user/{{user_id2}} Get User 2 Metadata

`PUT` /user/{{user_id2}} Edit User 2 Metadata

`GET` /user/{{user_id2}} Get User 2 Metadata again

`POST` /post Create Post 2 by User 2

`GET` /post/{{post_id2}} Read the Post 2

`POST` /post Create Reply by User 2

`GET` /post/{{reply_id}} Read the reply

`GET` /post/{{reply_id}} Read the Reply blow Post 1 by user 2

`GET` /posts/search?start_date={{post_timestamp1}}&end_date={{post_timestamp1}} Search Posts by date and time

`GET` /posts/user/{{user_id1}} Search Posts by User

`DEL` /post/{{post_id2}}/delete/{{post_key2}} Delete Post 2

To run these tests above, run ./test.sh or sudo ./test.sh.
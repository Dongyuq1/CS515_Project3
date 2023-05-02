## Names and Stevens Login
Yuqi Dong
Jia Gao
Chih-Chao Wang cwang126@stevens.edu

## Github Repo
[Repo](https://github.com/Dongyuq1/CS515_Project3)

## Estimate of hours
Around 3 days were spent on this project.
## How we tested our code
Initially, we use the curl to test out API as following command.
`curl -X POST -H "Content-Type: application/json" -d '{"username": "johndoe"}' <your_api_url>/user`
We just started to use Postman to test out API maulally after lecture. According to the requirements, we started to learn how to write some test code in Postman for convenience.
## Bugs and Issues that could not be resolved
No

## An example of difficult issue how I resolved

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
  "username": "David",
}
```
- Response:
``` Json
{
  "id": "123",
  "username": "David",
  "key": "randomKey"
}
```
### User Profiels(needs user)
#### Find User
- Path: /user/:userId [**GET**]
- Response:
``` Json
{
  "id": "123",
  "username": "David",
  "real_name": "None",
  "avatar": "None"
}
```
### Threaded replies

### Date- and time-based range queries
- Path: /posts [**GET**]
- Query Parameters: start, end
`/posts?start=2023-05-01T00:00:00&end=2023-05-31T23:59:59`
- Response: lists of posts that match the give timestamp

### User-based range queries (needs user)
- Path: /user/:user_id/posts [**GET**]
- Response: lists of posts that match the given userId


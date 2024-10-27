# TinyGallery Backend API Reference

This document provides a comprehensive guide to the TinyGallery Backend API endpoints.

## Base URL

All API requests should be made to: `http://your-domain.com/api/v1`

## Authentication

Most endpoints require authentication using a bearer token. Include the token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

### Get Access Token

```
POST /user/token
```

Authenticate a user and receive an access token.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Possible Errors:**
- 401 Unauthorized: Incorrect username or password
- 422 Unprocessable Entity: Invalid input data

## User Management

### Register User

```
POST /user/register
```

Register a new user.

**Request Body:**
```json
{
  "user_name": "string",
  "password": "string",
  "email": "string"
}
```

**Response:**
```json
{
  "status": "success",
  "user_id": "uuid-string"
}
```

**Possible Errors:**
- 400 Bad Request: Username already exists
- 422 Unprocessable Entity: Invalid input data

### Change Password

```
POST /userdata/change-password
```

Change the password for the authenticated user.

**Headers:**
- Authorization: Bearer <your_access_token>

**Request Body:**
```json
{
  "previous_password": "string",
  "new_password": "string",
  "confirm_password": "string"
}
```

**Response:**
```json
{
  "detail": "Password updated successfully"
}
```

**Possible Errors:**
- 400 Bad Request: New password and confirmation do not match
- 401 Unauthorized: Invalid token or previous password incorrect

## Posts

### Create Post

```
POST /posts/create
```

Create a new post.

**Headers:**
- Authorization: Bearer <your_access_token>
- Content-Type: multipart/form-data

**Request Body:**
- `is_nsfw`: "true" or "false" (Form data)
- `uploaded_file`: List of image files (Form data)
- `cover`: Cover image file (optional, Form data)
- `post_title`: Title of the post (Form data)
- `description`: Description of the post (Form data)

**Response:**
```json
{
  "status": "success",
  "post_id": "uuid-string"
}
```

**Possible Errors:**
- 400 Bad Request: Invalid file type or missing required fields
- 401 Unauthorized: Invalid token

### Update Post

```
PUT /posts/update/{post_uuid_for_update}
```

Update an existing post.

**Headers:**
- Authorization: Bearer <your_access_token>
- Content-Type: multipart/form-data

**Path Parameters:**
- `post_uuid_for_update`: UUID of the post to update

**Request Body:**
- Similar to create post, with additional `supplementary_mode` (Form data)

**Response:**
```json
{
  "status": "success",
  "updated_fields": ["title", "description"]
}
```

**Possible Errors:**
- 400 Bad Request: Invalid file type or missing required fields
- 401 Unauthorized: Invalid token or user doesn't own the post
- 404 Not Found: Post not found

### Delete Post

```
DELETE /posts/remove/{post_uuid_for_remove}
```

Delete a post.

**Headers:**
- Authorization: Bearer <your_access_token>

**Path Parameters:**
- `post_uuid_for_remove`: UUID of the post to delete

**Response:**
```json
{
  "status": "success",
  "deleted_post_id": "uuid-string"
}
```

**Possible Errors:**
- 401 Unauthorized: Invalid token or user doesn't own the post
- 404 Not Found: Post not found

### Get Posts

```
GET /resources/posts/{page}
```

Get a list of posts.

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Number of posts per page (default: 20, max: 100)

**Response:**
```json
{
  "total": 100,
  "page": 1,
  "limit": 20,
  "posts": [
    {
      "id": 1,
      "description": "A beautiful sunset",
      "share_num": 5,
      "post_uuid": "uuid-string",
      "nsfw": false,
      "user_name": "john_doe",
      "post_title": "Evening Sky",
      "dots": 42,
      "date": "2023-06-15T18:30:00Z",
      "cover_url": "http://example.com/images/cover1.jpg",
      "avatar": "http://example.com/avatars/john_doe.jpg"
    },
    // ... more posts
  ]
}
```

**Possible Errors:**
- 400 Bad Request: Invalid page number

### Get Single Post

```
GET /resources/posts/single/{post_uuid}
```

Get details of a single post.

**Path Parameters:**
- `post_uuid`: UUID of the post

**Response:**
```json
{
  "id": 1,
  "description": "A beautiful sunset",
  "share_num": 5,
  "post_uuid": "uuid-string",
  "nsfw": false,
  "user_name": "john_doe",
  "post_title": "Evening Sky",
  "dots": 42,
  "date": "2023-06-15T18:30:00Z",
  "files_url": {
    "image_files_url": [
      "http://example.com/images/sunset1.jpg",
      "http://example.com/images/sunset2.jpg"
    ],
    "original_cover_url": "http://example.com/images/cover_original.jpg",
    "compressed_cover_url": "http://example.com/images/cover_compressed.jpg"
  }
}
```

**Possible Errors:**
- 404 Not Found: Post not found

## Comments

### Create Comment

```
POST /remark/create/inpost
```

Create a new comment on a post.

**Headers:**
- Authorization: Bearer <your_access_token>

**Request Body:**
```json
{
  "post_uuid": "uuid-string",
  "content": "This is a great post!"
}
```

**Response:**
```json
{
  "status": "success",
  "comment_id": "uuid-string"
}
```

**Possible Errors:**
- 400 Bad Request: Missing required fields
- 401 Unauthorized: Invalid token
- 404 Not Found: Post not found

### Get Comments

```
GET /remark/get/inpost/{post_uuid_for_get_remark}/{page}
```

Get comments for a post.

**Path Parameters:**
- `post_uuid_for_get_remark`: UUID of the post
- `page`: Page number

**Query Parameters:**
- `limit`: Number of comments per page (default: 20, max: 100)

**Response:**
```json
{
  "total": 50,
  "page": 1,
  "limit": 20,
  "comments": [
    {
      "id": 1,
      "post_uuid": "uuid-string",
      "user_uuid": "user-uuid-string",
      "user_name": "jane_doe",
      "remark_uuid": "comment-uuid-string",
      "content": "This is a great post!",
      "date": "2023-06-15T19:00:00Z",
      "avatar": "http://example.com/avatars/jane_doe.jpg"
    },
    // ... more comments
  ]
}
```

**Possible Errors:**
- 400 Bad Request: Invalid page number
- 404 Not Found: Post not found

## Likes

### Get Like Status

```
GET /likes/get/like_status
```

Get the like status of a post for the authenticated user.

**Headers:**
- Authorization: Bearer <your_access_token>

**Query Parameters:**
- `post_uuid`: UUID of the post

**Response:**
```json
{
  "id": 1,
  "post_uuid": "uuid-string",
  "user_name": "john_doe",
  "user_uuid": "user-uuid-string",
  "liked": true,
  "date": "2023-06-15T20:00:00Z"
}
```

**Possible Errors:**
- 401 Unauthorized: Invalid token
- 404 Not Found: Post not found or user hasn't interacted with the post

### Like/Unlike Post

```
POST /likes/send/like
```

Like or unlike a post.

**Headers:**
- Authorization: Bearer <your_access_token>

**Query Parameters:**
- `post_uuid`: UUID of the post

**Response:**
```json
{
  "status": "success",
  "action": "liked",  // or "unliked"
  "current_likes": 43
}
```

**Possible Errors:**
- 401 Unauthorized: Invalid token
- 404 Not Found: Post not found

## User Data

### Get User Avatar

```
GET /resources/avatar/{user_name_for_get_avatar}
```

Get the avatar URLs for a user.

**Path Parameters:**
- `user_name_for_get_avatar`: Username

**Response:**
```json
{
  "status": "success",
  "avatar_200px": "http://example.com/avatars/john_doe_200.jpg",
  "avatar_40px": "http://example.com/avatars/john_doe_40.jpg",
  "full_image": "http://example.com/avatars/john_doe_full.jpg"
}
```

**Possible Errors:**
- 404 Not Found: User not found

### Set User Avatar

```
PUT /userdata/set/avatar
```

Set a new avatar for the authenticated user.

**Headers:**
- Authorization: Bearer <your_access_token>
- Content-Type: multipart/form-data

**Request Body:**
- `avatar`: Image file (Form data)

**Response:**
```json
{
  "status": "success",
  "avatar_url": "http://example.com/avatars/john_doe_new.jpg"
}
```

**Possible Errors:**
- 400 Bad Request: Invalid file type
- 401 Unauthorized: Invalid token

## Admin Endpoints

The following endpoints are only accessible to admin users. All admin endpoints require the Authorization header with a valid admin token.

### Get All Users

```
GET /admin/users
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Users per page (default: 20, max: 100)

**Response:**
```json
{
  "total": 1000,
  "page": 1,
  "limit": 20,
  "users": [
    {
      "id": 1,
      "user_name": "john_doe",
      "email": "john@example.com",
      "date_joined": "2023-01-01T00:00:00Z",
      "last_login": "2023-06-15T21:00:00Z",
      "is_active": true
    },
    // ... more users
  ]
}
```

### Create User (Admin)

```
POST /admin/users
```

**Request Body:**
```json
{
  "user_name": "new_user",
  "email": "newuser@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "status": "success",
  "user_id": "uuid-string"
}
```

### Update User (Admin)

```
PUT /admin/users/{user_uuid}
```

**Path Parameters:**
- `user_uuid`: UUID of the user to update

**Request Body:**
```json
{
  "email": "newemail@example.com",
  "is_active": false
}
```

**Response:**
```json
{
  "status": "success",
  "updated_fields": ["email", "is_active"]
}
```

### Delete User (Admin)

```
DELETE /admin/users/{user_uuid}
```

**Path Parameters:**
- `user_uuid`: UUID of the user to delete

**Response:**
```json
{
  "status": "success",
  "deleted_user_id": "uuid-string"
}
```

### Get All Posts (Admin)

```
GET /admin/posts
```

Similar structure to the non-admin get posts endpoint, but includes all posts regardless of user.

### Create Post (Admin)

```
POST /admin/posts
```

Similar structure to the non-admin create post endpoint, but allows specifying the user.

### Update Post (Admin)

```
PUT /admin/posts/{post_uuid}
```

Similar structure to the non-admin update post endpoint, but can update any post.

### Delete Post (Admin)

```
DELETE /admin/posts/{post_uuid}
```

Similar structure to the non-admin delete post endpoint, but can delete any post.

### Get All Comments (Admin)

```
GET /admin/comments
```

Get all comments across all posts.

### Create Comment (Admin)

```
POST /admin/comments
```

Create a comment on behalf of any user.

### Update Comment (Admin)

```
PUT /admin/comments/{comment_uuid}
```

Update any comment in the system.

### Delete Comment (Admin)

```
DELETE /admin/comments/{comment_uuid}
```

Delete any comment in the system.

Note: All admin endpoints may return a 403 Forbidden error if the authenticated user is not an admin.

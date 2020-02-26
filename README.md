# BrightBulb
A note taking application backend written in django using django-rest-framework.

### How to access

- Get auth token: **POST** <br/>
  https://treetrails.herokuapp.com/brightbulb/auth/
  ```
  {
    'username':'',
    'password':'',
  }
  ```

- Get all users: **GET** <br/>
  https://treetrails.herokuapp.com/brightbulb/users/
  ```
  {}
  ```

- Add new user: **POST** <br/>
  https://treetrails.herokuapp.com/brightbulb/users/
  ```
  {
    'username':'',
    'password':'',
    'email':'',
  }
  ```

- Get a user: **GET** <br/>
  https://treetrails.herokuapp.com/brightbulb/users/`username`
  ```
  {}
  ```

- Update a user: **PUT** <br/>
  https://treetrails.herokuapp.com/brightbulb/users/`username`
  ```
  {
    'username':'',
    'password':'',
    'email':'',
  }
  ```

- Delete a user: **DELETE** <br/>
  https://treetrails.herokuapp.com/brightbulb/users/`username`
  ```
  {}
  ```

- Get all notes: **GET** <br/>
  https://treetrails.herokuapp.com/brightbulb/notes/
  ```
  {}
  ```

- Add new note: **POST** <br/>
  https://treetrails.herokuapp.com/brightbulb/notes/
  ```
  {
    'title':'',
    'content':'',
  }
  ```  

- Get a note: **GET** <br/>
  https://treetrails.herokuapp.com/brightbulb/notes/`slug`
  ```
  {}
  ```

- Update a note: **PUT** <br/>
  https://treetrails.herokuapp.com/brightbulb/notes/`slug`
  ```
  {
    'title':'',
    'content':'',
  }
  ```

- Delete a note: **DELETE** <br/>
  https://treetrails.herokuapp.com/brightbulb/notes/`slug`
  ```
  {}
  ```

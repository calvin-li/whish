# whish
Simple REST API written in Python, for managing book wishlists.

### Schema
  - User
    - ID (automatically generated, int but can be adapted to guid)
    - First_name
    - Last_name
    - Email (must be unique)
    - Wishlist (array of book ISBNs)
  
  - Book
    - ISBN (serves as ID)
    - Title
    - Author
    - Publish_date
    
### Endpoints
##### `/users`
  - **GET:** Returns all Users
  - **POST:** Create a new User
##### `/users/<user_id>`
  - **GET:** Returns User
  - **PATCH:** Update properties of user
  - **DELETE** Delete User

##### `/users/<user_id>/wishlist`
  - **GET:** Returns that User's wishlist
  - **PUT:** Takes an array of ISBNs. Replaces User's wishlist with input list
  - **POST:** Takes an ISBN as input. Adds that ISBN to the User's wishlist
  
##### `/users/<user_id>/wishlist/<isbn>`
  - **DELETE** Remove book from User's wishlist 

##### `/books`
  - **GET:** Returns all Books
  - **POST:** Adds a new Book to the system
##### `/books/<isbn>`
  - **GET:** Returns Book
  - **PATCH:** Update properties of book
  - **DELETE** Delete Book


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

### Technologies and tools used:
I don't have any experience implementing REST APIs in Python before this, so I did some quick research and went with **Flask** because it looked easy. In particular, it has a built-in test client so I can test the API without having to actually spin up the service.

I also used **sqlalchemy** to help with the translation from database records to JSON. For the database itself, I used **sqlite3** for portability and simplicity. For everything else (eg, unit testing) I used the tools that came with Python. I used **PyCharm** for my IDE.

### Usage and Testing
The app runs on Python 3. Just run `App.py` to start the service. You can follow the schema to create users, add books, and update the wishlists. Data is stored in the `db` folder, in `whish.db`

Test files are in the `Tests` folder. You can run them using `python.unittest`. The tests copy the `test_base.db` database so they can make changes without affecting subsequent tests. 

### Final notes
The API isn't fully fleshed out; there isn't GET/POST/PATH/DELETE for every endpoint, and the error messaging needs improvement. I also don't have unit testing of all the possible error cases, particularly formatting of the queries and request bodies. These are all things I would work on if this wasa serious project. I also felt like I had to write too much boilerplate, repetitive code and can probably have used some more/better tooling.

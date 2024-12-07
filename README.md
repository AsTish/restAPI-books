# REST API for Managing Books and Authors

This project is a REST API for working with books and authors, developed using Django REST Framework.

## Features

The API provides the following functionality:

- **Author Management**:
  - Create a new author
  - Retrieve information about an author by their ID
  - Get a list of authors with filtering and sorting options
  - Delete an author (along with all their associated books)

- **Book Management**:
  - Create a new book
  - Retrieve information about a book by its ID
  - Get a list of books with filtering and sorting options
  - Update book information
  - Delete a book


## Installation and Setup

### Step 1: Clone the Repository

Clone the repository to your local machine:

```
git clone https://github.com/AsTish/restAPI-books.git
cd restAPI-books
cd restAPIbooks
```

### Step 2: Set Up a Virtual Environment Using `pipenv`

Ensure you have Python 3.8+ and `pipenv` installed.

1. Create a virtual environment and install dependencies:

    ```
    pipenv install
    ```

2. Activate the virtual environment:

    ```
    pipenv shell
    ```

### Step 3: Set Up the Database

Apply the database migrations:

    python manage.py migrate

### Step 4: Run the Development Server

Start the development server:

```
pipenv python manage.py runserver
```

The API will be accessible at `http://127.0.0.1:8000/`.

---

## API Endpoints

### Author Management

1. **Get a list of authors**  
   `GET /authors/`

2. **Get details of a specific author**  
   `GET /authors/{id}/`

3. **Create a new author**  
   `POST /create/author/` 

4. **Delete an author**  
   `DELETE /author/delete/{id}/`  
   Deleting an author will also delete all books associated with them.

---

### Book Management

1. **Get a list of books**  
   `GET /books/`

2. **Get details of a specific book**  
   `GET /books/{id}/`

3. **Create a new book**  
   `POST /create/books/`

4. **Update a book**  
   `PUT /books/update/{id}/`

5. **Delete a book**  
   `DELETE /books/delete/{id}/`

---

## Swagger UI

You can use Swagger UI to test the API. After starting the server, open your browser and navigate to:

```
http://127.0.0.1:8000/swagger/
```

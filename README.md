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
3. Enter the programm folder

   ```
   cd restAPIbooks
   ```

### Step 3: Set Up the Database

Apply the database migrations:

    python manage.py migrate

### Step 4: Run the Development Server

Start the development server:

```
pipenv run python manage.py runserver
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

Вот пример раздела о тестах для вашего файла `README`, который описывает, как выполнять тесты в проекте:

---

## Testing

### Running the Tests

This project includes tests to verify the functionality of the API endpoints and other components. The tests are written using Django's `TestCase` and `APITestCase` from the `rest_framework` package.

To run the tests, you can use the following command:

```bash
python manage.py test
```

This command will discover and run all the tests in the project.

### Test Coverage

Currently, the project includes tests for the following scenarios:

#### Author Tests
- **Create a new author** (`POST /authors/`): Verifies successful creation of a new author.
- **Create an existing author** (`POST /authors/`): Ensures that an attempt to create a duplicate author (with the same name and birth date) raises an error.
- **Delete an author** (`DELETE /authors/{id}/`): Verifies successful deletion of an author and all associated books.

#### Book Tests
- **Create a new book** (`POST /books/`): Verifies successful creation of a new book.
- **Create an existing book** (`POST /books/`): Ensures that an attempt to create a book with the same title and author raises an error.
- **Update a book** (`PUT /books/{id}/`): Verifies successful update of a book's information.
- **Delete a book** (`DELETE /books/{id}/`): Ensures that a book can be deleted successfully.

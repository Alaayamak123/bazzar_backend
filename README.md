# Flask Book Catalog API

This is a simple Flask-based API for managing a book catalog. It allows you to create catalogs, add books to them, search for books by name, and retrieve book information by ID. The API uses a SQLite database to store catalog and book data.

## Prerequisites

Before running the application, make sure you have the following installed:

- Python 3
- Flask
- Flask-SQLAlchemy

You can install Flask and Flask-SQLAlchemy using `pip`:

```bash
pip install -r requirements.txt
```


## API Endpoints

### Get All Catalogs

- **URL**: `/catalogs`
- **Method**: `GET`
- **Description**: Retrieve a list of all catalogs.
- **Response**:
  - Success: JSON object with a list of catalogs.
  - Error: JSON object with an error message.

### Create Catalog

- **URL**: `/catalogs`
- **Method**: `POST`
- **Description**: Create a new catalog.
- **Request Parameters**:
  - `name` (required): The name of the new catalog.
- **Response**:
  - Success: JSON object with the created catalog information.
  - Error: JSON object with an error message.

### Get All Books

- **URL**: `/books`
- **Method**: `GET`
- **Description**: Retrieve a list of all books in the catalog.
- **Response**:
  - Success: JSON object with a list of books.
  - Error: JSON object with an error message.

### Create Book

- **URL**: `/books`
- **Method**: `POST`
- **Description**: Create a new book in the catalog.
- **Request Parameters**:
  - `name` (required): The name of the new book.
  - `catalog` (required): The ID of the catalog to which the book belongs.
  - `count` (required): The count of the book in the catalog.
- **Response**:
  - Success: JSON object with the created book information.
  - Error: JSON object with an error message.

### Search Books by Catalog ID

- **URL**: `/books/search/<int:id>`
- **Method**: `GET`
- **Description**: Retrieve a list of books in a specific catalog by catalog ID.
- **Response**:
  - Success: JSON object with a list of books in the specified catalog.
  - Error: JSON object with an error message.

### Search Books by Name

- **URL**: `/books/find`
- **Method**: `GET`
- **Description**: Search for books by name or part of the name.
- **Request Parameters**:
  - `name` (optional): The name or part of the name to search for.
- **Response**:
  - Success: JSON object with a list of books matching the search criteria.
  - Error: JSON object with an error message.

### Get Book by ID

- **URL**: `/books/<int:id>`
- **Method**: `GET`
- **Description**: Retrieve detailed information about a book by its ID.
- **Response**:
  - Success: JSON object with the book's information.
  - Error: JSON object with an error message.

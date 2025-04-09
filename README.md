# Lateshow Stephen Mwangi Maina

# Episodes and Guests API

## Overview
This is a Flask-based API designed to manage episodes and their guest appearances. The application implements the relationships between episodes, guests, and appearances as shown in the ER diagram. The API enables you to perform CRUD operations on episodes, guests, and their associated appearances. The `Appearance` model tracks the rating of a guest's appearance on an episode.

## Setup

1. **Create a private repository** in the GitHub organization . Name the repository as `episodes-guests-firstname-lastname` (e.g., `episodes-guests-john-doe`).

2. **Postman Collection**:
   - Download the provided Postman Collection to test your API.
   - Import the collection into your Postman app using the `Upload Files` option.

3. **Flask Setup**: 
   - Clone the repository.
   - Install the required dependencies using `pip install -r requirements.txt`.
   - Run the application using `flask run`.

4. **Database Setup**:
   - Run migrations to set up the database schema.
   - Optionally, generate your own seed data if the provided CSV file isn't working.

## Models

The API uses the following models:

### Episode Model
Represents an episode in the show, including its date and episode number.

### Guest Model
Represents a guest who appeared on the show, including their name and occupation.

### Appearance Model
Joins the `Episode` and `Guest` models, and includes a `rating` to track how well the guest's appearance was received. The `rating` must be between 1 and 5, inclusive.

### Relationships
- An `Episode` has many `Guests` through `Appearance`.
- A `Guest` has many `Episodes` through `Appearance`.
- An `Appearance` belongs to both a `Guest` and an `Episode`.

Cascading deletes are configured for the `Appearance` model to ensure proper cleanup when either a guest or episode is deleted.

## Routes

### `GET /episodes`
Returns a list of all episodes in the system.

#### Example Response:
```json
[
  {
    "id": 1,
    "date": "1/11/99",
    "number": 1
  },
  {
    "id": 2,
    "date": "1/12/99",
    "number": 2
  }
]

#### Testing

- Import the provided Postman collection to verify your API functionality.
- Run the tests and ensure all routes respond correctly, including proper validation of the rating field.

```

Contributing

1. Fork the repository.
2. Clone the forked repository to your local machine.
3. Make your changes and commit them.
4. Push your changes and create a pull request.

```

 Created by Steve Mwangi





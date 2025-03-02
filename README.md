# Fund Management System

A Django-based web application for managing funds, including uploading CSV files containing fund data and viewing a list of funds with various filters.

## Features

- **Upload Funds**: Allows users to upload CSV files containing fund details (Name, Strategy, AUM, Inception Date). The system validates the CSV file for required columns.
- **View Fund List**: Displays a list of funds, with the ability to filter by strategy.
- **Delete Fund**: Allows users to delete a fund from the system.
- **Rate Limit**: Option to limit requests to API.
- **Performance Logs**: Track the performance of requests (optional but can be implemented).
- **File Size Limit**: Uploaded CSV files are restricted to a maximum of 10MB.
- **Unit Tests**: Includes automated unit tests for the fund API to ensure the system behaves as expected.

## Prerequisites

To run this project, ensure you have the following installed:

- Python 3.8+ (recommended)
- pip (Python package installer)
- Virtual environment (optional but recommended)

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/HamzaaMB/fund-project.git
```

### 2. Create a Virtual Environment
To keep dependencies isolated, create a virtual environment in the project directory.

```bash
python -m venv venv
```
Activate the virtual environment:

- On Windows:
```bash
venv\Scripts\activate
```
- On macOS/Linux:
```bash
source venv/bin/activate
```

### 3. Install Dependencies
Install the required dependencies from the requirements.txt file:
```
pip install -r requirements.txt
```

### 4. Set Up the Database
Ensure you have a database set up (e.g., PostgreSQL) and update the DATABASES setting in settings.py accordingly.

Then, run the migrations to set up your database:
```
python manage.py migrate
```

### 4. Run the Development Server
To start the development server:
```
python manage.py runserver
```
Access the application in your browser at (for the funds list):
```
http://127.0.0.1:8000
```

Access the upload page:
```
http://127.0.0.1:8000/upload
```
## Unit Tests
To run the tests for the API, use the following command:
```
python manage.py test funds/api
```

To run the tests for funds:
```
python manage.py test funds
```

## Technology Stack
- Django: Web framework for building the application.
- Django Rest Framework: For building RESTful APIs.
- Pandas: For processing and validating the CSV files.
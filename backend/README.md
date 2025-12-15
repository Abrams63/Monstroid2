# FastAPI Backend Server

This backend server serves the static website located in the `../site/` directory using FastAPI and uvicorn.

## Setup Instructions

1.Navigate to the backend directory:

``` bash
cd backend
```

2.Install the required dependencies:

``` bash
pip install -r requirements.txt
```

3.Start the server:

``` bash
python -m uvicorn server:app --host 127.0.0.1 --port 8000 --reload
```

   Or use the run script:

``` bash
python run_server.py
```

## Accessing the Website

Once the server is running, you can access the website at:

- Main page: <http://127.0.0.1:8000/>
- All static assets (CSS, JS, images, etc.) are served from the `../site/` directory

## Features

- Serves `index.html` as the main page when accessing the root URL
- Serves all static files (CSS, JS, images, etc.) from the site directory
- Handles client-side routing by returning `index.html` for non-existent routes
- Includes hot reloading during development for easier debugging

## Form Handling

The server handles form submissions through the `/contact` endpoint, supporting:

- Contact forms
- Subscription forms
- Order forms
- reCAPTCHA validation (placeholder implementation)
- Email sending functionality

## Configuration

- Email settings can be configured in `email_config.json`
- reCAPTCHA keys can be set via environment variables

## Project Structure

``` bash
backend/
├── server.py          # Main FastAPI application
├── email_config.json  # Email configuration
├── requirements.txt   # Python dependencies
├── run_server.py      # Script to install dependencies and run the server
├── test_server.py     # Script to test the server functionality
└── README.md          # This file
```

# PPI Project

## What is this website?

This is a professional website built with HTML, CSS, and JavaScript, featuring a responsive design and modern UI components. The site includes multiple pages such as homepage, about, contacts, and typography sections. It implements various interactive elements including sliders, contact forms, image galleries, testimonials, and newsletter subscription functionality.

## Tech Stack

### Frontend

- HTML5
- CSS3 (with Bootstrap framework)
- JavaScript
- Responsive design with mobile-first approach
- Font Awesome icons
- Google Fonts integration

### Backend

- Python (FastAPI framework)
- Uvicorn ASGI server
- SMTP email handling
- reCAPTCHA integration (placeholder implementation)

## Project Structure

```bash

├── backend/
│   ├── server.py              # Main FastAPI application
│   ├── email_config.json      # Email configuration
│   ├── requirements.txt       # Python dependencies
│   ├── run_server.py          # Script to install dependencies and run the server
│   ├── test_server.py         # Script to test the server functionality
│   └── README.md              # Backend documentation
└── site/
    ├── index.html            # Main homepage
    ├── about.html            # About page
    ├── contacts.html         # Contacts page
    ├── typography.html       # Typography page
    ├── css/
    │   ├── bootstrap.css     # Bootstrap framework
    │   └── style.css         # Custom styles
    ├── js/
    │   ├── core.min.js       # Core JavaScript functionality
    │   └── script.js         # Custom scripts
    ├── fonts/                # Font files
    ├── images/               # Image assets
    └── video/                # Video assets
```

## Backend Documentation

For detailed information about the backend implementation, configuration, and setup instructions, please refer to the [Backend README](backend/README.md).

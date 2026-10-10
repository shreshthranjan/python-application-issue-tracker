# Python Application Issue Tracker

A desktop application built with Python and Tkinter to help support teams record, manage, track, and report application issues.

## Features

- Add and view incidents
- Search for incidents
- Update incident status
- Delete incidents with confirmation
- Track issue priority
- Dashboard with incident statistics
- Reports grouped by status and priority
- SQLite database for persistent storage
- Logging and input validation
- Error handling

## Technologies Used

- Python
- Tkinter and ttk
- SQLite
- Logging
- Git and GitHub

## Project Purpose

This project simulates a basic application support workflow, where incidents are recorded, assigned priorities, tracked through different statuses, and reviewed using reports.

It was built to practice Python programming, database operations, GUI development, debugging, logging, and error handling.

## Application Statuses

- Open
- In Progress
- Resolved

## Installation and Setup

### Prerequisites

- Python 3.10 or later
- Git (optional, for cloning the repository)

### 1. Clone the Repository

```bash
git clone <your-github-repository-url>
cd application_issue_tracker
```

### 2. Run the Application

Run the following command from the project directory:

```bash
python gui.py
```

The application opens in a desktop window.

### Database

The application uses SQLite to store incident records in `incidents.db`. The database file is located in the project directory.

### Logging

Application events and errors are recorded in `app.log` to help with troubleshooting.

## Future Improvements

- Add incident filtering and sorting
- Improve automated test coverage
- Add incident export to CSV
- Package the application as a Windows executable
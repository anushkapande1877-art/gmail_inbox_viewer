# gmail_inbox_viewer
A Flask-based Gmail inbox viewer that connects via IMAP, filters emails by sender, and displays messages through a web interface.

# Gmail Inbox Viewer

A Flask-based application that connects to Gmail using IMAP and displays emails from a specified sender in a web interface.

## Features

* Connects to Gmail via IMAP
* Filters emails by sender
* Displays subject, sender, date, and email content
* Simple Flask-based interface

## Requirements

* Flask

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Then open:

```text
http://localhost:5001
```

## Note

Before running the application, update the following variables in `app.py`:

```python
EMAIL_ADDRESS = "your_email@gmail.com"
APP_PASSWORD = "your_app_password"
FILTER_SENDER = "sender@gmail.com"
```

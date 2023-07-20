# bot_status

This is a django project that provides an api to monitor the status of some python apps running on a centos server. The api returns a json response with the process information and the error message (if any) for each app.

## Requirements

- Python 3.9
- Django 3.2.10
- djangorestframework 3.13.0
- gunicorn 20.1.0

## Installation

- Clone this repository to your server:

```bash
git clone https://github.com/your_username/bot_status.git /var/www/bot_status
```

- Change to the project directory:

```bash
cd /var/www/bot_status
```

- Activate the virtual environment:

```bash
source env/bin/activate
```

- Install the dependencies:

```bash
pip install -r requirements.txt
```

- Migrate the database:

```bash
python manage.py migrate
```

## Usage

- Start gunicorn on port 8080:

```bash
gunicorn --bind 0.0.0.0:8080 bot_status.wsgi:application
```

- Send a GET request to the api endpoint:

```bash
curl http://localhost:8080/bot_status/
```

- You should see a json response with the status of your processes. For example:

```json
[
    {
        "goiu_v3.py": "running",
        "error_log": "No log",
        "status_code": 1
    },
    {
        "copn.py": "running",
        "error_log": "No log",
        "status_code": 1
    },
    {
        "main.py": "running",
        "error_log": "No log",
        "status_code": 1
    },
    {
        "app.py": "down",
        "path": "/home/novogad/novoapi/app.py",
        "status_code": 3
    },
    {
        "main.py": "running",
        "error_log": "No log",
        "status_code": 1
    }
]

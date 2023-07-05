# File Server

This project is a file server that allows users to download and preview files uploaded by an admin, and share them as email attachments. It is built with the Django framework to scale to meet the needs of a growing business.

# Development

- Copy the env_sample file to .env and update it with your postgres, smtp, and dropbox credentials.
- Install requirements with pip, run database migrations, and start the server.

```bash
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver
```

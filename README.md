# 🪸 Portfolio.co — Flask Profile App

A clean Flask profile application with real profile-picture uploads.

## Features

- Profile picture upload
- PNG/JPG/JPEG/GIF/WEBP support
- 5 MB upload limit
- Image preview before upload
- Username
- Email
- Bio
- Profile card
- Edit/update profile
- Delete profile
- Responsive design
- Clean modern CSS
- Automatic upload directory creation

## Folder Structure

ECE_A/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   └── base.html
└── static/
    └── uploads/

## Install

```powershell
python -m pip install -r requirements.txt
```

## Run

```powershell
python app.py
```

Open:

http://127.0.0.1:5000

## Important

Uploaded images are stored in:

static/uploads/

The current version stores the profile information in memory, so restarting Flask clears the profile data. For permanent storage, add SQLite/SQLAlchemy later.

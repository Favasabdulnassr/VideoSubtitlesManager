# Video Subtitle Manager

## Overview

The Video Subtitle Manager allows users to upload videos, extract multiple subtitles, and select from them through a small interface in the video player. It includes a search functionality that enables users to search for specific words, phrases, or letters within subtitles. The search results display the related subtitle sentences with timestamps. When a timestamp is clicked, the video will automatically start playing from that specific point.





# WITH DOCKER
Ensure Docker is installed and running on your system.


## clone git

```
git clone https://github.com/Favasabdulnassr/VideoSubtitlesManager.git
cd VideoSubtitlesManager

```

## Update Database Configurations

Update the database settings in the Django settings.py file

```

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": 'video_subtitle_extraction',
        "USER": 'postgres',
        "PASSWORD": '3636',
        "HOST": 'postgres_db',
        "PORT": "5432",
    }
}

```

## Build the Application with Docker Compose

```
docker-compose up --build -d
```



<------------------------------>

# WITHOUT DOCKER

## Clone the Repository

```
git clone https://github.com/Favasabdulnassr/VideoSubtitlesManager.git
cd VideoSubtitlesManager

```

## Create a Virtual Environment

```
python -m venv venv
source venv/bin/activate   # On Mac
venv\Scripts\activate   # On Windows

```

## Install Dependencies

```
pip install -r requirement.txt

```

## Add Environment Variables

-> Create a .env file in the project root.
-> Add the following information and replace with your actual database credentials:

```
DB_HOST= your_db_host
DB_USER= your_db_user
DB_PASSWORD= your_db_password
DB_NAME= your_db_name

```

## Apply Migrations


```
python manage.py migrate

```

## Run Application

```
python manage.py runserver
```


---End--





## Screenshots

A folder named screenshot_folder has been added to the project directory. It contains screenshots showing the project in action, including:

Uploading a video
Selecting a subtitle
Searching for subtitle phrases
Clicking timestamps to jump to specific points in the video
Feel free to check the screenshots to see the interface and functionalities in use.
# TinyGallery Backend (FastAPI)

## Introduction
The Backend of [TinyGallery Vue Edition](https://github.com/WeepingDogel/tinygallery-vue), powered by FastAPI.


# Running for test

```commandline
git clone git@github.com:WeepingDogel/tinygallery-backend.git
```
```commandline
cd tinygallery-backend
```
```commandline
python -m venv venv
```
```commandline
source ./venv/bin/activate
```
```commandline
pip install -r requirements.txt
```
```commandline
uvicorn app.main:app --reload
```
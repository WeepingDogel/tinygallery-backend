#!/bin/bash
service nginx start &
uvicorn app.main:app --host 127.0.0.1 --port 8000
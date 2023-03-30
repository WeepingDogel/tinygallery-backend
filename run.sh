#!/bin/bash

filename="secret.txt"

if [ ! -e "$filename" ]; then
  openssl rand -hex 32 >> "$filename"
  uvicorn app.main:app
else
  uvicorn app.main:app
fi
#!/bin/bash

filename="secret.txt"

if [ ! -e "$filename" ]; then
  openssl rand -hex 32 >> "$filename"
  uvicorn app.main:app --host 0.0.0.0
else
  uvicorn app.main:app --host 0.0.0.0
fi
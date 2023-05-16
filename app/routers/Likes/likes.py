from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path
from app.dependencies.db import get_db
from app.model import crud
from app.utilities import dir_tool



#!/usr/bin/env bash

# Activate virtual environment if you have one
# source venv/bin/activate

echo " Starting Reminder Bot Server..."
uvicorn app.main:app --reload --port 8000
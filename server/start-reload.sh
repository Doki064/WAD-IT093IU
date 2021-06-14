#!/usr/bin/env bash

# Start uvicorn instead while in development stage
uvicorn main:app --host 0.0.0.0 --port 8080 --reload

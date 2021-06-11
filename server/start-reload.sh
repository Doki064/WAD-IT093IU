#!/usr/bin/env bash

# Start uvicorn instead while in development stage
uvicorn server.main:app --host 0.0.0.0 --port 8080 --reload

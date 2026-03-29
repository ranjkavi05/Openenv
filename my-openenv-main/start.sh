#!/bin/bash
# Start the FastAPI server in the background
uvicorn api:app --host 0.0.0.0 --port 8000 &

# Start the Streamlit application in the foreground
streamlit run app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true

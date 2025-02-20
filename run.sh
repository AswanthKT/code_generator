#!/bin/bash



# Start the backend
cd backend
python3 server.py &

# Start the frontend
cd ../frontend
streamlit run app.py

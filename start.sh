Xvfb :1 -screen 0 1024x768x16 &
export DISPLAY=:1
uvicorn main:app --host 0.0.0.0 --port $PORT

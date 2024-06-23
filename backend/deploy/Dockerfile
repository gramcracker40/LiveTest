FROM python:3.11-slim
WORKDIR /app
COPY ./backend .
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python3", "API.py"]
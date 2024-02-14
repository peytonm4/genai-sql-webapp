# app/Dockerfile
#
# build with ~/github/genai-sql-co3/ docker build -t streamlit .
#
# run with   ~/github/genai-sql-co3/ docker run -it --rm -p 127.0.0.1:8501:8501 streamlit

FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

#Reference requirements file in repository - this file holds all the necessary modules and versioning to run the application
COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
# Run command streamlit -m run streamlit_web.py to begin running application using streamlit front end
ENTRYPOINT ["streamlit", "run", "streamlit_web.py"]

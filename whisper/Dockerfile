# FROM python:3.10-slim

# WORKDIR /whisper

# COPY requirements.txt requirements.txt
# RUN apt-get update && apt-get install git -y
# RUN pip3 install --upgrade pip
# RUN pip3 install -r requirements.txt
# RUN pip3 install "git+https://github.com/openai/whisper.git"
# RUN pip3 install --upgrade openai
# RUN apt-get install -y ffmpeg

# COPY /whisper /whisper

# EXPOSE 5000

# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    git \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install gitpython
RUN pip install git+https://github.com/openai/whisper.git

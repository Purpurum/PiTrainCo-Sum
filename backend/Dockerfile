FROM python:3-slim-buster

run apt-get update
RUN apt-get install -y libgl1-mesa-glx libglib2.0-0

RUN mkdir /code

WORKDIR /code

# 
COPY requirements.txt .

RUN pip install -r requirements.txt
# 
COPY . .

# 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
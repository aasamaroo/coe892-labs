# Choose Python Version
FROM python:3.9

#Setup working directory
WORKDIR /code

#Copy requirements into working directory
COPY ./requirements.txt /code/requirements.txt

#Install dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#Copy code to working directory
COPY ./app /code/app

#Run the Uvicorn command inside container
CMD ["uvicorn", "app.Server.app", "--host", "0.0.0.0", "--port", "80"]
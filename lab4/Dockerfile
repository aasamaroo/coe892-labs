# Choose Python Version
FROM python:3.9


#Setup working directory
WORKDIR /app

#Copy requirements into working directory
COPY requirements.txt .

#Install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt


#Copy code to working directory
COPY . .

EXPOSE 8000

#Run the Uvicorn command inside container
CMD ["uvicorn", "app.Server:app", "--host", "0.0.0.0", "--port", "8000"]
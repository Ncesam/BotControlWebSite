# Use the official Python image
FROM python:3.13-alpine

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . ./

# Expose the application port (default FastAPI port)
EXPOSE 8000


# Run the FastAPI app using Uvicorn
CMD ["/bin/bash", "alembic revision --autogenerate", "&& alembic upgrade head","&& uvicorn", "src.API.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]

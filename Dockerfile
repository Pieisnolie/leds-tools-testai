# Use a base Python image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy project files to the container
COPY requirements.txt requirements.txt
COPY src/Interface/api/api.py api.py
COPY src/Interface/api/api2.py api2.py
# COPY api2.py api2.py
# COPY .env .env

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 (where FastAPI will run)
EXPOSE 8000
# EXPOSE 8080

# Command to run the app
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["uvicorn", "api2:app", "--host", "0.0.0.0", "--port", "8000"]

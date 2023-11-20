# Use slim-bookworm as a parent image
FROM python:3.11-slim-bookworm

# Set the working directory in the container
WORKDIR /usr/src/app

# Install Pipenv
RUN pip install pipenv

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install dependencies using Pipenv
RUN pipenv install --ignore-pipfile

# Run the application
CMD ["uvicorn src.main:app --reload"]
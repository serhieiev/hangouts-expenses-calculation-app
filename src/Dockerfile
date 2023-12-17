# # Use python:3.10-slim as a base image
# FROM python:3.10-slim as base

# # Set the working directory in the container
# WORKDIR /usr/src/app

# # Install Pipenv
# RUN pip install pipenv

# # Copy the Pipfile and Pipfile.lock into the container
# COPY Pipfile Pipfile.lock ./

# # Install dependencies using Pipenv in the system python, not in a virtualenv
# RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --ignore-pipfile

# # Copy the rest of the application
# COPY . .

# # Run the application
# CMD ["uvicorn", "src.main:app", "--reload"]

# Define the Python version as an argument
ARG PYTHON_VERSION=3.11

# Use Alpine as the builder image
FROM alpine:latest as builder

# Set the Python version argument in the builder stage
ARG PYTHON_VERSION

# Create a virtual environment and install dependencies
RUN apk add --no-cache python3~=$PYTHON_VERSION py3-pip && \
    python3 -m venv /venv

# Set the working directory
WORKDIR /app

# Activate the virtual environment and install dependencies
COPY src/requirements.txt ./
RUN source /venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

# Copy your application
COPY src /app

# Compile Python byte-code
RUN source /venv/bin/activate && \
    python -m compileall -o 2 .

# Use scratch for the final minimal image
FROM scratch

# Copy over the necessary Python files and libraries from the builder stage
COPY --from=builder /venv /venv
COPY --from=builder /lib/ld-musl-x86_64.so.1 /lib/
COPY --from=builder /usr/lib /usr/lib/
COPY --from=builder /app /app

# Set the working directory and entry point for running your application
WORKDIR /app
ENTRYPOINT ["/venv/bin/python"]
CMD ["uvicorn", "main:app", "--reload"]

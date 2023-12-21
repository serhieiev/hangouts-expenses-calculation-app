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

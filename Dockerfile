
    # Use a lightweight Linux environment with Python pre-installed
    FROM python:3.10-slim

    # Set the working directory inside the container
    WORKDIR /app

    # Copy your requirements and install them
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt

    # Copy the rest of your project files into the container
    COPY scripts/ ./scripts/
    COPY tests/ ./tests/

    # Ensure the bash script has execution permissions inside the container
    RUN chmod +x scripts/orchestrate_tests.sh

    # Define the command that runs automatically when the container starts
    ENTRYPOINT ["/bin/bash", "-c", "./scripts/orchestrate_tests.sh"]
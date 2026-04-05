# Step 1: Use an official, lightweight Python base image
FROM python:3.10.14-slim-bookworm

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy only the requirements first (this optimizes Docker caching)
COPY requirements.txt .

# Step 4: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of application code
COPY monitor.py .

# Step 6: Do not run the container as root!
RUN useradd -m dummy
USER dummy

# Step 7: The command that runs when the container starts
CMD ["python", "monitor.py"]
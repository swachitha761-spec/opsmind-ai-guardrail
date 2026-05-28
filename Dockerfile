# Step 1: Download a lightweight, official miniature Linux operating system with Python pre-installed
FROM python:3.11-slim

# Step 2: Create a secure working directory inside the container space
WORKDIR /app

# Step 3: Copy our dependency list inside the container first
COPY requirements.txt .

# Step 4: Install all our Python libraries inside the container's isolated system
RUN pip install --no-cache-dir -r requirements.txt google-genai

# Step 5: Copy our actual source code folder into the container layout
COPY src/ ./src

# Step 6: Expose port 8000 so the container can receive internet traffic from the outside world
EXPOSE 8000

# Step 7: The execution command that fires up our Uvicorn server the second the container boots
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
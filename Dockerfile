# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install uv
RUN pip install uv

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN uv pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container at /app
COPY src/ /app/src/

# Copy the .env file
COPY .env /app/.env

# Make port 8501 available to the world outside this container (for Streamlit)
EXPOSE 8501

# Define environment variable
ENV OPENAI_API_KEY=$OPENAI_API_KEY

# Run app.py when the container launches
CMD ["uv", "run", "streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]

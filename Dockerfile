# 1. We use an official (lightweight) Python base image
FROM python:3.13-slim

# 2. We set the working directory inside the container
WORKDIR /app

# 3. We only copy the requirements file first (to take advantage of the cache)
COPY requirements.txt .

# 4. Now that we installed the facilities
RUN pip install --no-cache-dir -r requirements.txt

# 5. We copy all the rest of the code to the container
COPY . .

# 6. Initialize the database within the container
# (This ensures the database exists and the table has been created)
RUN python app/database/init_db.py

# 7. (Optional) If you want the database to already have test data, uncomment this line:
# RUN python populate_db.py

# 8. We're exposing port 5000 so we can enter
EXPOSE 5000

# 9. Command to start the server when the container starts
CMD ["python", "run.py"]
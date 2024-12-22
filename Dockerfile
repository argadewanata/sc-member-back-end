FROM python:3.10.15-slim

WORKDIR /opt/sc-member-back-end

# Copy only the requirements file first and install dependencies to use caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

EXPOSE 8000

ENTRYPOINT [ "python", "-u", "main.py" ]
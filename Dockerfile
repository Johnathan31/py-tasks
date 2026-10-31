FROM python:3.14.4-slim

WORKDIR /app

# activating the virtual environment
RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Creating a non-root user
RUN useradd -m python
RUN chown -R python:python /app

USER python

# Starting the docker container
CMD ["./start.sh"]


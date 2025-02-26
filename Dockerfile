FROM python:3.12-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install necessary packages
RUN mkdir /crm

# Copy requirements file
COPY ./crm/requirements.txt /crm/requirements.txt

# Set workdir
WORKDIR /crm

# Install python packages
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy code into 
COPY ./crm /crm
# Taskapp

A Flask Application to find the distance from the Moscow Ring Road to the specified address. The address is passed to the application in an HTTP request

## Installation and Run

[Docker](https://docker.com) is required to install taskapp.

Build the Docker Image
```bash
docker build -t taskapp:latest .
```
Run application
```bash
docker run -d -p 5000:5000 taskapp:latest
```
Confirm run

```bash
docker ps
```

## Usage
Visit site and enter address location
```bash
http://localhost:5000
```
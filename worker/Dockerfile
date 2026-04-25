FROM python:3.12-slim
WORKDIR /app
COPY worker.py .
RUN echo "intentional worker build break" && exit 17
EXPOSE 9000
CMD ["python", "worker.py"]

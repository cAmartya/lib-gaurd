FROM python:3.10-bullseye

WORKDIR /app
# Copy source code
COPY . /app/
# Create volume mount points
VOLUME ["/app/static"]
VOLUME [ "/app/instance" ]
# install dependencies
RUN pip install -r requirements.txt
# expose port
EXPOSE 8000
# command
CMD [ "python", "src/main.py" ]
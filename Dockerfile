FROM datatransfer:latest
WORKDIR /app/
COPY . .
CMD [ "poetry", "run", "python", "main.py" ]
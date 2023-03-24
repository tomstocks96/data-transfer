FROM datatransfer:latest
WORKDIR /app/
COPY . .        
CMD [ "poetry", "run", "python", "-m", "faust", "-A", "main", "worker", "-l", "info"]
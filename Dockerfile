FROM datatransfer:latest
WORKDIR /app/
COPY . .        
CMD [ "faust", "-A", "main"]
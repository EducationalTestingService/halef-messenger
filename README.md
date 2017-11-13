## halef-messenger

halef-messenger is a message server based on SocketIO using WebSocket and HTTP. Clients can register via WebSocket and receive messages from other clients via WebSocket or HTTP. HTTP clients do not need to register to send a message.

### Requirements
You need docker and docker-compose installed on your machine. 

### Development
Run a development server (Interrupt with [Ctrl]+[C]):  
```docker-compose up --build``` 

Stop the containers:  
```docker-compose stop```.

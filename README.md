## halef-messenger

halef-messenger is a message server based on SocketIO using WebSocket and HTTP. Clients can register via WebSocket and receive messages from other clients via WebSocket or HTTP. HTTP clients do not need to register to send a message.

## API
An example website connecting using SocketIO is provided in examples/index.html. The website registers as user '1234' and sends two messages two itself.

The 'examples/http-post.sh' script can be used to test the HTTP endpoint. It will send a message to users registered as '1234'.

For more details, look at the comments in the examples.

## Getting started

### Requirements
You need docker and docker-compose installed on your machine. 

### Starting a development server
Run 'docker-compose up --build' inside the development directory. Once you are done, you can interrupt the command and stop the container with 'docker-compose stop'.

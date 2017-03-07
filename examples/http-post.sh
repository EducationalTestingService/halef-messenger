#!/bin/bash

set -e 

# Sends JSON message '{"command":"function", "arg1": "Hello world"}' to user '1234' with namespace 'custom-api'.
# Returns false if no user '1234' is connected. Returns true otherwise.
curl -X POST -d 'user=1234&event=custom-api&message={"command":"function", "arg1": "Hello world"}' http://localhost:8000/messenger/send_json
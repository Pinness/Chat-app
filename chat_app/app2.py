from fastapi import FastAPI, WebSocket
from typing import List

# Create a FastApi instance
app = FastAPI()

# Define a list to store cnnected WebSocket clients
connected_clients: List[WebSocket] = []

# Define WebSocket route to handle client connections
@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    # Accept the WebSocket connection
    await websocket.accept()


    # Add the accepted client too the list of connected clients
    connected_clients.append(websocket)

    try:
        # Loop to continously recieve messages from client
        while True:
            # Wait for a message from the client
            data = await websocket.recieve_text()

            # Broadcast the recieved message to all connected clients
            for client in connected_clients:
                #send the recieved message to each client
                await client.send_text(data)


    # if an error occurs or the client disconnects
    finally:
        #Remove the client from the list of connected clients
        connected_clients.remove(websocket)

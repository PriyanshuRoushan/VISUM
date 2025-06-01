from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os,requests

app = FastAPI()
connected_clients = []
load_dotenv()


API_KEY = os.getenv("MAP_API_KEY")


# Allow frontend to connect (CORS config)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws/location")
async def location_websocket(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    print("Client connected")

    try:
        while True:
            data = await websocket.receive_json()
            # Broadcast to all other clients (like OpenCV app)
            # print(data["latitude"],data["longitude"])

            friendly_address = getAddress(lat=data["latitude"],lng=data["longitude"])

            data["address"] = friendly_address["location"]
            print(data)
            for client in connected_clients:
                if client != websocket:
                    await client.send_json(data)
    except Exception as e:
        print("Client disconnected:", e)
        connected_clients.remove(websocket)


def getAddress(lat, lng):
    # Reverse Geocode
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={API_KEY}"
    response = requests.get(geocode_url)
    address = "Unknown"
    if response.status_code == 200 and response.json().get("results"):
        address = response.json()["results"][0]["formatted_address"]

    # print(f"Location: {address}")
    return {"location":address}
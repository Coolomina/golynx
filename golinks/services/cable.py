from starlette.websockets import WebSocket
from starlette.websockets import WebSocketDisconnect

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            await websocket.send_text(f"Received: {message}")
    except WebSocketDisconnect:
        pass

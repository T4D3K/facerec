import asyncio
import websockets

N = 100

WEBSOCKET_URL = "ws://localhost:8080/ws/v1/faces"


async def listen_websocket(index):
    try:
        async with websockets.connect(WEBSOCKET_URL) as websocket:
            print(f"[WebSocket {index}] Connected to {WEBSOCKET_URL}")

            while True:
                try:
                    message = await websocket.recv()
                    print(f"[WebSocket {index}] Received: {message}")
                except websockets.ConnectionClosed:
                    print(f"[WebSocket {index}] Connection closed")
                    break
    except Exception as e:
        print(f"[WebSocket {index}] Error: {e}")


async def main():
    tasks = [listen_websocket(i) for i in range(1, N + 1)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())

import asyncio

from starlette.websockets import WebSocketDisconnect

from app.business_logic.models import PubSubChannel
from app.business_logic.ports import PubSubManager


class SendWsNotificationCmd:
    def __init__(self, pubsub_manager: PubSubManager):
        self.pubsub_manager: PubSubManager = pubsub_manager

    async def execute(self, ws):
        await ws.accept()
        pubsub = await self.pubsub_manager.subscribe(PubSubChannel.img_channel)

        try:
            await asyncio.gather(self.ignore_incoming_messages(ws), self.send_messages(pubsub, ws))

        finally:
            await self.pubsub_manager.unsubscribe(pubsub, PubSubChannel.img_channel)
            await self.pubsub_manager.close()

    async def ignore_incoming_messages(self, ws):
        try:
            while True:
                await ws.receive_text()
        except WebSocketDisconnect:
            pass

    async def send_messages(self, pubsub, ws):
        try:
            async for message in pubsub.listen():
                if message["type"] == "message":
                    await ws.send_text(message["data"].decode("utf-8"))
        except WebSocketDisconnect:
            pass

from main import app
import uvicorn

uvicorn.run(app=app, host="localhost", port=8081)

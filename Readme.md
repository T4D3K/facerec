### Task Description

Task: Real-Time Face Detection and Image Generation Server

Description:
You are tasked with developing a server application that receives an image via a POST request,
detects faces in the provided image, generates a new image with the detected faces marked,
and returns a URL to the new image using websockets. Additionally, you need to create an
endpoint for serving the generated image.

Requirements:

1. Implement a server using Python with a framework such as Django.
2. Set up an endpoint to receive an image via a POST request: /image
3. Use a face detection algorithm to find coordinates of faces in the provided image.
4. Generate a new image with the detected faces marked as bounding boxes around the
   faces.
5. Implement websockets to send the URL of the generated image to all connected clients
   in real-time. Websocket endpoint: /faces
6. Serve the generated image using an endpoint with a unique URL.
7. Ensure that the server handles errors gracefully and provides informative error
   messages when necessary.
8. The app must be running in a docker container on port 8282
9.

Submission Guidelines:

1. Submit your code via a Git repository (GitHub, GitLab, etc.).
2. Include a README.md file with instructions on how to run the server.
3. Provide any necessary setup/configuration instructions.
4. Optionally, include any additional notes or explanations about your implementation
   choices.

# Solution

Ad.1 I've picked up FastAPI over Django as I don't need database integration built in, what's more I like FastAPI much
more.

Ad.2 I decided to rename endpoint from `image` to `images` as it's closer to REST standard in my opinion, I prefer much
more plural form of endpoints.

Ad.3 As face detection algorithm I used openCV library with already trained model, as I'm not an ML engineer I didn't
want to open already opened doors by building own face recognition mechanism.

Apart from points above this project presents my understanding and own implementation of Hexagonal Architecture which I
call Hexagonal abc. Basically it coresponds to project structure where there are 3 main
components: `adapters`, `business_logic` and `core`

```
app/ 
│── adapters/  # ports integration
│── business_logic/ # here all logic happens
│───── ports.py # interfaces for ports
│── core/ # configuration, factories etc.
```

If you wonder why repository is a context manager, basically it's because ofter reporistories are saving data in
database and they need to handle session, with this approach we can easily session.commit() in `__exit__`

## How it works?

Whenever image is sent to `api/v1/images` it will be validated and processed by OpenCV. Image and it's metadata, are
saved on local disk from which they are served by `api/v1/images/{uuid}` endpoint.
There is also `api/v1/images/{uuid}/meta` endpoint providing file metadata.

As soon as file is processed, message is published on specific channel (I've used redis as it's simple).

Reason behind that is app is being served by multiple gunicorn workers, and it needs to send
message to each ws connection no matter on which worker image was processed. It also allows to scale solution better.

### *Important*

Improvement:

`POST` on `/api/v1/images` should not trigger image processing (as it does right now), it should trigger a job (e.g.
using Celery) and that job should publish message on channel, so all regiestered websocket connections can get message.

## Local setup

Install virtualenv + make redis running

```shell
make install
make redis-up
```

Run app from terminal, it will run on port 8081

```shell
export PYTHONPATH=${PYTHONPATH}:$(pwd)
.venv/bin/python app
```

#### OR

Build docker image

```shell
make build
```

Run app in docker, app will be served on port 8282 which will be mapped to localhost:8080

```shell
make compose-up
```

#### THEN

Run 100 ws connections

```shell
make ws
```

#### AND

visit [docs](http://localhost:8080/docs) -> that should open swagger

Whenever you send a valid file with face, your ws connections should display url to that file
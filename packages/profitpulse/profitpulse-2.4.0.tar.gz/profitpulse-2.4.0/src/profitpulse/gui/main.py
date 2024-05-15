import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

gui = FastAPI()


def start_server() -> None:
    print("Open your browser and go to http://127.0.0.1:8000")
    print("Press CTRL + C to terminate")
    uvicorn.run(gui, host="127.0.0.1", port=8000, log_level="critical")


@gui.get("/", response_class=HTMLResponse)
def homepage() -> HTMLResponse:
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Profit Pulse</title>
    </head>
    <body>
        <h1>Profit Pulse</h1>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

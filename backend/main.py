from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Mount the site directory to serve static files
app.mount("/site", StaticFiles(directory="../site"), name="site")
app.mount("/css", StaticFiles(directory="../site/css"), name="css")
app.mount("/js", StaticFiles(directory="../site/js"), name="js")
app.mount("/images", StaticFiles(directory="../site/images"), name="images")
app.mount("/fonts", StaticFiles(directory="../site/fonts"), name="fonts")
app.mount("/video", StaticFiles(directory="../site/video"), name="video")

@app.get("/")
async def read_root():
    # Serve the index.html file from the site directory
    return FileResponse("../site/index.html")

@app.get("/index.html")
async def read_index():
    # Also serve index.html when specifically requested
    return FileResponse("../site/index.html")

@app.get("/about.html")
async def read_about():
    return FileResponse("../site/about.html")

@app.get("/contacts.html")
async def read_contacts():
    return FileResponse("../site/contacts.html")

@app.get("/typography.html")
async def read_typography():
    return FileResponse("../site/typography.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.1", port=8000)
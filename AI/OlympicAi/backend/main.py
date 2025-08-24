import os
from typing import Annotated
from io import BytesIO
from fastapi import FastAPI, File, UploadFile,  HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse, FileResponse, JSONResponse
from AI.MediaPipe import MediaPipeVideoProcessor
import tempfile


app = FastAPI()
# Dictionary to store uploaded videos in memory (filename -> BytesIO buffer)
video_store = {}


# POST ----------------------------------------------------------------------


# 📤 Endpoint to upload a file using FastAPI's UploadFile.
# This method is more efficient for large files, as it streams the data.
# Only the filename is returned in the response.
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}


# 📤 POST endpoint to upload a video without any processing.
# The uploaded video is saved to the 'uploaded/' directory on disk.
# The filename is returned in the response.
@app.post("/upload/")
async def upload_video(file: UploadFile):
    upload_dir = "uploaded"
    os.makedirs(upload_dir, exist_ok=True)  # Create folder if it doesn't exist
    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return {"filename": file.filename, "status": "uploaded"}


# 📤 POST endpoint to upload a video and store it in memory.
# The video file is read fully into RAM and saved inside a BytesIO buffer.
# This means the video only lives as long as the app is running.
# Returns the filename and status confirmation.
@app.post("/upload_in_memory/")
async def upload_in_memory(file: UploadFile):
    content = await file.read()
    video_store[file.filename] = BytesIO(content)
    return {"filename": file.filename, "status": "stored in memory"}



@app.post("/process_in_memory/{filename}")
async def process_in_memory(filename: str):
    # 1. Get the uploaded video from memory
    video = video_store.get(filename)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found in memory")
    video.seek(0)

    # 2. Create temp files for input and output
    with tempfile.NamedTemporaryFile(suffix=".mp4") as temp_in, \
         tempfile.NamedTemporaryFile(suffix=".mp4") as temp_out:

        # Write the in-memory video to temp input file
        temp_in.write(video.read())
        temp_in.flush()

        # 3. Process the video using MediaPipeVideoProcessor
        processor = MediaPipeVideoProcessor()
        processor.process_video(temp_in.name, temp_out.name)

        # 4. Read the processed video into a BytesIO buffer
        temp_out.seek(0)
        processed_bytes = temp_out.read()
        processed_buffer = BytesIO(processed_bytes)

    # 5. Return the processed video as a streaming response
    processed_buffer.seek(0)
    return StreamingResponse(processed_buffer, media_type="video/mp4")


@app.get("/verdict", response_class=JSONResponse)
async def get_verdict(path: str):
    processor = MediaPipeVideoProcessor()
    return processor.verdict(path)

@app.post("/process_video/")
async def process_video(file: UploadFile = File(...)):
    # Save uploaded file to a temp file
    with tempfile.NamedTemporaryFile(suffix=".mp4") as temp_in, \
         tempfile.NamedTemporaryFile(suffix=".mp4") as temp_out:
        temp_in.write(await file.read())
        temp_in.flush()

        # Process video
        processor = MediaPipeVideoProcessor()
        processor.process_video(temp_in.name, temp_out.name)

        # Return processed video as a stream
        temp_out.seek(0)
        return StreamingResponse(BytesIO(temp_out.read()), media_type="video/mp4")


#@app.post("/verdict/")
#async def get_verdict(input_path: str):
#    return MediaPipeVideoProcessor.verdict(input_path)


# GET ----------------------------------------------------------------------

# 🌐 GET endpoint to serve a basic HTML page that embeds the uploaded video.
# This can be used to visually test whether the uploaded video is viewable in the browser.
@app.get("/watch/{filename}", response_class=HTMLResponse)
def watch_video_page(filename: str):
    return f"""
    <html>
        <body>
            <h2>Watching: {filename}</h2>
            <video width="640" height="480" controls>
                <source src="/view/{filename}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        </body>
    </html>
    """


# 📺 GET endpoint to stream a video stored in memory by filename.
# Looks up the video BytesIO buffer in the in-memory store and streams it back.
# Raises 404 error if the video is not found in memory.
@app.get("/view_in_memory/{filename}")
def stream_in_memory(filename: str):
    video = video_store.get(filename)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found in memory")
    video.seek(0)  # Reset read pointer to start
    return StreamingResponse(video, media_type="video/mp4")



@app.get("/view_processed/{filename}")
def view_processed_file(filename: str):
    file_path = os.path.join(filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type="video/mp4")



# PUT ----------------------------------------------------------------------



# PATCH ----------------------------------------------------------------------



# DELETE ----------------------------------------------------------------------



# OPTIONS ----------------------------------------------------------------------



# HEAD ----------------------------------------------------------------------

from fastapi import FastAPI
from src.api import video_router, frame_router, inference_router

app = FastAPI(title="My FastAPI App")

# Include the router
app.include_router(frame_router.router)
app.include_router(inference_router.router)
app.include_router(video_router.router)

# Optional: a simple root route
@app.get("/health")
async def health_check():
    return {"status": "OK"}
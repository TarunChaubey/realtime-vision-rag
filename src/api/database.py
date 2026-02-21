from fastapi import APIRouter

# Create a router instance
db_router = APIRouter()

# Example GET route
@db_router.get("/")
async def home():
    return {"message": "Welcome to FastAPI!"}

# Example GET route with path parameter
@db_router.get("/items/{item_id}")
async def get_item(item_id: int):
    return {"item_id": item_id, "name": f"Item {item_id}"}

# Example POST route
@db_router.post("/add_video/")
async def add_video(item: dict):
    return {"message": "Item created", "item": item}
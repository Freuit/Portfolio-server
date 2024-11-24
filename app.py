from fastapi import FastAPI
from notion import router as notion_router

app = FastAPI()

app.include_router(notion_router)

@app.get("/", status_code=204)
async def get_root():
    pass

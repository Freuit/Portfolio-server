from datetime import datetime
from fastapi import APIRouter, Response
from setting import setting
import os
import requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging

router = APIRouter(
    prefix="/notion",
)
scheduler = AsyncIOScheduler()
LOG = logging.getLogger('uvicorn.error')

def key_to_directory(key: str):
    return os.path.join(setting.WORKSPACE, 'notion', key)

def get_notion_file(db_key: str):
    file_directory = key_to_directory(db_key)

    if os.path.isfile(file_directory):
        with open(file_directory, mode="r") as file:
            return file.read()
    else: return None

def download_notion_file(db_key: str):
    response = requests.post(
        url=f'https://api.notion.com/v1/databases/{db_key}/query',
        headers = {
            'Notion-Version': '2022-06-28',
            'Authorization': 'Bearer ' + setting.NOTION_KEY
        }
    )

    file_directory = key_to_directory(db_key)
    with open(file_directory, mode="w") as file:
        file.write(response.text)


@router.get('/projects')
async def getNotionProjects():
    content = get_notion_file(setting.NOTION_PROJECT_KEY)
    if content is None:
        return Response(status_code=400)
    else:
        return Response(status_code=200, content=content, media_type="application/json")

@router.get('/skills')
async def getNotionSkills():
    content = get_notion_file(setting.NOTION_SKILL_KEY)
    if content is None:
        return Response(status_code=400)
    else:
        return Response(status_code=200, content=content, media_type="application/json")

@scheduler.scheduled_job('interval', minutes=30, 
                        next_run_time= None if setting.isdev else datetime.now())
                        # next_run_time=datetime.now())
async def fetch_notion_data():
    download_notion_file(setting.NOTION_PROJECT_KEY)
    download_notion_file(setting.NOTION_SKILL_KEY)
    LOG.info("NOTION FETCHING COMPLETE")

scheduler.start()
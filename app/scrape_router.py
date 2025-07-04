from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
import httpx
from datetime import datetime, timezone
from bs4 import BeautifulSoup
import validators
from .dependencies import get_db
from .schemas import ScrapeRequest, Log as LogSchema
from .models import Log as LogModel


scrape_router = APIRouter( prefix='/scrape' )

async def get_html_document(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text
    
async def create_log( log:dict, db:Session = Depends(get_db)):

    new_log = LogModel(
        url = log["url"],
        timestamp = log["timestamp"],
        status_code = log["status_code"],
    )

    db.add(new_log)
    db.commit()
    db.refresh(new_log)

def normalize_url(url: str) -> str:
    if not url.startswith(('http://', 'https://')):
        return 'https://' + url
    return url


@scrape_router.post('/url')
async def scrape_url(payload: ScrapeRequest, db:Session = Depends(get_db)):
    url_string = normalize_url(payload.url)

    if not validators.url(url_string):
        raise HTTPException(400, detail='Url is not valid!')

    html = await get_html_document(url_string)

    soup = BeautifulSoup(html, 'html.parser')

    title_tag = soup.title
    title_string = title_tag.string.strip() if title_tag and title_tag.string else "No title found"

    new_log: dict = {
        "url": url_string,
        "timestamp": str(datetime.now(timezone.utc)),
        "status_code": 200
        }
    
    await create_log( log=new_log, db=db)

    return  {
                "title": title_string,
                "status_code": 200,
                "url": url_string
            }




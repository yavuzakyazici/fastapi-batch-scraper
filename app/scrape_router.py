from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
import httpx, uuid, asyncio
from datetime import datetime, timezone
from bs4 import BeautifulSoup
import validators
from .dependencies import get_db
from .schemas import ScrapeRequest, Log as LogSchema, BatchScrapeRequests
from .models import Log as LogModel, ScrapeResult

scrape_router = APIRouter(prefix='/scrape')


def normalize_url(url: str) -> str:
    if not url.startswith(('http://', 'https://')):
        return 'https://' + url
    return url


async def get_html_document(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text


async def create_log(log: dict, db: Session):
    new_log = LogModel(
        url=log["url"],
        timestamp=log["timestamp"],
        status_code=log["status_code"],
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)


async def scrape_url(payload: ScrapeRequest, db: Session):
    url_string = normalize_url(payload.url)

    if not validators.url(url_string):
        raise HTTPException(400, detail='Url is not valid!')

    html = await get_html_document(url_string)

    soup = BeautifulSoup(html, 'html.parser')
    title_tag = soup.title
    title_string = title_tag.string.strip() if title_tag and title_tag.string else "No title found"

    new_log = {
        "url": url_string,
        "timestamp": str(datetime.now(timezone.utc)),
        "status_code": 200
    }

    await create_log(log=new_log, db=db)

    return {
        "title": title_string,
        "status_code": 200,
        "url": url_string
    }


async def store_scrape_result(batch_id: str, scrape_request: ScrapeRequest, db: Session):
    try:
        result = await scrape_url(scrape_request, db)
        now = datetime.now(timezone.utc)

        scrape_result = ScrapeResult(
            batch_id=batch_id,
            url=result["url"],
            title=result["title"],
            status_code=result["status_code"],
            timestamp=str(now)
        )

        db.add(scrape_result)
        db.commit()
        db.refresh(scrape_result)

    except Exception as e:
        print(f"[store_scrape_result] Failed for URL {scrape_request.url}: {e}")


@scrape_router.post('/url')
async def scrape_single_url(payload: ScrapeRequest, db: Session = Depends(get_db)):
    return await scrape_url(payload, db)


@scrape_router.post('/request_batch')
async def scrape_batch_url(batch: BatchScrapeRequests, db: Session = Depends(get_db)):
    if not batch.requests:
        raise HTTPException(400, detail="Batch cannot be empty")

    batch_id = str(uuid.uuid4())

    for url in batch.requests:
        scrape_request = ScrapeRequest(url=str(url))
        asyncio.create_task(store_scrape_result(batch_id, scrape_request, db))

    return {
        "batch_id": batch_id
    }

@scrape_router.get('/results/{batch_id}')
async def get_batch_results(batch_id: str, db: Session = Depends(get_db)):
    results = db.query(ScrapeResult).filter(ScrapeResult.batch_id == batch_id).all()

    if not results:
        raise HTTPException(404, detail="No results found for this batch_id")

    return {
        "batch_id": batch_id,
        "results": [
            {
                "url": result.url,
                "title": result.title,
                "status_code": result.status_code,
                "timestamp": result.timestamp
            } for result in results
        ]
    }

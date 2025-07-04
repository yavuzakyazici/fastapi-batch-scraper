# FastAPI Batch Scraper

A fully asynchronous batch web scraping API built with **FastAPI**, **httpx**, and **SQLAlchemy**.

This service lets you submit a batch of URLs, scrape their HTML titles in the background, and retrieve the results by `batch_id`.

![Scrape Request](.app/assets/scrape_request.png)
![Scrape Response](.app/assets/scrape_response.png)
![Batch Scrape Request](.app/assets/batch_scrape_request.png)
![Batch Scrape Response](.app/assets/batch_scrape_response.png)

---

## 🚀 Features

- ✅ Submit a **batch of URLs** to be scraped
- ✅ **Extract `<title>`** tags from web pages
- ✅ Background scraping using `asyncio.create_task()` (no duplication of logic)
- ✅ Store and retrieve results from **SQLite** using SQLAlchemy
- ✅ API endpoints for submitting and retrieving results
- ✅ Full **async/await** support with `httpx.AsyncClient`
- ✅ URL validation and normalization included

---

## 🔧 Tech Stack

- FastAPI
- httpx (for async HTTP requests)
- SQLAlchemy + SQLite
- Pydantic
- BeautifulSoup (for HTML parsing)

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/fastapi-batch-scraper.git
cd fastapi-batch-scraper
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
````

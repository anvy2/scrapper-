# Steps to run
1. Install requirements.txt in a virtual environment.
2. Run a local Redis server, reachable at localhost:6379.
3. To run the app:
   If using uv for package management, use `uv run uvicorn src.main:app --reload --loop uvloop`.
   Otherwise, activate the virtual environment and use `uvicorn src.main:app --reload --loop uvloop` from the project root.

The src/scrapper directory contains all the scraper code, and the project uses bs4 for HTML parsing and httpx as an asynchronous HTTP client. More scrapers can be added to the same directory. Currently, the price does not include the currency indicator and only shows the value. In the local file, the Indian currency symbol is rendered as Unicode for readability. However, it is an easy change if currency indication is needed.

Selenium is not included in the project, and the website seems to use SSR, which returns HTML and not JS.

The src/redis.py file contains the Redis initialization code and is designed to work with FastAPI dependency injection. If, in another scenario, it needs to be used outside a FastAPI context where FastAPI dependency injection cannot be used, a different package, fast_depends, is already present in the project.  This package provides FastAPI-compatible dependency injection but can be used outside of FastAPI handler scope.

The src/notification directory contains an abstract base class in __init__.py that can be used in any other notification implementation.  For this project, a console notification is used, printing data to the console after scraping is complete.

The src/storage directory contains an abstract base class in __init__.py that can be used in any other storage implementation.  It stores the scraped data in a specific format specified in the project requirements.  The project scope is local file storage.

The src/object_storage also follows the same structure. It is used to store objects, which can be images, videos, or any other files. Currently, only a local storage implementation is given, but this can be extended with other implementations, such as for S3, MinIO, etc.

The static API key used is `1234` and is declared in `src/dependencies.py`.  For now, it is hardcoded in the project, but it can also be provided via environment variables.

The simple retry mechanism is in src/decorators and is supposed to be used as a decorator.  It includes the number of retries and the delay (in seconds) for each retry, and an option for specifying exceptions. This defaults to all exceptions; the retry will only be triggered if the specified exception is encountered.

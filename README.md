# Steps to run

1. Install requirements.txt in a virtual env
2. Run a local redis-server which should be reachable at localhost:6379
3. To run the app
   If using uv for package management, then use `uv run uvicorn src.main:app --reload --loop uvloop`
   else activate the virtual env and use `uvicorn src.main:app --reload --loop uvloop` from the project root

The src/scrapper directory contains all the scrapper code and the project uses bs4 for html parsing and httpx as async http client. More scrapper can be added in a same directory. Currently the price does not include the currency indicator and only shows the value. As in local file, the indian currency symbol is rendered as unicode so it is done for readability purpose. But it's an easy change if the currently indication needs to be used.

Selenium is not included in the project and the website seem to return SSR which returns html and not js.

The src/redis.py contains the redis initialisation code and is made to work with fastapi dependency injection. If in other scenario, it needs to be used outside of fastapi context where we can't use fastapi dependecy injection then a different package is already present in the project fast_depends which provide fastapi compatible dependency inject but can be used outside of fastapi handler's scope.

The src/notification contains an abstract base class in **init**.py which can be used in any other notification implementation. As for the scope of the project a console notification is used which prints data to console once the scrapping is done.

The src/storage contains an abstract base class in **init**.py which can be used in any other storage implementation. It stores the scrapped data in a specific format specified in project requirements. As for the scope of the project local file storage.

The src/object_storage also follows the same structure. It is used to store objects which can be images, videos or any other files. Currently, only local storage implementation is given but again can be extended with other implementations like for s3, minio etc

The static api key used is `1234` and is declared in src/dependencies.py. For now it is hardcoded in the project but can be given from env as well.

The simple retry mechanism is in src/decorators and are supposed to be used as decorators. It includes number of retries and the delay (in seconds) for each retry and option for specifying exceptions which defaults to all Exceptions and the retry will only be triggered if the specified exception is encountered.

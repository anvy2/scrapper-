# Steps to run

1. Install requirements.txt in a virtual env
2. Run a local redis-server which should be reachable at localhost:6379
3. To run the app
   If using uv for package management, then use `uv run uvicorn src.main:app --reload --loop uvloop`
   else activate the virtual env and use `uvicorn src.main:app --reload --loop uvloop` from the project root

from APP import app
import os
from dotenv import load_dotenv


load_dotenv()

host = os.getenv("HOST")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=host, port=8080)

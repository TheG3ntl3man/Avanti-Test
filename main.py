import os

from dotenv import load_dotenv

from app.app import create_app

load_dotenv(verbose=True)


app = create_app(os.getenv("FLASK_ENV"))

if __name__ == '__main__':
    app.run(debug="on")

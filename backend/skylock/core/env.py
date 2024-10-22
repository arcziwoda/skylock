import dotenv
import os


dotenv.load_dotenv()

JWT_SECRET = os.environ["JWT_SECRET"]
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/db.sqlite")

import dotenv
import os


dotenv.load_dotenv()

JWT_SECRET = os.getenv(
    "JWT_SECRET", "test_token"
)  # test_token used in tests only, normally always override with env
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/db.sqlite")

from env_loading import ENV

DB_HOST = ENV.get("DB_HOST")
DB_PORT = ENV.get("DB_PORT")
DB_USER = ENV.get("DB_USER")
DB_PASSWORD = ENV.get("DB_PASSWORD")
DB_NAME = ENV.get("DB_NAME")

def get_dburl() -> str:
    return f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
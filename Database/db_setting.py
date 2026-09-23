DB_HOST = "192.168.0.9"
DB_PORT = 5432
DB_USER = "debian"
DB_PASSWORD = "debian"
DB_NAME = "test"

def get_dburl() -> str:
    return f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
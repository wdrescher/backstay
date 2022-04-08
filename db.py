from databases import Database, DatabaseURL

# uri = f"mysql://{settings.db_username}:{settings.db_password}@{settings.db_url}/{settings.db_db}"
# uri = f"{settings.db_username}:{settings.db_password}@{settings.db_url}/{settings.db_db}"

database = Database(DatabaseURL("user:password@localhost:33061/db"))
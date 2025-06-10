import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

DATABASE_URL = (
    "postgresql+asyncpg://ubydtzfq76agbyx9yxwr:XIiqD55NfbI6HMVOkWJWdUNSquwC4c@"
    "btng9poyhgttpjvdekzs-postgresql.services.clever-cloud.com:50013/"
    "btng9poyhgttpjvdekzs"
)

engine = create_async_engine(DATABASE_URL, echo=True)

async def run_alter():
    async with engine.begin() as conn:
        # Artista
        await conn.execute(text("ALTER TABLE artistadb ADD COLUMN IF NOT EXISTS eliminado BOOLEAN DEFAULT FALSE"))
        await conn.execute(text("ALTER TABLE artistadb ADD COLUMN IF NOT EXISTS imagen_url VARCHAR"))
        await conn.execute(text("ALTER TABLE artistadb ADD COLUMN IF NOT EXISTS imagen_bytes BYTEA"))
        # Canción
        await conn.execute(text("ALTER TABLE canciondb ADD COLUMN IF NOT EXISTS eliminado BOOLEAN DEFAULT FALSE"))
        await conn.execute(text("ALTER TABLE canciondb ADD COLUMN IF NOT EXISTS imagen_url VARCHAR"))
        await conn.execute(text("ALTER TABLE canciondb ADD COLUMN IF NOT EXISTS imagen_bytes BYTEA"))
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(run_alter())
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

def get_async_engine(user, password, host, port, database):
    url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
    engine = create_async_engine(url, echo=True)  # echo=True logs SQL
    return engine

def get_async_session(user, password, host, port, database):
    engine = get_async_engine(user, password, host, port, database)
    AsyncSessionLocal = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    return AsyncSessionLocal

def get_async_engine_session(user, password, host, port, database):
    engine = create_async_engine(
        f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}",
        echo=True,
    )
    AsyncSessionLocal = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    return engine, AsyncSessionLocal

# import asyncio

# async def main():
#     # Create a dynamic session
#     AsyncSessionLocal = get_async_session(
#         user="postgres",
#         password="mypassword",
#         host="localhost",
#         port=5432,
#         database="mydb"
#     )
    
#     async with AsyncSessionLocal() as session:
#         result = await session.execute("SELECT version();")
#         version = result.fetchone()
#         print("PostgreSQL version:", version[0])

# asyncio.run(main())
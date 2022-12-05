from app.endpoints import endpoints

async def get_db():
    async_session = endpoints.postgres.session()
    try:
        yield async_session
    finally:
        await async_session.close()
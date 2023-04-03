import httpx
from fastapi import status, HTTPException
from sqlalchemy.orm import Session

# import asyncio

from app.sql.crud import create_beer, create_hop
from app.sql.database import SessionLocal, engine
from app.sql import models
from app.schemas import Beer, Hop


# models.Base.metadata.create_all(bind=engine)
#
# session = SessionLocal()

async def punk_request(page: int) -> dict:
    """
    HTTP requests to fetch all beer data from Punk API
    :return: a list of all beers
    """
    url = f"https://api.punkapi.com/v2/beers?page={page}&per_page=80"
    async with httpx.AsyncClient() as client:
        response = await client.get(url=url)

    if not response.status_code == 200:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Failed to fetch data from the PunkAPI'
        )
    beers = response.json()
    return beers


# async def punk_request(db: Session) -> None:
#     """
#     HTTP requests to fetch all beer data from Punk API
#     :return: a list of all beers
#     """
#     for page in range(1, 6):
#         url = f"https://api.punkapi.com/v2/beers?page={page}&per_page=80"
#         async with httpx.AsyncClient() as client:
#             response = await client.get(url=url)
#
#         if response.status_code == 200:
#             beers = response.json()
#             for beer in beers:
#                 if beer.get("method").get("fermentation").get("temp").get(
#                         "value") is not None:
#                     new_beer: Beer = Beer(
#                         id=beer.get("id"),
#                         name=beer.get("name"),
#                         fermentation_temp=beer.get("method").get(
#                             "fermentation").get("temp").get("value")
#                     )
#                     # print(new_beer)
#                     create_beer(db=db, beer=new_beer)
#                     # session.add(models.Beer(**new_beer.dict()))
#                     # session.commit()
#
#                 hops = beer.get("ingredients").get("hops")
#                 for hop in hops:
#                     if hops is not None:
#                         new_hop: Hop = Hop(
#                             name=hop.get("name"),
#                             amount=hop.get("amount").get("value"),
#                             add=hop.get("add"),
#                             attribute=hop.get("attribute"),
#                             beer_id=beer.get("id")
#                         )
#                         # print(new_hop)
#                         create_hop(db=db, hop=new_hop)
#                         # session.add(models.Hop(**new_hop.dict()))
#                         # session.commit()
#
#         else:
#             print('Failed to fetch data from the PunkAPI')


# loop = asyncio.get_event_loop()
# loop.run_until_complete(punk_request())
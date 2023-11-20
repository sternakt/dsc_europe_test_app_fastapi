from fastapi import Depends, FastAPI
from typing_extensions import Annotated
from pydantic import BaseModel, Field

from faststream.kafka import KafkaBroker, fastapi

router = fastapi.KafkaRouter("localhost:9092")

app = FastAPI(lifespan=router.lifespan_context)


class Name(BaseModel):
    name: str = Field(..., description="Name of the person")

def broker():
    return router.broker

to_names = router.broker.publisher(
    "names",
    description="Produces a message on names after receiving a post on name endpoint",
)

@router.get("/")
async def hello_http():
    return "Hello from HTTP"

@router.post("/name/")
async def post_name(name: Name, broker: Annotated[KafkaBroker, Depends(broker)]):
    await broker.publish(name, "names")
    return name


app.include_router(router)

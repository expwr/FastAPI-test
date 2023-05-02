from enum import Enum

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field

app = FastAPI(
    title="Noah's cards and candy",
    description="This store will help you get all of your candy and cards that you could ever want",
    version="0.1.0",
)

# This class is going to be used to create the categories to be able to sort through different sections
class Category(Enum):
    """Category of an item"""
    CANDY = "candy"
    CARDS = "cards"

# This class sets the "base model" of the items that are in the category
class Item(BaseModel):
    name: str = Field(description="Name of the item")
    price: float = Field(description="Price of the item")
    count: int = Field(description="Number of the items")
    id: int = Field(description="Id of the item")
    category: Category = Field(description="Category of the item")


# These are a dict of sample items to be used in the example
items = {
    0: Item(name="Chocolate_bar", price=1.99, count=50, id=0, category=Category.CANDY),
    1: Item(name="Payday_bar", price=3.99, count=5, id=1, category=Category.CANDY),
    2: Item(name="Charizard", price=25.99, count=100, id=1, category=Category.CARDS)
}


# FastAPI handles the JSON serialization and deserialization. This means it has built in object->string and string->object 
@app.get("/")
def index() -> dict[str, dict[int, Item]]:
    return {"items": items}

@app.get("/items/{item_id}")
def query_item_by_id(item_id: int) -> Item:
    if item_id not in items:
        raise HTTPException(status_code=404, detail=f"Item with {item_id=} does not exist.")
    return items[item_id]

# Dict containing the users query arguments
Selection = dict[
    str, str | int | float | Category | None
] 

@app.get("/items/")
def query_item_by_parameters(
    name: str | None = None, 
    price: float | None = None,
    count: int | None = None,
    category: Category | None = None,
) -> dict[str, Selection | list[Item]]:
    def check_item(item: Item) -> bool:
        return all(
            (
            name is None or item.name == name,
            price is None or item.price == price,
            count is None or item.count != count,
            category is None or item.category is category
            )
        )
    selection = [item for item in items.values() if check_item(item)]
    return {
        "query": {"name": name, "price": price, "count": count, "category": category},
        "selection": selection,
    }

@app.post("/")
def add_item(item: Item) -> dict[str, Item]:

    if item.id in items:
        HTTPException(status_code=400, detail=f"Item with {item.id} already exists.")

    items[item.id] = item
    return {"added": item}

@app.put("/update/{item_id}",
         # Allows specifying of error codes
         responses={
             404: {"description": "Item not found"},
             400: {"description": "No arguments specified"}
         }
         )
def update(
    item_id: int = Path(ge=0, title="Item ID", description="Unique int that specifies an item."),
    name: str | None = Query(default=None, min_length=1, max_length=8, title="Name", description="New name for the item."),
    price: float | None = Query(default=None, gt=0.0, title="Price", description="Price for the item"),
    count: int | None = Query(default=None, ge=0, title="Count", description="Count of the item"),
) -> dict[str, Item]:

    if item_id not in items:
        HTTPException(status_code=404, detail=f"Item with {item_id} does not exist.")
    if all(info is None for info in (name, price, count)):
        raise HTTPException(
            status_code=400, detail=f"No parameters provided for update."
        )
    
    item = items[item_id]
    if name is not None:
        item.name = name
    if price is not None:
        item.price = price
    if count is not None:
        item.count = count

    return {"updated": item}

@app.delete("/delete/{item_id}")
def delete_item(item_id: int) -> dict[str, Item]:

    if item_id not in items:
        raise HTTPException(
            status_code=404, detail=f"Item with {item_id} does not exist."
        )
    
    item = items.pop(item_id)
    return {"deleted": item}
from fastapi import APIRouter

router = APIRouter(prefix="/products",
                   tags= ["products"],
                   responses={404: {"message": "No encontrado"}})

products = ["Porducto 1", "Porducto 2",
            "Porducto 3", "Porducto 4", "Porducto 5"]


@router.get("/")
async def get_products():
    return products


@router.get("/{id}")
async def get_products(id_product: int):
    return products[id]

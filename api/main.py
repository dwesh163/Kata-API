from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from db import execute_query  # Assuming execute_query function is imported from db module

app = FastAPI()

# Modèle Pydantic pour représenter une bière
class Beer(BaseModel):
    id: Optional[int] = None
    brewery_id: Optional[int] = None
    name: Optional[str] = None
    cat_id: Optional[int] = None
    style_id: Optional[int] = None
    abv: Optional[float] = None
    ibu: Optional[float] = None
    srm: Optional[float] = None
    upc: Optional[int] = None
    filepath: Optional[str] = None
    descript: Optional[str] = None
    add_user: Optional[int] = None

    class Config:
        orm_mode = True

# Endpoints CRUD pour les bières
@app.post("/beer", response_model=Beer)
async def add_beer(beer: Beer):
    insert_query = """
        INSERT INTO beers (brewery_id, name, cat_id, style_id, abv, ibu, srm, upc, filepath, descript, add_user)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
    """
    result = execute_query(insert_query, (
        beer.brewery_id, beer.name, beer.cat_id, beer.style_id, beer.abv,
        beer.ibu, beer.srm, beer.upc, beer.filepath, beer.descript, beer.add_user
    ))
    beer.id = result[0]['id']  # Assuming execute_query returns a list of dicts with 'id' field
    return beer

@app.get("/beers", response_model=List[Beer])
async def get_beers():
    select_query = "SELECT * FROM beers;"
    results = execute_query(select_query)
    return results

@app.get("/beer/{id}", response_model=Beer)
async def get_beer(id: int):
    select_query = "SELECT * FROM beers WHERE id = %s"
    result = execute_query(select_query, (id,))
    if not result:
        raise HTTPException(status_code=404, detail="Beer not found")
    return result[0]

@app.put("/beer/{id}", response_model=Beer)
async def update_beer(id: int, beer: Beer):
    update_query = """
        UPDATE beers
        SET brewery_id = %s, name = %s, cat_id = %s, style_id = %s, abv = %s,
            ibu = %s, srm = %s, upc = %s, filepath = %s, descript = %s, add_user = %s
        WHERE id = %s
        RETURNING *;
    """
    result = execute_query(update_query, (
        beer.brewery_id, beer.name, beer.cat_id, beer.style_id, beer.abv,
        beer.ibu, beer.srm, beer.upc, beer.filepath, beer.descript, beer.add_user, id
    ))
    if not result:
        raise HTTPException(status_code=404, detail="Beer not found")
    return result[0]

@app.patch("/beer/{id}", response_model=Beer)
async def partial_update_beer(id: int, beer: Beer):
    # Fetch existing beer data if needed
    select_query = "SELECT * FROM beers WHERE id = %s"
    existing_beer = execute_query(select_query, (id,))
    
    # Prepare update query and parameters based on changes
    update_fields = {}
    for field, value in beer.dict(exclude_unset=True).items():
        update_fields[field] = value
    
    if not update_fields:
        raise HTTPException(status_code=400, detail="No valid fields provided for update")
    
    update_query = f"""
        UPDATE beers
        SET {', '.join(f"{field} = %s" for field in update_fields.keys())}
        WHERE id = %s
        RETURNING *;
    """
    print(update_query)
    params = list(update_fields.values())
    params.append(id)
    result = execute_query(update_query, tuple(params))
    if not result:
        raise HTTPException(status_code=404, detail="Beer not found")
    return result[0]

@app.delete("/beer/{id}", response_model=dict)
async def delete_beer(id: int):
    delete_query = "DELETE FROM beers WHERE id = %s"
    result = execute_query(delete_query, (id,))
    if not result:
        raise HTTPException(status_code=404, detail="Beer not found")
    return {"message": "Beer data deleted successfully"}

# /breweries 	Affiche toutes les brasseries 	GET
@app.get("/breweries")
async def get_breweries():
    select_query = "SELECT * FROM breweries"
    return execute_query(select_query)

# /brewerie/{id} 	Affiche la brasserie {id} 	GET
@app.get("/brewery/{id}")
async def get_brewery(id: int):
    select_query = "SELECT * FROM breweries WHERE id = %s"
    return execute_query(select_query, (id,))

# /categories 	Affiche toutes les catégories 	GET
@app.get("/categories")
async def get_categories():
    select_query = "SELECT * FROM categories"
    return execute_query(select_query)

# /categorie/{id} 	Affiche la catégorie {id} 	GET
@app.get("/category/{id}")
async def get_category(id: int):
    select_query = "SELECT * FROM categories WHERE id = %s"
    return execute_query(select_query, (id,))

# /styles 	Affiche toutes les styles 	GET
@app.get("/styles")
async def get_styles():
    select_query = "SELECT * FROM styles"
    return execute_query(select_query)

# /style/{id} 	Affiche le style {id} 	GET
@app.get("/style/{id}")
async def get_style(id: int):
    select_query = "SELECT * FROM styles WHERE id = %s"
    return execute_query(select_query, (id,))

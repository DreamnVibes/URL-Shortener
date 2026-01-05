from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random 
import string

app = FastAPI()

# In-memory database for storing URLs (will replace with sqlite current db in ram volatile)
db = {}

#schema
class URLCreate(BaseModel):
    target_url: str

#helper
def generate_key(length = 5):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length)) 

#Endpoint A - Create short link
@app.post("/url")
def create_url(item: URLCreate):
    key = generate_key()

    #checking for collision
    while key in db:
        key = generate_key()
    
    db[key] = item.target_url #save to volatile db

    #result return
    return {
        "key": key,
        "short_url": f"http://localhost:8000/{key}",
        "target_url": item.target_url
    }

#Endpoint B - Redirect to original
from fastapi.responses import RedirectResponse
@app.get("/{key}")
def redirect_to_url(key: str):
    if key in db:
        long_url = db[key]
        return RedirectResponse(url=long_url, status_code=302)
    else:
        raise HTTPException(status_code=404, detail="URL not found")

#GET needs to be fixed  


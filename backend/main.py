from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from config import settings
from search.engine import SearchEngine

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize search engine
search_engine = SearchEngine()

class SearchQuery(BaseModel):
    query: str
    limit: Optional[int] = None

class CodeSnippet(BaseModel):
    code: str

class SearchResponse(BaseModel):
    results: List[dict]

# Include routers
# app.include_router(code_search.router, prefix=settings.API_V1_STR)
# app.include_router(auth.router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Welcome to AI Code Search API"}

@app.post("/search", response_model=SearchResponse)
async def search_code(query: SearchQuery):
    try:
        results = search_engine.search(query.query, k=query.limit)
        return {
            "results": [
                {"code": code, "score": float(score)} 
                for code, score in results
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/add-code")
async def add_code(snippet: CodeSnippet):
    try:
        search_engine.add_code([snippet.code])
        return {"message": "Code snippet added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/save-index")
async def save_index():
    try:
        search_engine.save_index()
        return {"message": "Index saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)
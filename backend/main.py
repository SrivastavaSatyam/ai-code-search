from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import traceback
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
        print(f"Error in search: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/add-code")
async def add_code(snippet: CodeSnippet):
    try:
        if not snippet.code or len(snippet.code.strip()) == 0:
            raise ValueError("Code snippet cannot be empty")
        
        # Add more detailed logging    
        print(f"Adding code snippet: {snippet.code[:100]}...")
        
        # Try to add the code with better error handling
        try:
            search_engine.add_code([snippet.code])
            return {"message": "Code snippet added successfully"}
        except Exception as inner_e:
            # Log the specific error from the search engine
            print(f"Search engine error: {str(inner_e)}")
            print(traceback.format_exc())
            
            # Return a more specific error message
            raise HTTPException(
                status_code=500, 
                detail=f"Error in search engine: {str(inner_e)}"
            )
    except Exception as e:
        print(f"Error in add-code: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/save-index")
async def save_index():
    try:
        search_engine.save_index()
        return {"message": "Index saved successfully"}
    except Exception as e:
        print(f"Error in save-index: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/load-index")
async def load_index():
    try:
        search_engine.load_index()
        return {"message": "Index Loaded Successfully"}
    except Exception as e:
        print(f"Error while Loading Index {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

from server import mcp

EXPECTED_TOKEN = os.getenv("MCP_TOKEN", "")
security = HTTPBearer(auto_error=False)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not EXPECTED_TOKEN:
        return True
    
    if not credentials or credentials.credentials != EXPECTED_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    
    return True

# Create an mcp Endpoint
mcp_app = mcp.http_app(path="/mcp")

# Create the main app with FastAPI
app = FastAPI(lifespan=mcp_app.lifespan)

@app.get("/")
def health_check():
    return {"status": "ok", "service": "gnomAD MCP Remote", "transport": "HTTP Streamable"}

# 4. Montamos la aplicación MCP en FastAPI, protegiéndola con el token
app.mount("/", mcp_app)

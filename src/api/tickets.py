import os
import httpx
from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api/v1/tickets", tags=["Tickets"])

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_API_URL = "https://api.github.com"

class TicketBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=10)
    priority: str = Field("medium", pattern="^(low|medium|high|critical)$")
    category: str = Field("general", pattern="^(general|bug|feature|support)$")

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    status: Optional[str] = Field(None, pattern="^(open|closed)$")
    priority: Optional[str] = Field(None, pattern="^(low|medium|high|critical)$")
    note: Optional[str] = None

class Ticket(TicketBase):
    id: str
    status: str
    created_at: str
    updated_at: str
    url: Optional[str] = None

def get_headers():
    if not GITHUB_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="GitHub token not configured"
        )
    return {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

async def create_github_issue(ticket: TicketCreate) -> dict:
    if not GITHUB_REPO:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="GitHub repository not configured"
        )
        
    url = f"{GITHUB_API_URL}/repos/{GITHUB_REPO}/issues"
    labels = [f"priority:{ticket.priority}", f"category:{ticket.category}"]
    
    payload = {
        "title": ticket.title,
        "body": ticket.description,
        "labels": labels
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=get_headers())
        
    if response.status_code != 201:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"GitHub API Error: {response.text}"
        )
        
    return response.json()

async def list_github_issues(state: str = "open") -> List[dict]:
    if not GITHUB_REPO:
        return []
        
    url = f"{GITHUB_API_URL}/repos/{GITHUB_REPO}/issues"
    params = {"state": state}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=get_headers())
        
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"GitHub API Error: {response.text}"
        )
        
    return response.json()

async def get_github_issue(issue_number: str) -> dict:
    if not GITHUB_REPO:
        raise HTTPException(status_code=503, detail="GitHub repo not configured")
        
    url = f"{GITHUB_API_URL}/repos/{GITHUB_REPO}/issues/{issue_number}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=get_headers())
        
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"GitHub API Error: {response.text}"
        )
        
    return response.json()

async def update_github_issue(issue_number: str, update: TicketUpdate) -> dict:
    if not GITHUB_REPO:
        raise HTTPException(status_code=503, detail="GitHub repo not configured")
        
    url = f"{GITHUB_API_URL}/repos/{GITHUB_REPO}/issues/{issue_number}"
    payload = {}
    
    if update.status:
        payload["state"] = update.status
        
    if update.priority:
        # We need to fetch current labels first to preserve others
        current_issue = await get_github_issue(issue_number)
        current_labels = [l["name"] for l in current_issue.get("labels", [])]
        # Remove old priority labels
        new_labels = [l for l in current_labels if not l.startswith("priority:")]
        new_labels.append(f"priority:{update.priority}")
        payload["labels"] = new_labels

    if not payload:
        return await get_github_issue(issue_number)

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, json=payload, headers=get_headers())
        
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"GitHub API Error: {response.text}"
        )
        
    return response.json()

def map_issue_to_ticket(issue: dict) -> Ticket:
    labels = issue.get("labels", [])
    priority = "medium"
    category = "general"
    
    for label in labels:
        name = label["name"]
        if name.startswith("priority:"):
            priority = name.split(":")[1]
        elif name.startswith("category:"):
            category = name.split(":")[1]
            
    return Ticket(
        id=str(issue["number"]),
        title=issue["title"],
        description=issue.get("body") or "",
        priority=priority,
        category=category,
        status=issue["state"],
        created_at=issue["created_at"],
        updated_at=issue["updated_at"],
        url=issue["html_url"]
    )

@router.post("/", response_model=Ticket, status_code=status.HTTP_201_CREATED)
async def create_ticket(ticket: TicketCreate):
    issue = await create_github_issue(ticket)
    return map_issue_to_ticket(issue)

@router.get("/", response_model=List[Ticket])
async def list_tickets(status: str = "open"):
    issues = await list_github_issues(status)
    return [map_issue_to_ticket(issue) for issue in issues]

@router.get("/{ticket_id}", response_model=Ticket)
async def get_ticket(ticket_id: str):
    issue = await get_github_issue(ticket_id)
    return map_issue_to_ticket(issue)

@router.patch("/{ticket_id}", response_model=Ticket)
async def update_ticket(ticket_id: str, update: TicketUpdate):
    issue = await update_github_issue(ticket_id, update)
    return map_issue_to_ticket(issue)

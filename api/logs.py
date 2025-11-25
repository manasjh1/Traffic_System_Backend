from fastapi import APIRouter, Query
from database.supabase_client import supabase_select

router = APIRouter()

@router.get("/logs/")
def get_logs(limit: int = Query(100)):
    logs = supabase_select("traffic_logs", limit)
    
    if not logs:
        return {"message": "No logs found", "count": 0, "logs": []}

    return {
        "message": "Logs fetched successfully",
        "count": len(logs),
        "logs": logs
    }


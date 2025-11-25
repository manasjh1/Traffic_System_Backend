from fastapi import APIRouter
from database.supabase_client import supabase_select
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/stats/")
def get_stats():
    logs = supabase_select("traffic_logs", 5000)  # fetch more for stats

    if not logs:
        return {"message": "No data available"}

    total_events = len(logs)
    helmet_violations = sum(x["violation_type"] == "No Helmet" for x in logs)
    speed_violations = sum(x["violation_type"] == "Overspeeding" for x in logs)
    multiple = sum(x["violation_type"] == "Multiple" for x in logs)
    normal = sum(x["violation_type"] == "Normal" for x in logs)

    today = datetime.now().date()
    today_events = [
        x for x in logs 
        if datetime.fromisoformat(x["created_at"]).date() == today
    ]

    last_week = datetime.now() - timedelta(days=7)
    week_events = [
        x for x in logs
        if datetime.fromisoformat(x["created_at"]) >= last_week
    ]

    # Weekly chart data
    chart_data = {}
    for i in range(7):
        day = today - timedelta(days=i)
        chart_data[str(day)] = 0

    for x in week_events:
        day = datetime.fromisoformat(x["created_at"]).date()
        day = str(day)
        if day in chart_data:
            chart_data[day] += 1

    return {
        "total_events": total_events,
        "total_violations": helmet_violations + speed_violations + multiple,
        "helmet_violations": helmet_violations,
        "speed_violations": speed_violations,
        "multiple_violations": multiple,
        "normal_events": normal,
        "today_events": len(today_events),
        "last_7_days": len(week_events),
        "weekly_chart_data": [{"date": k, "count": v} for k, v in chart_data.items()]
    }


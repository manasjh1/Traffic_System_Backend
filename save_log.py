from database.supabase_client import supabase_insert
import time

def save_log(vehicle_type, speed, helmet_status, violation_type, plate):
    data = {
        "vehicle_type": vehicle_type,
        "speed": speed,
        "helmet_status": helmet_status,
        "violation_type": violation_type,
        "number_plate_uuid": plate,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    return supabase_insert("traffic_logs", data)

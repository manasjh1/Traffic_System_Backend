# College Traffic Monitoring System - Backend

A real-time AI-based traffic monitoring system that automatically detects and logs traffic violations using dual YOLO models, EasyOCR, and Supabase database integration.

## Features

- **Dual YOLO Detection**: Specialized models for vehicle detection and safety compliance
- **Real-time OCR**: License plate text extraction using EasyOCR
- **Speed Monitoring**: Automatic speed calculation and violation detection
- **Admin Dashboard API**: Complete violation management and review system
- **Database Integration**: Supabase PostgreSQL with proper relationships

## System Architecture

```
Video Input → Vehicle Detection (YOLO 1) → Safety Detection (YOLO 2) → OCR → Database
```

## Project Structure

```
traffic-monitoring-backend/
├── main.py                     # FastAPI application entry point
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
├── core/                       # AI processing pipeline
├── database/                   # Database operations
├── api/                        # REST API endpoints
├── utils/                      # Configuration and helpers
├── models/                     # AI model files
└── tests/                      # Backend testing
```

## Database Schema

### Core Tables
- `admin_users` - Admin authentication and management
- `vehicle_entries` - Vehicle entry/exit tracking
- `rule_violations` - Traffic violations with admin review

### Relationships
```sql
admin_users (id) ← rule_violations (reviewed_by)
vehicle_entries (id) ← rule_violations (vehicle_entry_id)
```

## Installation

### Prerequisites
- Python 3.11 (recommended for compatibility)
- Conda or virtual environment
- Supabase account and database

### Setup Environment

```bash
# Create conda environment
conda create -n Traffic_System python=3.11
conda activate Traffic_System

# Clone and navigate to project
cd traffic-monitoring-backend

# Install dependencies
pip install -r requirements.txt

## Usage

### Start the Backend Server

```bash
# Development mode
python main.py

# Or with uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### API Endpoints

#### Authentication
```
POST /api/auth/login           # Admin login
POST /api/auth/logout          # Admin logout
GET  /api/auth/verify          # Verify session
```

#### Traffic Monitoring
```
POST /api/traffic/start        # Start monitoring
GET  /api/vehicles/current     # Vehicles in campus
GET  /api/vehicles/history     # Vehicle history
```

#### Violation Management
```
GET  /api/violations/pending   # Pending violations
PUT  /api/violations/{id}      # Review violation
GET  /api/violations/stats     # Statistics
```

#### Dashboard Data
```
GET  /api/dashboard/summary    # Overview statistics
GET  /api/dashboard/today      # Today's activity
```

## AI Models

### Model Requirements
- `yolo_vehicles.pt` - Vehicle detection model
- `yolo_safety.pt` - Helmet and license plate detection model

### Processing Flow
1. **Vehicle Detection**: YOLO model detects cars and motorcycles
2. **Safety Check**: Second YOLO model checks helmets and plates on vehicle regions
3. **OCR Processing**: EasyOCR extracts license plate text
4. **Speed Calculation**: Movement tracking between frames
5. **Violation Detection**: Business rules applied to determine violations

## Configuration

### System Rules
- Speed limit: 20 km/h (configurable)
- Motorcycle without helmet = violation
- Speed above limit = violation
- Unauthorized vehicle entry = violation

### Performance Settings
- Frame skip rate: Process every 5th frame
- Confidence threshold: 0.5 for detections
- GPU acceleration: Automatic if available

## Troubleshooting

### Common Issues

**Installation Problems**:
- Use Python 3.11 for better package compatibility
- Install PyTorch separately if needed: `pip install torch torchvision`

**Model Loading Errors**:
- Ensure YOLO model files are in `models/` directory
- Check file paths in environment variables

**Database Connection Issues**:
- Verify Supabase URL and key
- Check network connectivity
- Ensure database schema is created

### Logs and Debugging
- Check application logs for errors
- Use debug mode: `DEBUG=true python main.py`
- Monitor API response times
- Check database query performance

## API Documentation

When the server is running, visit:
- API docs: `http://localhost:8000/docs`

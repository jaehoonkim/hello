from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
import time
from typing import Dict, Any

app = FastAPI(
    title="Time API",
    description="현재 날짜와 시간을 제공하는 REST API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_current_time_data() -> Dict[str, Any]:
    """현재 시간 정보를 반환하는 헬퍼 함수"""
    now = datetime.now(timezone.utc)
    local_now = datetime.now()
    
    return {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
        "timestamp": int(time.time()),
        "timezone": "UTC",
        "local_date": local_now.strftime("%Y-%m-%d"),
        "local_time": local_now.strftime("%H:%M:%S"),
        "local_datetime": local_now.strftime("%Y-%m-%d %H:%M:%S")
    }

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {"message": "Time API Service", "version": "1.0.0"}

@app.get("/api/time")
async def get_current_time():
    """현재 시간 정보를 반환합니다."""
    return get_current_time_data()

@app.get("/api/time/{format}")
async def get_time_format(format: str):
    """지정된 형식으로 현재 시간을 반환합니다."""
    now = datetime.now(timezone.utc)
    local_now = datetime.now()
    
    if format == "iso":
        return {
            "format": "iso",
            "utc": now.isoformat(),
            "local": local_now.isoformat()
        }
    elif format == "unix":
        return {
            "format": "unix",
            "timestamp": int(time.time()),
            "milliseconds": int(time.time() * 1000)
        }
    elif format == "korean":
        # 한국어 형식
        weekdays = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
        months = ["1월", "2월", "3월", "4월", "5월", "6월", 
                 "7월", "8월", "9월", "10월", "11월", "12월"]
        
        weekday = weekdays[local_now.weekday()]
        month = months[local_now.month - 1]
        
        # 오전/오후 구분
        hour = local_now.hour
        am_pm = "오전" if hour < 12 else "오후"
        display_hour = hour if hour <= 12 else hour - 12
        if display_hour == 0:
            display_hour = 12
            
        korean_format = f"{local_now.year}년 {month} {local_now.day}일 {weekday} {am_pm} {display_hour}시 {local_now.minute}분 {local_now.second}초"
        
        return {
            "format": "korean",
            "korean": korean_format,
            "date": f"{local_now.year}년 {month} {local_now.day}일",
            "time": f"{am_pm} {display_hour}시 {local_now.minute}분",
            "weekday": weekday
        }
    else:
        raise HTTPException(
            status_code=400, 
            detail=f"지원하지 않는 형식입니다. 사용 가능한 형식: iso, unix, korean"
        )

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy", "timestamp": int(time.time())}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
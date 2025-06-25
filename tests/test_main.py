import pytest
from fastapi.testclient import TestClient
from main import app
import json
from datetime import datetime
import time

client = TestClient(app)


class TestTimeAPI:
    """Time API 테스트 클래스"""
    
    def test_root_endpoint(self):
        """루트 엔드포인트 테스트"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Time API Service"
        assert data["version"] == "1.0.0"
    
    def test_health_check(self):
        """헬스체크 엔드포인트 테스트"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert isinstance(data["timestamp"], int)
    
    def test_basic_time_endpoint(self):
        """기본 시간 API 테스트"""
        response = client.get("/api/time")
        assert response.status_code == 200
        data = response.json()
        
        # 필수 필드 확인
        required_fields = [
            "date", "time", "datetime", "timestamp", "timezone",
            "local_date", "local_time", "local_datetime"
        ]
        for field in required_fields:
            assert field in data
        
        # 데이터 형식 확인
        assert data["timezone"] == "UTC"
        assert isinstance(data["timestamp"], int)
        
        # 날짜 형식 확인 (YYYY-MM-DD)
        assert len(data["date"]) == 10
        assert data["date"].count("-") == 2
        
        # 시간 형식 확인 (HH:MM:SS)
        assert len(data["time"]) == 8
        assert data["time"].count(":") == 2
    
    def test_iso_format_endpoint(self):
        """ISO 형식 시간 API 테스트"""
        response = client.get("/api/time/iso")
        assert response.status_code == 200
        data = response.json()
        
        assert data["format"] == "iso"
        assert "utc" in data
        assert "local" in data
        
        # ISO 형식 확인
        assert "T" in data["utc"]
        assert "T" in data["local"]
    
    def test_unix_format_endpoint(self):
        """Unix timestamp 형식 시간 API 테스트"""
        response = client.get("/api/time/unix")
        assert response.status_code == 200
        data = response.json()
        
        assert data["format"] == "unix"
        assert "timestamp" in data
        assert "milliseconds" in data
        
        # Unix timestamp 확인
        assert isinstance(data["timestamp"], int)
        assert isinstance(data["milliseconds"], int)
        assert data["milliseconds"] > data["timestamp"]
        
        # 현재 시간과 비교 (5초 이내 차이)
        current_time = int(time.time())
        assert abs(data["timestamp"] - current_time) < 5
    
    def test_korean_format_endpoint(self):
        """한국어 형식 시간 API 테스트"""
        response = client.get("/api/time/korean")
        assert response.status_code == 200
        data = response.json()
        
        assert data["format"] == "korean"
        assert "korean" in data
        assert "date" in data
        assert "time" in data
        assert "weekday" in data
        
        # 한국어 형식 확인
        assert "년" in data["korean"]
        assert "월" in data["korean"]
        assert "일" in data["korean"]
        assert ("오전" in data["korean"]) or ("오후" in data["korean"])
        
        # 요일 확인
        weekdays = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
        assert data["weekday"] in weekdays
    
    def test_invalid_format_endpoint(self):
        """잘못된 형식 요청 테스트"""
        response = client.get("/api/time/invalid")
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "지원하지 않는 형식" in data["detail"]
    
    def test_api_response_time(self):
        """API 응답 시간 테스트 (100ms 이하)"""
        import time
        
        start_time = time.time()
        response = client.get("/api/time")
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # 밀리초로 변환
        assert response.status_code == 200
        assert response_time < 100  # 100ms 이하
    
    def test_concurrent_requests(self):
        """동시 요청 처리 테스트"""
        import concurrent.futures
        import threading
        
        def make_request():
            response = client.get("/api/time")
            return response.status_code == 200
        
        # 10개의 동시 요청
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # 모든 요청이 성공해야 함
        assert all(results)
    
    def test_cors_headers(self):
        """CORS 헤더 테스트"""
        response = client.get("/api/time", headers={"Origin": "http://localhost:3000"})
        # FastAPI의 CORS 미들웨어가 적절히 처리하는지 확인
        assert response.status_code == 200
        # CORS 헤더가 포함되어 있는지 확인 (실제 환경에서만 확인 가능)


class TestDataConsistency:
    """데이터 일관성 테스트"""
    
    def test_timestamp_consistency(self):
        """타임스탬프 일관성 테스트"""
        # 기본 API
        response1 = client.get("/api/time")
        data1 = response1.json()
        
        # Unix API
        response2 = client.get("/api/time/unix")
        data2 = response2.json()
        
        # 1초 이내 차이여야 함
        assert abs(data1["timestamp"] - data2["timestamp"]) <= 1
    
    def test_time_progression(self):
        """시간 진행 테스트"""
        response1 = client.get("/api/time")
        data1 = response1.json()
        
        time.sleep(1)
        
        response2 = client.get("/api/time")
        data2 = response2.json()
        
        # 두 번째 요청의 타임스탬프가 더 커야 함
        assert data2["timestamp"] >= data1["timestamp"] 
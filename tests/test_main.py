import pytest
from fastapi.testclient import TestClient
from main import app

# TestClient 초기화를 fixture로 변경
@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


class TestTimeAPI:
    """Time API 핵심 테스트"""
    
    def test_root_endpoint(self, client):
        """루트 엔드포인트 테스트"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Time API Service"
        assert data["version"] == "1.0.0"
    
    def test_health_check(self, client):
        """헬스체크 엔드포인트 테스트"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert isinstance(data["timestamp"], int)
    
    def test_basic_time_endpoint(self, client):
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
        
        # 기본 데이터 타입 확인
        assert data["timezone"] == "UTC"
        assert isinstance(data["timestamp"], int)
        assert isinstance(data["date"], str)
        assert isinstance(data["time"], str)
    
    def test_iso_format_endpoint(self, client):
        """ISO 형식 시간 API 테스트"""
        response = client.get("/api/time/iso")
        assert response.status_code == 200
        data = response.json()
        
        assert data["format"] == "iso"
        assert "utc" in data
        assert "local" in data
        assert isinstance(data["utc"], str)
        assert isinstance(data["local"], str)
    
    def test_unix_format_endpoint(self, client):
        """Unix timestamp 형식 시간 API 테스트"""
        response = client.get("/api/time/unix")
        assert response.status_code == 200
        data = response.json()
        
        assert data["format"] == "unix"
        assert "timestamp" in data
        assert "milliseconds" in data
        assert isinstance(data["timestamp"], int)
        assert isinstance(data["milliseconds"], int)
    
    def test_korean_format_endpoint(self, client):
        """한국어 형식 시간 API 테스트"""
        response = client.get("/api/time/korean")
        assert response.status_code == 200
        data = response.json()
        
        assert data["format"] == "korean"
        assert "korean" in data
        assert "date" in data
        assert "time" in data
        assert "weekday" in data
        
        # 기본 타입 확인
        assert isinstance(data["korean"], str)
        assert isinstance(data["weekday"], str)
    
    def test_invalid_format_endpoint(self, client):
        """잘못된 형식 요청 테스트"""
        response = client.get("/api/time/invalid")
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data 
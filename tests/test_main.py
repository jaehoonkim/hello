import pytest
from fastapi.testclient import TestClient
from main import app

# TestClient 초기화를 fixture로 변경
@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


class TestTimeAPI:
    """기본 API 동작 확인 테스트"""
    
    def test_root_endpoint(self, client):
        """루트 엔드포인트 테스트"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
    
    def test_health_check(self, client):
        """헬스체크 엔드포인트 테스트"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_basic_time_endpoint(self, client):
        """기본 시간 API 테스트"""
        response = client.get("/api/time")
        assert response.status_code == 200
        data = response.json()
        
        # 필수 필드 존재 확인
        assert "timestamp" in data
        assert "date" in data
        assert "time" in data
        assert isinstance(data["timestamp"], int)
    
    def test_invalid_format_endpoint(self, client):
        """잘못된 형식 요청 에러 처리 테스트"""
        response = client.get("/api/time/invalid")
        assert response.status_code == 400 
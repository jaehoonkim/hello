# Time API

현재 날짜와 시간을 제공하는 FastAPI 기반 REST API 서비스입니다.

## 기능

- 현재 시간 정보 조회 (UTC 및 로컬 시간)
- 다양한 형식으로 시간 정보 제공 (ISO 8601, Unix timestamp, 한국어)
- CORS 지원
- 자동 API 문서 생성 (Swagger UI)

## 설치 및 실행

### 방법 1: Docker 사용 (권장)

#### Docker Compose로 실행
```bash
docker-compose up -d
```

#### 컨테이너 상태 확인
```bash
docker-compose ps
```

#### 로그 확인
```bash
docker-compose logs -f
```

#### 서비스 중지
```bash
docker-compose down
```

### 방법 2: 직접 실행

#### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

#### 2. 서버 실행
```bash
# 개발 서버 실행
python main.py

# 또는 uvicorn으로 직접 실행
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

서버가 실행되면 `http://localhost:8000`에서 접근할 수 있습니다.

## API 엔드포인트

### 1. 기본 시간 정보
```
GET /api/time
```

**응답 예시:**
```json
{
  "date": "2024-01-15",
  "time": "14:30:25",
  "datetime": "2024-01-15 14:30:25",
  "timestamp": 1705327825,
  "timezone": "UTC",
  "local_date": "2024-01-15",
  "local_time": "23:30:25",
  "local_datetime": "2024-01-15 23:30:25"
}
```

### 2. 형식별 시간 정보

#### ISO 8601 형식
```
GET /api/time/iso
```

**응답 예시:**
```json
{
  "format": "iso",
  "utc": "2024-01-15T14:30:25.123456+00:00",
  "local": "2024-01-15T23:30:25.123456"
}
```

#### Unix Timestamp
```
GET /api/time/unix
```

**응답 예시:**
```json
{
  "format": "unix",
  "timestamp": 1705327825,
  "milliseconds": 1705327825123
}
```

#### 한국어 형식
```
GET /api/time/korean
```

**응답 예시:**
```json
{
  "format": "korean",
  "korean": "2024년 1월 15일 월요일 오후 11시 30분 25초",
  "date": "2024년 1월 15일",
  "time": "오후 11시 30분",
  "weekday": "월요일"
}
```

### 3. 헬스 체크
```
GET /health
```

## API 문서

서버 실행 후 다음 URL에서 자동 생성된 API 문서를 확인할 수 있습니다:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 개발

### 개발 모드로 실행
```bash
uvicorn main:app --reload
```

### 테스트
```bash
# 기본 API 테스트
curl http://localhost:8000/api/time

# 형식별 테스트
curl http://localhost:8000/api/time/iso
curl http://localhost:8000/api/time/unix
curl http://localhost:8000/api/time/korean
```

## 기술 스택

- **Python 3.8+**
- **FastAPI**: 현대적이고 빠른 웹 프레임워크
- **Uvicorn**: ASGI 서버
- **CORS**: 크로스 오리진 요청 지원 
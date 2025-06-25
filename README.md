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

### 개발 환경 설정
```bash
# 개발 의존성 설치
pip install -r requirements-dev.txt
```

### 개발 모드로 실행
```bash
uvicorn main:app --reload
```

### 테스트 실행
```bash
# 전체 테스트 실행
pytest

# 상세 테스트 실행
pytest -v

# 특정 테스트 실행
pytest tests/test_main.py::TestTimeAPI::test_basic_time_endpoint
```

### 코드 품질 검사
```bash
# 린팅
flake8 main.py

# 코드 포맷팅 검사
black --check main.py

# 코드 포맷팅 적용
black main.py

# Import 정렬
isort main.py

# 보안 검사
bandit -r main.py
```

### API 테스트
```bash
# 기본 API 테스트
curl http://localhost:8000/api/time

# 형식별 테스트
curl http://localhost:8000/api/time/iso
curl http://localhost:8000/api/time/unix
curl http://localhost:8000/api/time/korean
```

## CI/CD

GitHub Actions를 통한 자동화된 CI/CD 파이프라인:

### CI 단계
1. **테스트**: Python 3.8-3.11에서 pytest 실행
2. **코드 품질**: flake8, black, isort 검사
3. **보안 스캔**: Trivy 취약점 스캔
4. **Docker 빌드**: 멀티 아키텍처 이미지 빌드
5. **스모크 테스트**: 컨테이너 기본 동작 확인

### CD 단계
- main 브랜치 푸시 시 자동 배포
- GitHub Container Registry에 이미지 푸시
- 자동 태깅 및 버전 관리

## 기술 스택

- **Python 3.8+**
- **FastAPI**: 현대적이고 빠른 웹 프레임워크
- **Uvicorn**: ASGI 서버
- **CORS**: 크로스 오리진 요청 지원 
# Spartamarket_DRF

Django REST Framework를 활용하여 간단한 온라인 마켓 API 서버를 구현한 프로젝트입니다.

<br>

## 목차
1. [프로젝트 소개](#프로젝트-소개)  
2. [주요 기능](#주요-기능)  
3. [프로젝트 구조](#프로젝트-구조)  
4. [설치 및 실행 방법](#설치-및-실행-방법)  
5. [API 상세](#api-상세)  

---

## 프로젝트 소개
&emsp;**Spartamarket_DRF**는 Django REST Framework(DRF)를 기반으로 한 간단한 온라인 마켓 API 서버입니다. 사용자는 회원 가입 및 로그인을 통해 상품을 등록, 조회, 수정, 삭제할 수 있으며, 댓글 기능 등을 통해 커뮤니케이션을 할 수 있습니다.

- **Django REST Framework** 활용
- **JWT 인증**(예: SimpleJWT)을 적용할 수 있음
- API 문서를 통해 엔드포인트 확인 및 테스트 (Postman, Thunder Client 등 사용)

---

## 주요 기능
- **계정 관리** (회원가입, 로그인, 사용자 목록 확인 등)
- **상품 관리** (상품 등록, 목록 조회, 상세 조회, 수정, 삭제)
- **댓글 관리** (댓글 작성, 조회, 수정, 삭제)

---

## 프로젝트 구조

```bash
├── accounts
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── db.sqlite3
├── manage.py
├── products
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── readme.md
├── requirements.txt
├── spartamarket_DRF
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
```
- **accounts/**: 사용자(회원) 관리 기능을 담당하는 앱
  - `models.py`: 사용자 관련 모델 정의
  - `serializers.py`: 사용자 모델 직렬화
  - `views.py`: 회원가입, 로그인, 사용자 조회 등의 기능 구현
  - `urls.py`: 계정 관련 URL 라우팅
- **products/**: 상품(마켓) 관리 기능을 담당하는 앱
  - `models.py`: 상품, 댓글 등 관련 모델 정의
  - `serializers.py`: 상품, 댓글 직렬화
  - `views.py`: 상품 등록/조회/수정/삭제, 댓글 기능 구현
  - `urls.py`: 상품 및 댓글 관련 URL 라우팅
- **spartamarket_DRF/**: Django 프로젝트 메인 폴더
  - `settings.py`: Django 및 DRF 설정
  - `urls.py`: 프로젝트 전역 URL 라우팅
  - `wsgi.py`, `asgi.py`: WSGI/ASGI 서버 구동용 파일
- `manage.py`: Django 명령줄 유틸리티
- `requirements.txt`: 프로젝트 의존성 라이브러리 목록
- `readme.md`: 프로젝트 소개 및 사용 방법

---

## 설치 및 실행 방법

### 1) 저장소 클론
```bash
$ git clone https://github.com/사용자명/Spartamarket_DRF.git
$ cd Spartamarket_DRF
```

### 2) 가상환경 생성 및 활성화
```bash
# 가상환경 생성 (venv 예시)
$ python -m venv venv

# Mac / Linux
$ source venv/bin/activate

# Windows
$ venv\Scripts\activate
```

### 3) 패키지 설치
```bash
(venv) $ pip install -r requirements.txt
```

### 4) 데이터베이스 마이그레이션
```bash
(venv) $ python manage.py migrate
```

### 5) 슈퍼유저 생성
```bash
(venv) $ python manage.py createsuperuser
```

### 6) 서버 실행
```bash
(venv) $ python manage.py runserver
```
이후 브라우저 또는 Postman/Thunder Client 등에서  
`http://127.0.0.1:8000/` 로 접속하여 서버 동작을 확인합니다.

---

## API 상세
> **주의**: 아래 API 예시는 사용 예시일 뿐, 실제 구현 내용과 다를 수 있습니다.  
> 프로젝트 진행 시 **accounts/urls.py**, **products/urls.py** 등에 맞춰 실제 엔드포인트를 확인하세요.

### 1) 계정(회원) 관련
| 기능         | 메서드 | 엔드포인트               | 요청 바디 예시                                      | 응답 예시                               |
|------------|------|-------------------------|------------------------------------------------|----------------------------------------|
| 회원가입      | POST | `/accounts/signup/`       | `{ "username": "testuser", "password": "1234" }` | `{ "message": "회원가입 성공" }`         |
| 로그인       | POST | `/accounts/login/`        | `{ "username": "testuser", "password": "1234" }` | `{ "token": "JWT 토큰" }` (예: SimpleJWT) |
| 사용자 목록 조회 | GET  | `/accounts/`             | -                                              | `[ { "id": 1, "username": "testuser" } ]` |

### 2) 상품 관련
| 기능         | 메서드  | 엔드포인트                | 요청 바디 예시                                                   | 응답 예시                                                      |
|------------|-------|--------------------------|-----------------------------------------------------------|--------------------------------------------------------------|
| 상품 목록 조회  | GET   | `/products/`              | -                                                         | `[ {"id":1, "title":"상품명", "content":"설명", "price":1000}, ... ]` |
| 상품 등록     | POST  | `/products/`              | `{ "title":"새 상품", "content":"설명", "price":2000 }`          | `{ "id":2, "title":"새 상품", "content":"설명", "price":2000 }`      |
| 상품 상세 조회  | GET   | `/products/1/`            | -                                                         | `{ "id":1, "title":"상품명", "content":"설명", "price":1000 }`      |
| 상품 수정     | PUT/PATCH | `/products/1/`            | `{ "title":"수정된 상품", "content":"설명 수정", "price":3000 }` | `{ "id":1, "title":"수정된 상품", "content":"설명 수정", "price":3000 }` |
| 상품 삭제     | DELETE | `/products/1/`            | -                                                         | `{ "message":"상품이 삭제되었습니다."}`                            |

### 3) 댓글 관련
| 기능        | 메서드  | 엔드포인트                            | 요청 바디 예시                   | 응답 예시                                              |
|-----------|-------|---------------------------------------|-----------------------------|-------------------------------------------------------|
| 댓글 목록 조회  | GET   | `/products/1/comments/`               | -                           | `[ {"id":1, "text":"좋은 상품입니다.", "user":...}, ... ]`  |
| 댓글 작성    | POST  | `/products/1/comments/`               | `{ "text": "좋은 상품이네요!" }` | `{ "id":2, "text":"좋은 상품이네요!", "user":"testuser" }`  |
| 댓글 수정    | PUT/PATCH | `/products/1/comments/2/`             | `{ "text": "내용 수정" }`      | `{ "id":2, "text":"내용 수정", "user":"testuser" }`       |
| 댓글 삭제    | DELETE | `/products/1/comments/2/`             | -                           | `{ "message":"댓글이 삭제되었습니다."}`                    |

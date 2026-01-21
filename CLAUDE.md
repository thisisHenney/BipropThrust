# BipropThrust 프로젝트

OpenFOAM 기반 이중추진제(MMH/NTO) 로켓 엔진 연소 시뮬레이션 GUI 애플리케이션

## 기술 스택
- **GUI**: PySide6 (Qt 6.10)
- **3D 시각화**: VTK 9.5.2
- **CFD**: OpenFOAM v2112
- **유틸리티**: nextlib (D:\lib\nextlib 또는 https://github.com/thisisHenney/nextlib)

## 프로젝트 구조
```
BipropThrust/
├── main.py              # 진입점 (temp 케이스 자동 생성)
├── common/              # 공용 데이터 모델
│   ├── app_context.py   # 서비스 레지스트리 (DI)
│   ├── app_data.py      # 전역 설정
│   └── case_data.py     # 케이스 데이터 관리
├── view/                # UI 레이어
│   ├── main/            # 메인 윈도우
│   │   └── main_window.py
│   └── panels/          # 설정 패널들 (미구현)
├── config/              # OpenFOAM 템플릿
│   └── basecase/        # 기본 케이스 (미복사)
├── res/                 # 리소스
└── old_code/            # 참고용 이전 코드
```

## 현재 진행 상황

### 완료
- [x] 프로젝트 구조 설계 및 생성
- [x] common 모듈 (app_context, app_data, case_data)
- [x] main.py (temp 케이스 자동 생성, 7일 후 자동 정리)
- [x] main_window.py 기본 구현
- [x] 임시 케이스 저장/삭제 다이얼로그
- [x] 윈도우 타이틀에 케이스 경로 표시
- [x] GitHub 연동 완료

### 다음 작업
- [ ] config/basecase 복사 (old_code에서)
- [ ] 실제 UI 구현 (메뉴, 독, VTK 위젯)
- [ ] center_widget.py 구현
- [ ] 패널들 구현 (geometry, mesh 등)
- [ ] OpenFOAM 연동

## 실행 방법
```bash
python main.py              # temp 케이스로 시작
python main.py <case_path>  # 특정 케이스 열기
```

## 주요 설계 결정
1. **Temp 케이스 방식**: MS Office처럼 즉시 작업 가능, Save As로 저장
2. **nextlib 활용**: OpenFOAM 파싱, VTK, 위젯 등 외부 라이브러리 사용
3. **서비스 레지스트리**: AppContext로 의존성 주입

## GitHub
- Repository: https://github.com/thisisHenney/BipropThrust

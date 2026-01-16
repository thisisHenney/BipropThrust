# BipropThrust GUI

OpenFOAM 기반 이중추진제 로켓 엔진 연소 시뮬레이션 GUI 애플리케이션

## 개요

BipropThrust는 MMH(Monomethylhydrazine)와 NTO(Nitrogen Tetroxide) 이중추진제 로켓 엔진의 연소 및 열전달 시뮬레이션을 위한 사용자 친화적인 그래픽 인터페이스입니다.

## 주요 기능

- 3D 형상 가져오기 및 시각화 (STL)
- OpenFOAM 메쉬 생성 및 관리
- 초기 조건 및 경계 조건 설정
- 물리 모델 선택 (난류, 연소, 복사 등)
- 분무 특성 설정 (MMH/NTO)
- 시뮬레이션 실행 및 모니터링
- 후처리 및 결과 시각화

## 기술 스택

- **GUI Framework:** PySide6 (Qt 6.10)
- **3D Visualization:** VTK 9.5.2
- **CFD Framework:** OpenFOAM v2112
- **Scientific Computing:** NumPy, matplotlib
- **Language:** Python 3.x

## 요구사항

- Python 3.8+
- OpenFOAM v2112+
- nextlib (커스텀 라이브러리)

## 설치

```bash
pip install -r requirements.txt
```

## 실행

```bash
python main.py
```

## 프로젝트 구조

```
BipropThrust/
├── main.py                  # 애플리케이션 진입점
├── common/                  # 공통 데이터 모델
│   ├── app_context.py      # 서비스 레지스트리
│   ├── app_data.py         # 애플리케이션 설정
│   └── case_data.py        # 케이스 데이터 관리
├── view/                    # UI 컴포넌트
│   ├── main/               # 메인 윈도우
│   └── panel/              # 설정 패널들
├── config/                  # OpenFOAM 템플릿
│   └── basecase/           # 기본 케이스 설정
├── res/                     # 리소스 (아이콘, 이미지)
└── help/                    # 도움말 문서
```

## 라이선스

Copyright (c) 2025 KARI

## 개발 상태

🚧 현재 개발 중

# 🎯 자리 입찰 게임

[![Streamlit](https://img.shields.io/badge/Streamlit-1.0-brightgreen)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/)

## 프로젝트 개요
## 프로젝트 개요

**자리 입찰 게임**은 학생들이 원하는 자리에 대해 포인트를 사용하여 입찰하고, 그 결과를 확인하는 인터랙티브 웹 애플리케이션입니다. 이 프로젝트는 교실 내에서 학생들이 공정하게 자리를 선택할 수 있도록 돕기 위해 개발되었습니다.

## 주요 기능

- **포인트 분배**: 학생들은 시작 포인트를 사용하여 원하는 자리에 입찰할 수 있습니다.
- **입찰 기능**: 학생들은 1지망, 2지망, 3지망으로 자리를 선택하고 입찰할 수 있습니다.
- **자리 배정**: 입찰 결과에 따라 각 학생에게 자리가 배정됩니다.
- **빈자리 처리**: 입찰에 실패한 학생들은 남은 빈자리 중에서 자동으로 배정됩니다.
- **결과 확인**: 최종 자리 배정 결과를 테이블 형식으로 확인할 수 있습니다.

## 사용 방법

1. **애플리케이션 실행**: 프로젝트를 로컬에서 실행하려면, 다음 명령어를 사용하세요.
    ```bash
    streamlit run app.py
    ```
   또는 [Streamlit Cloud](https://share.streamlit.io/)와 같은 호스팅 서비스를 통해 웹에서 실행할 수 있습니다.
   - 웹페이지 링크: [https://biddingseats.streamlit.app/](https://biddingseats.streamlit.app/)

2. **CSV 파일 업로드**: 게임에 참가할 학생들의 정보를 담은 CSV 파일을 업로드합니다. 이 CSV 파일에는 다음과 같은 컬럼이 포함되어야 합니다:
    - `studentId`: 학생 ID
    - `studentName`: 학생 이름
    - `points`: 학생이 시작할 때 가지는 포인트
    - `choice1`, `choice2`, `choice3`: 학생이 선택한 1지망, 2지망, 3지망 자리 번호
    - `bidPrice1`, `bidPrice2`, `bidPrice3`: 각 지망에 입찰한 포인트

3. **게임 진행**: 
    - 학생들이 원하는 자리에 대해 입찰을 진행합니다.
    - 각 자리마다 입찰할 수 있는 최대 포인트는 30점이며, 1지망에는 최소 10점 이상을 걸어야 합니다.

4. **결과 확인**: 모든 입찰이 완료되면, **게임 결과 확인** 버튼을 눌러 최종 자리 배정 결과를 확인할 수 있습니다. 결과는 테이블 형식으로 표시되며, 고정된 빈자리와 자동으로 배정된 자리도 포함됩니다.

## 예시 CSV 파일 구조

```csv
studentId,studentName,points,choice1,bidPrice1,choice2,bidPrice2,choice3,bidPrice3
1,김철수,100,3,20,5,10,7,5
2,이영희,100,2,15,4,20,1,10
3,박민수,100,1,30,6,15,8,5

## 프로젝트 구조

```plaintext
📂 프로젝트 루트
│
├── 📄 app.py           # Streamlit 애플리케이션 메인 파일
├── 📄 requirements.txt # 필요한 Python 패키지 목록
└── 📄 README.md        # 프로젝트 설명서 (이 파일)

## 요구 사항 (버전 1)

- Python 3.8 이상
- 필요한 패키지 설치:
    ```bash
    pip install -r requirements.txt
    ```

## Contribution

기여를 원하시면, 이 프로젝트를 포크한 후 풀 리퀘스트를 제출해 주세요. 버그 리포트와 기능 개선 제안도 환영합니다!

## Contact

- GitHub: [@hscrown](https://github.com/hscrown)
- 이메일: kwonhs.alice@gmail.com

## 라이선스

이 프로젝트는 MIT 라이선스에 따라 배포됩니다. 자세한 내용은 [LICENSE](./LICENSE) 파일을 참조하세요.


![image](https://github.com/user-attachments/assets/759abb67-b408-47bf-a9a4-882d72cb0e11)

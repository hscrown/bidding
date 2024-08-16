import streamlit as st
import pandas as pd

# 페이지 기본 설정
st.set_page_config(page_title="Bidding Game", page_icon="🎯", layout="wide")

# 제목과 설명
st.title("🎯 자리 입찰 게임")
st.markdown("""
    **자리 입찰 게임**에 오신 것을 환영합니다! 
    이 애플리케이션을 통해 학생들이 원하는 자리에 대해 입찰하고, 
    그 결과를 확인할 수 있습니다.

    ### 게임 방법
    1. **포인트 분배**: 각 학생은 서로 다른 포인트를 가지고 시작합니다. 이 포인트를 사용하여 원하는 자리에 입찰할 수 있습니다.

    2. **입찰 진행**: 
       - 학생들은 원하는 자리에 대해 1지망, 2지망, 3지망으로 입찰합니다.
       - 각 자리마다 입찰할 수 있는 최대 포인트는 **30점**입니다.
       - **1지망**에 입찰할 때는 **최소 10점 이상**을 걸어야 합니다.
       - 2지망과 3지망은 최소 점수 제한이 없으며, 학생들이 자유롭게 포인트를 분배하여 입찰할 수 있습니다.

    3. **자리 배정**: 입찰이 완료되면, 각 자리에 대해 가장 높은 포인트를 입찰한 학생이 해당 자리에 배정됩니다. 동일한 자리에 대해 같은 포인트를 입찰한 경우, 우선순위에 따라 자리가 배정됩니다.

    4. **빈자리 처리**: 입찰에서 실패한 학생들은 남은 빈자리 중에서 무작위로 자리가 배정됩니다. 특정 자리는 고정된 빈자리로 설정될 수 있으며, 이 자리는 누구도 배정되지 않습니다.

    5. **결과 확인**: 모든 자리가 배정된 후, 학생들의 최종 자리 배정 결과를 확인할 수 있습니다.

    이 게임을 통해 가장 원하는 자리를 차지해보세요! 모두에게 행운을 빕니다!
""")

# CSV 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # 데이터프레임 확인
    st.subheader("📊 가장 인기 있는 자리는?")
    
    # 1지망 상위 3개 인기 자리 계산
    top_3_seats_choice1 = df['choice1'].value_counts().head(3)
    
    # 결과 출력
    st.write("상위 3개의 인기 자리 (1지망 기준):")
    for seat, count in top_3_seats_choice1.items():
        st.write(f"{seat:02d}번 자리는 {count}명이 비딩했습니다.")

    # 1지망, 2지망, 3지망을 모두 합쳐서 상위 3개 인기 자리 계산
    combined_choices = pd.concat([df['choice1'], df['choice2'], df['choice3']])
    top_3_seats_combined = combined_choices.value_counts().head(3)

    # 결과 출력
    st.write("상위 3개의 인기 자리 (1지망, 2지망, 3지망 합산 기준):")
    for seat, count in top_3_seats_combined.items():
        st.write(f"{seat:02d}번 자리는 {count}명이 비딩했습니다.")
    
    # Student 클래스 정의
    class Student:
        def __init__(self, studentId, studentName, points, choice1, bidPrice1, choice2, bidPrice2, choice3, bidPrice3):
            self.studentId = studentId
            self.studentName = studentName
            self.points = points
            self.choice1 = choice1
            self.bidPrice1 = bidPrice1
            self.choice2 = choice2
            self.bidPrice2 = bidPrice2
            self.choice3 = choice3
            self.bidPrice3 = bidPrice3

    # df로 Student 객체 생성
    students = [Student(studentId, studentName, points, choice1, bidPrice1, choice2, bidPrice2, choice3, bidPrice3)
                for studentId, studentName, points, choice1, bidPrice1, choice2, bidPrice2, choice3, bidPrice3 
                in zip(df['studentId'], df['studentName'], df['points'], df['choice1'], df['bidPrice1'], 
                       df['choice2'], df['bidPrice2'], df['choice3'], df['bidPrice3'])]

    # 자리 배정을 위한 딕셔너리
    assigned_seats = {}
    failed_students = set()

    # 고정된 빈자리
    fixed_empty_seats = {5, 30}

    def assign_seat(student, choice, bidding):
        # 고정된 빈자리에 베팅한 경우 무효 처리 (즉, 배정하지 않음)
        if choice in fixed_empty_seats:
            return False
        
        # 선택한 자리가 아직 배정되지 않았거나, 더 높은 입찰가인 경우 배정
        if choice not in assigned_seats or bidding > assigned_seats[choice][1]:
            assigned_seats[choice] = (student, bidding)
            return True
        return False

    def assign_all_seats(students):
        for priority in ['first', 'second', 'third']:  # 1지망, 2지망, 3지망 순서대로 처리
            for student in students:
                if priority == 'first':
                    if assign_seat(student, student.choice1, student.bidPrice1):
                        continue
                elif priority == 'second':
                    if assign_seat(student, student.choice2, student.bidPrice2):
                        continue
                elif priority == 'third':
                    if assign_seat(student, student.choice3, student.bidPrice3):
                        continue
                failed_students.add(student)

    # 자리 배정을 수행
    assign_all_seats(students)

    # 남은 자리 찾기 (고정된 빈자리를 제외한 자리들 중에서 1번부터 시작해서 빈 번호가 없게)
    total_seats = list(range(1, len(students) + 1))  # 전체 자리 번호 (1부터 시작)
    occupied_seats = set(assigned_seats.keys())  # 이미 배정된 자리 번호
    remaining_seats = sorted(list(set(total_seats) - occupied_seats - fixed_empty_seats))  # 남은 자리 번호를 정렬 (고정된 빈자리 제외)

    # 탈락한 학생들을 남는 자리에 순서대로 배정
    for student in failed_students:
        if remaining_seats:
            next_seat = remaining_seats.pop(0)  # 가장 작은 번호의 자리부터 배정
            assigned_seats[next_seat] = (student, 'random')

    # 게임 결과 확인 버튼
    if st.button("게임 결과 확인"):
        st.subheader("🎮 자리 배정 결과")

        max_columns = 5
        sorted_seats = sorted(assigned_seats.items(), key=lambda x: x[0])  # 자리번호로 정렬

        # 5열로 나누어 결과 표시
        rows = []
        for i in range(0, len(total_seats), max_columns):
            row = []
            for j in range(max_columns):
                seat_number = i + j + 1
                if seat_number in assigned_seats:
                    student, _ = assigned_seats[seat_number]
                    row.append(f"{seat_number}번: {student.studentName}")
                elif seat_number in fixed_empty_seats:
                    row.append(f"{seat_number}번: 빈자리 (고정)")
                else:
                    row.append(f"{seat_number}번: 빈자리")
            rows.append(row)

        result_df = pd.DataFrame(rows, columns=[f"열 {i+1}" for i in range(max_columns)])

        # 표 스타일링
        st.write("자리 배정 결과:")
        st.table(result_df.style.set_table_styles([
            {'selector': 'thead th', 'props': [('background-color', '#4CAF50'), ('color', 'white')]},
            {'selector': 'tbody td', 'props': [('text-align', 'center'), ('padding', '10px')]},
            {'selector': 'tbody tr:nth-child(even)', 'props': [('background-color', '#f2f2f2')]}
        ]))

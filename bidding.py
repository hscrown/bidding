import streamlit as st
import pandas as pd
import random

# 페이지 기본 설정
st.set_page_config(page_title="Bidding Game", page_icon="🎯", layout="wide")

# 제목과 설명
st.title("🎯 학생 입찰 게임")
st.markdown("""
    **학생 입찰 게임**에 오신 것을 환영합니다! 
    이 애플리케이션을 통해 학생들이 원하는 항목에 대해 입찰하고, 
    그 결과를 확인할 수 있습니다.
""")

# CSV 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # 데이터프레임 확인
    st.subheader("📊 CSV 파일 데이터")
    st.dataframe(df.head())

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

    def assign_seat(student, choice, bidding, priority):
        if choice not in assigned_seats:
            assigned_seats[choice] = (student, priority)
            return True
        else:
            assigned_student, assigned_priority = assigned_seats[choice]
            assigned_bidding = getattr(assigned_student, f"bidPrice{['first', 'second', 'third'].index(assigned_priority) + 1}")
            
            if priority == assigned_priority and bidding == assigned_bidding:
                failed_students.add(student)
                return False
            elif bidding > assigned_bidding:
                assigned_seats[choice] = (student, priority)
                failed_students.add(assigned_student)
                return True
            else:
                return False

    def assign_all_seats(students):
        for student in students:
            for choice, bid_price, priority in zip([student.choice1, student.choice2, student.choice3], 
                                                   [student.bidPrice1, student.bidPrice2, student.bidPrice3], 
                                                   ['first', 'second', 'third']):
                if assign_seat(student, choice, bid_price, priority):
                    break

    assign_all_seats(students)

    # 남는 자리 찾기
    total_seats = list(range(1, len(students) + 1))  # 전체 자리 번호 (1부터 시작)
    occupied_seats = set(assigned_seats.keys())  # 이미 배정된 자리 번호
    remaining_seats = list(set(total_seats) - occupied_seats)  # 남은 자리 번호

    # 탈락한 학생들을 남는 자리에 랜덤 배정
    for student in failed_students:
        if remaining_seats:
            random_seat = random.choice(remaining_seats)
            assigned_seats[random_seat] = (student, 'random')
            remaining_seats.remove(random_seat)

    # 게임 결과 확인 버튼
    if st.button("게임 결과 확인"):
        st.subheader("🎮 자리 배정 결과")

        max_columns = 5
        sorted_seats = sorted(assigned_seats.items(), key=lambda x: x[0])  # 자리번호로 정렬

        # 5열로 나누어 결과 표시
        rows = []
        for i in range(0, len(sorted_seats), max_columns):
            row = [f"{seat_number}번: {student.studentName}" for seat_number, (student, _) in sorted_seats[i:i + max_columns]]
            rows.append(row)

        result_df = pd.DataFrame(rows, columns=[f"열 {i+1}" for i in range(max_columns)])

        # 표 스타일링
        st.write("자리 배정 결과:")
        st.table(result_df.style.set_table_styles([
            {'selector': 'thead th', 'props': [('background-color', '#4CAF50'), ('color', 'white')]},
            {'selector': 'tbody td', 'props': [('text-align', 'center'), ('padding', '10px')]},
            {'selector': 'tbody tr:nth-child(even)', 'props': [('background-color', '#f2f2f2')]}
        ]))

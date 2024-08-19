import streamlit as st
import pandas as pd

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

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        if df.empty:
            st.warning("업로드한 파일이 비어 있습니다. 유효한 CSV 파일을 업로드하세요.")
        else:
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

            def assign_choice(priority, remaining_students):
                """ 
                주어진 priority에 따라 학생들을 배정하는 함수 
                priority는 'choice1', 'choice2', 'choice3' 중 하나를 의미
                """
                while remaining_students:
                    choices = [getattr(student, priority) for student in remaining_students]
                    bids = [getattr(student, f'bidPrice{priority[-1]}') for student in remaining_students]

                    # choice 기준으로 bid의 최대값을 구하고, 동일한 최고 입찰자가 있을 경우 탈락 처리
                    df_choices = pd.DataFrame({
                        'student': remaining_students,
                        'choice': choices,
                        'bid': bids
                    })
                    
                    # 각 choice에 대해 최대 입찰가 계산
                    max_bids = df_choices.groupby('choice')['bid'].max()

                    assigned = False
                    for choice, max_bid in max_bids.items():
                        best_students = df_choices[(df_choices['choice'] == choice) & (df_choices['bid'] == max_bid)]
                        
                        if len(best_students) == 1:
                            # 최고 입찰자가 한 명인 경우 해당 학생 배정
                            chosen_student = best_students.iloc[0]['student']
                            assigned_seats[choice] = chosen_student
                            remaining_students.remove(chosen_student)
                            assigned = True
                        else:
                            # 최고 입찰자가 여러 명인 경우 모두 탈락 처리
                            for _, student_row in best_students.iterrows():
                                remaining_students.remove(student_row['student'])

                    if not assigned:
                        break
                return remaining_students

            # 1지망, 2지망, 3지망에 대해 순차적으로 배정
            remaining_students = assign_choice('choice1', students)
            remaining_students = assign_choice('choice2', remaining_students)
            remaining_students = assign_choice('choice3', remaining_students)

            # 남은 자리 찾기 (고정된 빈자리를 제외한 자리들 중에서 1번부터 시작해서 빈 번호가 없게)
            total_seats = list(range(1, len(students) + 1))  # 전체 자리 번호 (1부터 시작)
            occupied_seats = set(assigned_seats.keys())  # 이미 배정된 자리 번호
            remaining_seats = sorted(list(set(total_seats) - occupied_seats - fixed_empty_seats))  # 남은 자리 번호를 정렬 (고정된 빈자리 제외)

            # 탈락한 학생들을 남는 자리에 순서대로 배정
            failed_students = set(students) - set(assigned_seats.values())
            for student in failed_students:
                if remaining_seats:
                    next_seat = remaining_seats.pop(0)  # 가장 작은 번호의 자리부터 배정
                    assigned_seats[next_seat] = student

            # 5열로 나누어 결과 표시
            rows = []
            for i in range(0, len(total_seats), 5):
                row = []
                for j in range(5):
                    seat_number = i + j + 1
                    if seat_number in assigned_seats:
                        student = assigned_seats[seat_number]
                        row.append(f"{seat_number}번: {student.studentName}")
                    elif seat_number in fixed_empty_seats:
                        row.append(f"{seat_number}번: 빈자리 (고정)")
                    else:
                        row.append(f"{seat_number}번: 빈자리")
                rows.append(row)

            result_df = pd.DataFrame(rows, columns=[f"열 {i+1}" for i in range(5)])

            # 표 스타일링
            st.write("자리 배정 결과:")
            st.table(result_df.style.set_table_styles([
                {'selector': 'thead th', 'props': [('background-color', '#4CAF50'), ('color', 'white'), ('text-align', 'center')]},
                {'selector': 'tbody td', 'props': [('text-align', 'center'), ('padding', '10px')]},
                {'selector': 'tbody tr:nth-child(even)', 'props': [('background-color', '#f2f2f2')]}
            ]))
    except pd.errors.EmptyDataError:
        st.error("업로드한 파일이 비어 있거나 유효한 CSV 형식이 아닙니다. 다시 시도하세요.")
else:
    st.warning("먼저 CSV 파일을 업로드하세요.")

# 푸터 추가
st.markdown("""
    <div class="footer">
        © 2024 oystershells
    </div>
""", unsafe_allow_html=True)

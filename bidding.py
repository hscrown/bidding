import streamlit as st
import pandas as pd

# Student 클래스 정의
class Student:
    def __init__(self, studentId, studentName, points, choice1, bidPrice1, choice2, bidPrice2):
        self.studentId = studentId
        self.studentName = studentName
        self.points = points
        self.choice1 = choice1
        self.bidPrice1 = bidPrice1
        self.choice2 = choice2
        self.bidPrice2 = bidPrice2

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        if df.empty:
            st.warning("업로드한 파일이 비어 있습니다. 유효한 CSV 파일을 업로드하세요.")
        else:
            # df로 Student 객체 생성
            students = [Student(studentId, studentName, points, choice1, bidPrice1, choice2, bidPrice2)
                        for studentId, studentName, points, choice1, bidPrice1, choice2, bidPrice2
                        in zip(df['studentId'], df['studentName'], df['points'], df['choice1'], df['bidPrice1'], 
                               df['choice2'], df['bidPrice2'])]

            # 자리 배정을 위한 딕셔너리
            assigned_seats = {}

            def assign_choice(students, priority):
                """
                특정 지망(priority)을 기준으로 자리 배정을 수행하는 함수
                priority는 'choice1' 또는 'choice2'로 지정
                """
                remaining_students = students[:]
                while remaining_students:
                    # 현재 남아있는 학생들 중에서 지망에 대한 최고점 찾기
                    df_choices = pd.DataFrame({
                        'student': remaining_students,
                        'choice': [getattr(s, priority) for s in remaining_students],
                        'bidPrice': [getattr(s, f'bidPrice{priority[-1]}') for s in remaining_students]
                    })

                    max_bid = df_choices['bidPrice'].max()
                    best_students = df_choices[df_choices['bidPrice'] == max_bid]

                    if len(best_students) > 1:
                        # 동일한 최고 입찰가를 제시한 학생들이 여러 명인 경우, 이 학생들을 탈락시킴
                        for _, student_row in best_students.iterrows():
                            remaining_students.remove(student_row['student'])
                    else:
                        # 유일한 최고 입찰가 학생이 있는 경우, 그 학생을 해당 자리에 배정
                        chosen_student = best_students.iloc[0]['student']
                        assigned_seats[best_students.iloc[0]['choice']] = chosen_student
                        remaining_students.remove(chosen_student)

                    # 최종적으로 유일한 학생이 배정되면, 다음 순번으로 진행
                    if len(best_students) == 1:
                        break

                return remaining_students

            # 1지망 배정 수행
            remaining_students_after_choice1 = assign_choice(students, 'choice1')

            # 2지망 배정 수행 (1지망에서 자리가 배정되지 않은 학생들만 대상으로)
            assign_choice(remaining_students_after_choice1, 'choice2')

            # 배정된 결과를 테이블로 출력
            st.subheader("🎮 자리 배정 결과")
            result_rows = []
            for seat, student in sorted(assigned_seats.items()):
                result_rows.append([f"{seat}번 자리", student.studentName])

            result_df = pd.DataFrame(result_rows, columns=["자리", "배정된 학생"])

            # 결과 출력
            st.write("자리 배정 결과:")
            st.table(result_df)
    
    except pd.errors.EmptyDataError:
        st.error("업로드한 파일이 비어 있거나 유효한 CSV 형식이 아닙니다. 다시 시도하세요.")
else:
    st.warning("먼저 CSV 파일을 업로드하세요.")

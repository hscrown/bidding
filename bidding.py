import streamlit as st
import pandas as pd

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        if df.empty:
            st.warning("업로드한 파일이 비어 있습니다. 유효한 CSV 파일을 업로드하세요.")
        else:
            # 자리 배정을 위한 딕셔너리 (seat_number: studentID)
            assigned_seats = {}

            def assign_seat(df, choice_column, bid_column, taken_seats):
                """
                주어진 지망에 따라 자리를 배정하는 함수
                - choice_column: 'choice1', 'choice2', 'choice3' 중 하나
                - bid_column: 'bidPrice1', 'bidPrice2', 'bidPrice3' 중 하나
                - taken_seats: 이미 배정된 자리 (다른 지망에서 배정된 자리 포함)
                """
                unassigned_students = []

                for _, student in df.iterrows():
                    student_id = student['studentId']
                    student_name = student['studentName']
                    choice = student[choice_column]
                    bid = student[bid_column]

                    # 해당 자리가 이미 배정되었는지 확인
                    if choice in taken_seats:
                        st.write(f"학생 {student_name}의 {choice_column} 자리 {choice}는 이미 배정됨.")
                        continue  # 이미 배정된 자리면 건너뜀

                    # 해당 자리를 차지할 다른 학생이 있는지 확인
                    conflicting_students = df[(df[choice_column] == choice) & (df[bid_column] > bid)]

                    if conflicting_students.empty:
                        # 자리를 배정
                        assigned_seats[choice] = {
                            'studentId': student_id,
                            'studentName': student_name,
                            'bid': bid,
                            'choice': choice_column
                        }
                        taken_seats.add(choice)
                        st.write(f"학생 {student_name}가 {choice}번 자리에 배정됨. (입찰 점수: {bid})")
                    else:
                        st.write(f"학생 {student_name}는 {choice_column}에서 자리 배정 실패.")
                        unassigned_students.append(student)

                return pd.DataFrame(unassigned_students)

            # 1지망 배정 수행
            taken_seats = set()
            remaining_df = assign_seat(df, 'choice1', 'bidPrice1', taken_seats)

            # 2지망 배정 수행 (1지망에서 자리가 배정되지 않은 학생들만 대상으로)
            if not remaining_df.empty:
                remaining_df = assign_seat(remaining_df, 'choice2', 'bidPrice2', taken_seats)

            # 3지망 배정 수행 (2지망에서도 자리가 배정되지 않은 학생들만 대상으로)
            if not remaining_df.empty:
                remaining_df = assign_seat(remaining_df, 'choice3', 'bidPrice3', taken_seats)

            # 1, 2, 3지망 모두에서 자리를 배정받지 못한 학생들
            unassigned_students = remaining_df

            # 배정된 결과를 테이블로 출력
            st.subheader("🎮 자리 배정 결과")
            result_rows = []
            for seat, data in sorted(assigned_seats.items()):
                result_rows.append([f"{seat}번 자리", data['studentName'], data['choice'], data['bid']])

            result_df = pd.DataFrame(result_rows, columns=["자리", "배정된 학생", "지망", "입찰 점수"])
            st.write("자리 배정 결과:")
            st.table(result_df)

            # 자리를 배정받지 못한 학생들 출력
            if not unassigned_students.empty:
                st.subheader("🚨 자리를 배정받지 못한 학생들")
                st.write("다음 학생들은 1, 2, 3지망 모두에서 자리를 배정받지 못했습니다:")
                st.table(unassigned_students[['studentId', 'studentName']])
            else:
                st.success("모든 학생이 자리를 배정받았습니다!")

    except pd.errors.EmptyDataError:
        st.error("업로드한 파일이 비어 있거나 유효한 CSV 형식이 아닙니다. 다시 시도하세요.")
else:
    st.warning("먼저 CSV 파일을 업로드하세요.")

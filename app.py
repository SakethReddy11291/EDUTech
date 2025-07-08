import streamlit as st
import random

# Mock student data for progress tracking
students_progress = {
    "student_1": {
        "score": 85,
        "last_quiz": "Algebra",
        "attempts": 3,
        "next_topic": "Geometry"
    },
    "student_2": {
        "score": 65,
        "last_quiz": "Fractions",
        "attempts": 2,
        "next_topic": "Decimals"
    },
    "student_3": {
        "score": 45,
        "last_quiz": "Addition",
        "attempts": 4,
        "next_topic": "Subtraction"
    }
}

# Mock courses
mock_courses = [
    {"name": "Math 101"},
    {"name": "Science Basics"},
    {"name": "English Grammar"}
]

# Mock AI-powered quiz generation
def generate_quiz(course_data, difficulty="medium"):
    # Placeholder: questions differ by difficulty
    easy_q = [{"question": "What is 1+1?", "options": ["1", "2", "3"], "answer": "2"}]
    medium_q = [{"question": "What is 5x5?", "options": ["20", "25", "30"], "answer": "25"}]
    hard_q = [{"question": "Solve √144", "options": ["10", "12", "14"], "answer": "12"}]

    return {
        "questions": easy_q if difficulty == "easy" else hard_q if difficulty == "hard" else medium_q,
        "difficulty": difficulty
    }

# Adaptive quiz logic
def adaptive_quiz(student_id):
    student_score = students_progress[student_id]["score"]
    difficulty = "easy" if student_score < 60 else "medium" if student_score < 80 else "hard"
    quiz_data = generate_quiz({'course_name': 'Math 101'}, difficulty)
    return quiz_data

# Streamlit UI for student dashboard
def student_dashboard():
    st.title("📘 Student Dashboard")
   
    student_id = st.selectbox("Select Student", list(students_progress.keys()))
    student_data = students_progress[student_id]
   
    st.subheader(f"Progress for **{student_id}**")
    st.write(f"**Last Quiz:** {student_data['last_quiz']}")
    st.write(f"**Current Score:** {student_data['score']}")
    st.write(f"**Attempts:** {student_data['attempts']}")
    st.write(f"**Next Topic:** {student_data['next_topic']}")
   
    if st.button("Generate Adaptive Quiz"):
        quiz_data = adaptive_quiz(student_id)
        st.write(f"📋 Difficulty: **{quiz_data['difficulty'].capitalize()}**")
        for idx, q in enumerate(quiz_data["questions"]):
            st.write(f"**Q{idx + 1}.** {q['question']}")
            st.radio("Select Answer", q['options'], key=f"q{idx}")
       
        if st.button("Submit Quiz"):
            score = random.randint(50, 100)  # Simulate quiz score
            students_progress[student_id]["score"] = score
            students_progress[student_id]["attempts"] += 1
            st.success(f"🎉 Your new score is **{score}**")

# Streamlit UI for educator dashboard
def educator_dashboard():
    st.title("🧑‍🏫 Educator Dashboard")

    st.subheader("Courses")
    for course in mock_courses:
        st.write(f"📚 Course Name: **{course['name']}**")

    student_id = st.selectbox("Select Student", list(students_progress.keys()))
    student_data = students_progress[student_id]

    st.subheader(f"Progress for **{student_id}**")
    st.write(f"**Last Quiz:** {student_data['last_quiz']}")
    st.write(f"**Score:** {student_data['score']}")
    st.write(f"**Attempts:** {student_data['attempts']}")

    st.subheader(f"Mock Insights")
    insight_score = "Above Average" if student_data["score"] >= 75 else "Needs Improvement"
    st.info(f"Insight: This student is performing **{insight_score}**")

# Main function
def main():
    st.sidebar.title("🎓 EduTutor AI")
    choice = st.sidebar.selectbox("Select Dashboard", ["Student Dashboard", "Educator Dashboard"])
   
    if choice == "Student Dashboard":
        student_dashboard()
    else:
        educator_dashboard()

if __name__ == '__main__':
    main()

import streamlit as st
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import random
import pinecone
import requests
import os

# Google OAuth 2.0 setup
SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly', 'https://www.googleapis.com/auth/classroom.rosters.readonly']

# Initialize Pinecone for Vector DB
pinecone.init(api_key="your-pinecone-api-key", environment="us-west1-gcp")
index = pinecone.Index("student-performance")

# Mock student data for progress tracking
students_progress = {
    "student_1": {
        "score": 85,
        "last_quiz": "Algebra",
        "attempts": 3,
        "next_topic": "Geometry"
    }
}

# Google Classroom integration (OAuth flow)
def authenticate_google():
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    return build('classroom', 'v1', credentials=creds)

def get_courses():
    service = authenticate_google()
    courses = service.courses().list().execute()
    return courses.get('courses', [])

# AI-powered quiz generation (Granite API - mock)
def generate_quiz(course_data, difficulty="medium"):
    # Placeholder for an actual Granite API call
    quiz_data = {
        "questions": [
            {"question": "What is 2+2?", "options": ["2", "4", "6"], "answer": "4"},
            {"question": "What is the capital of France?", "options": ["Berlin", "Madrid", "Paris"], "answer": "Paris"}
        ],
        "difficulty": difficulty
    }
    return quiz_data

# Adaptive quiz generation based on student progress
def adaptive_quiz(student_id):
    student_score = students_progress[student_id]["score"]
    difficulty = "easy" if student_score < 60 else "medium" if student_score < 80 else "hard"
    quiz_data = generate_quiz({'course_name': 'Math 101'}, difficulty)
    return quiz_data

# Store student data to Pinecone
def store_student_data(student_id, performance_vector):
    index.upsert([(student_id, performance_vector)])

# Get student performance from Pinecone
def get_student_insights(student_id):
    result = index.query([student_id], top_k=3)
    return result

# Streamlit UI for student dashboard
def student_dashboard():
    st.title("Student Dashboard")
    
    student_id = st.selectbox("Select Student", list(students_progress.keys()))
    student_data = students_progress[student_id]
    
    st.subheader(f"Progress for {student_id}")
    st.write(f"Last Quiz: {student_data['last_quiz']}")
    st.write(f"Current Score: {student_data['score']}")
    st.write(f"Attempts: {student_data['attempts']}")
    st.write(f"Next Topic: {student_data['next_topic']}")
    
    # Show adaptive quiz
    if st.button("Generate Adaptive Quiz"):
        quiz_data = adaptive_quiz(student_id)
        st.write("Here is your adaptive quiz:")
        for idx, q in enumerate(quiz_data["questions"]):
            st.write(f"{idx + 1}. {q['question']}")
            st.radio("Select Answer", q['options'], key=f"q{idx}")
        
        # Mock score submission
        if st.button("Submit Quiz"):
            score = random.randint(50, 100)  # Random mock score
            students_progress[student_id]["score"] = score
            students_progress[student_id]["attempts"] += 1
            st.success(f"Your new score is {score}")

# Streamlit UI for educator dashboard
def educator_dashboard():
    st.title("Educator Dashboard")
    
    # Fetch courses from Google Classroom
    courses = get_courses()
    
    st.subheader("Courses from Google Classroom")
    for course in courses:
        st.write(f"Course Name: {course['name']}")
    
    # Show student performance in a chart-like format
    student_id = st.selectbox("Select Student to View Progress", list(students_progress.keys()))
    student_data = students_progress[student_id]
    
    st.subheader(f"Student Progress for {student_id}")
    st.write(f"Last Quiz: {student_data['last_quiz']}")
    st.write(f"Current Score: {student_data['score']}")
    st.write(f"Attempts: {student_data['attempts']}")
    
    # Pinecone Insights (Mock)
    st.subheader(f"Insights from Pinecone DB for {student_id}")
    insights = get_student_insights(student_id)
    st.write(insights)

# Main function to display the appropriate dashboard
def main():
    st.sidebar.title("EduTutor AI")
    choice = st.sidebar.selectbox("Select Dashboard", ["Student Dashboard", "Educator Dashboard"])
    
    if choice == "Student Dashboard":
        student_dashboard()
    else:
        educator_dashboard()

if __name__ == '__main__':
    main()

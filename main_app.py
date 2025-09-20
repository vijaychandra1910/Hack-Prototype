# AI-Powered Career and Skills Advisor - Complete Prototype
# Main Application File

import streamlit as st
import pandas as pd
import numpy as np
import json
import pickle
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import sqlite3
import hashlib

# Page Configuration
st.set_page_config(
    page_title="🎓 AI Career Advisor", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'assessment_complete' not in st.session_state:
    st.session_state.assessment_complete = False

# Database Setup
def init_database():
    conn = sqlite3.connect('career_advisor.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, 
                  username TEXT UNIQUE, 
                  password TEXT, 
                  email TEXT,
                  created_at TIMESTAMP)''')
    
    # Assessments table
    c.execute('''CREATE TABLE IF NOT EXISTS assessments
                 (id INTEGER PRIMARY KEY,
                  user_id INTEGER,
                  technical_skills TEXT,
                  personality_traits TEXT,
                  career_interests TEXT,
                  recommendations TEXT,
                  created_at TIMESTAMP,
                  FOREIGN KEY(user_id) REFERENCES users(id))''')
    
    # Progress tracking table
    c.execute('''CREATE TABLE IF NOT EXISTS progress
                 (id INTEGER PRIMARY KEY,
                  user_id INTEGER,
                  goal_type TEXT,
                  goal_description TEXT,
                  target_date TEXT,
                  completion_status TEXT,
                  created_at TIMESTAMP,
                  FOREIGN KEY(user_id) REFERENCES users(id))''')
    
    conn.commit()
    conn.close()

# Authentication Functions
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def create_user(username, password, email):
    conn = sqlite3.connect('career_advisor.db')
    c = conn.cursor()
    try:
        hashed_pw = hash_password(password)
        c.execute("INSERT INTO users (username, password, email, created_at) VALUES (?, ?, ?, ?)",
                  (username, hashed_pw, email, datetime.now()))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(username, password):
    conn = sqlite3.connect('career_advisor.db')
    c = conn.cursor()
    hashed_pw = hash_password(password)
    c.execute("SELECT id, username FROM users WHERE username=? AND password=?", 
              (username, hashed_pw))
    user = c.fetchone()
    conn.close()
    return user

# Career Data and Models
class CareerAdvisor:
    def __init__(self):
        self.technical_skills = [
            "Python Programming", "Java Programming", "JavaScript", "Database Management",
            "Web Development", "Mobile Development", "Data Structures & Algorithms",
            "Machine Learning", "Artificial Intelligence", "Cybersecurity",
            "Cloud Computing", "DevOps", "Software Testing", "System Design",
            "Computer Networks", "UI/UX Design", "Project Management"
        ]
        
        self.personality_traits = [
            "Openness", "Conscientiousness", "Extraversion", 
            "Agreeableness", "Neuroticism"
        ]
        
        self.career_interests = [
            "Realistic", "Investigative", "Artistic", 
            "Social", "Enterprising", "Conventional"
        ]
        
        self.career_paths = {
            "Software Developer": {
                "description": "Design and develop software applications and systems",
                "key_skills": ["Python Programming", "Java Programming", "Software Testing"],
                "salary_range": "$70K - $120K",
                "growth_rate": "25%",
                "personality_fit": ["Conscientiousness", "Openness"]
            },
            "Data Scientist": {
                "description": "Analyze complex data to extract insights and build predictive models",
                "key_skills": ["Machine Learning", "Python Programming", "Data Structures & Algorithms"],
                "salary_range": "$90K - $150K",
                "growth_rate": "35%",
                "personality_fit": ["Openness", "Conscientiousness"]
            },
            "Cybersecurity Analyst": {
                "description": "Protect organizations from cyber threats and security breaches",
                "key_skills": ["Cybersecurity", "Computer Networks", "System Design"],
                "salary_range": "$80K - $130K",
                "growth_rate": "28%",
                "personality_fit": ["Conscientiousness", "Investigative"]
            },
            "AI Engineer": {
                "description": "Develop and implement artificial intelligence solutions",
                "key_skills": ["Artificial Intelligence", "Machine Learning", "Python Programming"],
                "salary_range": "$100K - $160K",
                "growth_rate": "40%",
                "personality_fit": ["Openness", "Investigative"]
            },
            "Full Stack Developer": {
                "description": "Develop both frontend and backend of web applications",
                "key_skills": ["Web Development", "JavaScript", "Database Management"],
                "salary_range": "$75K - $125K",
                "growth_rate": "30%",
                "personality_fit": ["Conscientiousness", "Openness"]
            },
            "Product Manager": {
                "description": "Lead product development and strategy",
                "key_skills": ["Project Management", "UI/UX Design", "System Design"],
                "salary_range": "$95K - $140K",
                "growth_rate": "20%",
                "personality_fit": ["Extraversion", "Enterprising"]
            }
        }
    
    def calculate_career_match(self, technical_scores, personality_scores, interest_scores):
        recommendations = []
        
        for career, details in self.career_paths.items():
            # Technical skill match
            tech_match = 0
            for skill in details["key_skills"]:
                if skill in technical_scores:
                    tech_match += technical_scores[skill]
            tech_match = tech_match / len(details["key_skills"]) if details["key_skills"] else 0
            
            # Personality match
            personality_match = 0
            for trait in details["personality_fit"]:
                if trait in personality_scores:
                    personality_match += personality_scores[trait]
                elif trait in interest_scores:
                    personality_match += interest_scores[trait]
            personality_match = personality_match / len(details["personality_fit"]) if details["personality_fit"] else 0
            
            # Overall match score
            overall_score = (tech_match * 0.6) + (personality_match * 0.4)
            
            recommendations.append({
                "career": career,
                "score": overall_score,
                "details": details,
                "tech_match": tech_match,
                "personality_match": personality_match
            })
        
        return sorted(recommendations, key=lambda x: x['score'], reverse=True)

# Authentication UI
def authentication_page():
    st.title("🎓 AI Career and Skills Advisor")
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login to Your Account")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            user = verify_user(username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user_id = user[0]
                st.session_state.username = user[1]
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")
    
    with tab2:
        st.subheader("Create New Account")
        new_username = st.text_input("Username", key="reg_username")
        new_email = st.text_input("Email", key="reg_email")
        new_password = st.text_input("Password", type="password", key="reg_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")
        
        if st.button("Register"):
            if new_password == confirm_password:
                if create_user(new_username, new_password, new_email):
                    st.success("Account created successfully! Please login.")
                else:
                    st.error("Username already exists")
            else:
                st.error("Passwords do not match")

# Profile Management
def profile_page():
    st.title("👤 User Profile")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Personal Information")
        name = st.text_input("Full Name", value=st.session_state.user_data.get('name', ''))
        age = st.number_input("Age", min_value=16, max_value=100, value=st.session_state.user_data.get('age', 20))
        education = st.selectbox("Education Level", 
                                ["High School", "Bachelor's", "Master's", "PhD"],
                                index=1)
        field_of_study = st.text_input("Field of Study", value=st.session_state.user_data.get('field', ''))
    
    with col2:
        st.subheader("Academic Information")
        university = st.text_input("University/Institution", value=st.session_state.user_data.get('university', ''))
        graduation_year = st.number_input("Expected Graduation Year", 
                                        min_value=2024, max_value=2030, value=2026)
        gpa = st.number_input("GPA (0-10)", min_value=0.0, max_value=10.0, value=7.5, step=0.1)
        experience = st.selectbox("Work Experience", 
                                 ["No Experience", "Internships", "0-2 years", "2-5 years"])
    
    if st.button("Save Profile"):
        st.session_state.user_data.update({
            'name': name,
            'age': age,
            'education': education,
            'field': field_of_study,
            'university': university,
            'graduation_year': graduation_year,
            'gpa': gpa,
            'experience': experience
        })
        st.success("Profile saved successfully!")

# Skills Assessment
def skills_assessment_page():
    st.title("🛠️ Technical Skills Assessment")
    st.markdown("Rate your proficiency level for each skill (1 = Beginner, 7 = Expert)")
    
    advisor = CareerAdvisor()
    technical_scores = {}
    
    # Create skills assessment grid
    col1, col2 = st.columns(2)
    
    skills_left = advisor.technical_skills[:len(advisor.technical_skills)//2]
    skills_right = advisor.technical_skills[len(advisor.technical_skills)//2:]
    
    with col1:
        for skill in skills_left:
            technical_scores[skill] = st.slider(
                skill, 1, 7, 4, 
                key=f"tech_{skill}"
            )
    
    with col2:
        for skill in skills_right:
            technical_scores[skill] = st.slider(
                skill, 1, 7, 4, 
                key=f"tech_{skill}"
            )
    
    # Skills visualization
    if st.button("Analyze Skills"):
        st.subheader("📊 Your Skills Profile")
        
        # Create radar chart
        skills_df = pd.DataFrame(list(technical_scores.items()), 
                               columns=['Skill', 'Proficiency'])
        
        fig = px.bar(skills_df.head(10), x='Skill', y='Proficiency', 
                     title="Top 10 Technical Skills",
                     color='Proficiency',
                     color_continuous_scale='viridis')
        if fig is not None:
            fig.update_xaxis(tickangle=45)


        st.plotly_chart(fig, use_container_width=True)
        
        st.session_state.user_data['technical_skills'] = technical_scores
        st.success("Technical skills assessment completed!")

# Personality Assessment
def personality_assessment_page():
    st.title("🧠 Personality Assessment")
    st.markdown("Answer these questions honestly to understand your personality traits")
    
    # Big Five Personality Test Questions
    personality_questions = {
        "Openness": [
            "I enjoy exploring new ideas and concepts",
            "I am creative and imaginative",
            "I prefer routine and familiar tasks",
            "I am curious about different fields of study"
        ],
        "Conscientiousness": [
            "I am organized and methodical in my work",
            "I complete tasks on time",
            "I pay attention to details",
            "I plan ahead for projects"
        ],
        "Extraversion": [
            "I enjoy working in teams",
            "I am comfortable speaking in public",
            "I prefer working alone",
            "I am energized by social interactions"
        ],
        "Agreeableness": [
            "I enjoy helping others",
            "I am cooperative in group settings",
            "I trust others easily",
            "I avoid conflicts when possible"
        ],
        "Neuroticism": [
            "I remain calm under pressure",
            "I worry about deadlines",
            "I get stressed easily",
            "I handle criticism well"
        ]
    }
    
    personality_scores = {}
    
    for trait, questions in personality_questions.items():
        st.subheader(f"{trait}")
        trait_scores = []
        
        for i, question in enumerate(questions):
            score = st.slider(
                question, 1, 5, 3,
                key=f"{trait}_{i}",
                help="1 = Strongly Disagree, 5 = Strongly Agree"
            )
            # Reverse scoring for negative items
            if "prefer routine" in question or "prefer working alone" in question or "get stressed easily" in question or "worry about" in question:
                score = 6 - score
            trait_scores.append(score)
        
        personality_scores[trait] = np.mean(trait_scores)
    
    if st.button("Complete Personality Assessment"):
        st.subheader("🎯 Your Personality Profile")
        
        # Create personality radar chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=list(personality_scores.values()),
            theta=list(personality_scores.keys()),
            fill='toself',
            name='Your Profile'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[1, 5]
                )),
            showlegend=True,
            title="Personality Traits Profile"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.session_state.user_data['personality_traits'] = personality_scores
        st.success("Personality assessment completed!")

# Career Interest Assessment (RIASEC)
def career_interest_page():
    st.title("🎯 Career Interest Assessment")
    st.markdown("Based on Holland's Career Interest Model (RIASEC)")
    
    riasec_questions = {
        "Realistic": [
            "I enjoy working with tools and machines",
            "I like hands-on problem solving",
            "I prefer practical applications over theory"
        ],
        "Investigative": [
            "I enjoy analyzing data and research",
            "I like solving complex problems",
            "I am curious about how things work"
        ],
        "Artistic": [
            "I enjoy creative and innovative work",
            "I like designing and creating new things",
            "I value self-expression in my work"
        ],
        "Social": [
            "I enjoy helping and teaching others",
            "I like working in team environments",
            "I am motivated by making a positive impact"
        ],
        "Enterprising": [
            "I enjoy leading and managing projects",
            "I like taking on business challenges",
            "I am motivated by achieving goals"
        ],
        "Conventional": [
            "I enjoy organized and structured work",
            "I like following established procedures",
            "I am detail-oriented and systematic"
        ]
    }
    
    interest_scores = {}
    
    for interest, questions in riasec_questions.items():
        st.subheader(f"{interest}")
        interest_score_list = []
        
        for i, question in enumerate(questions):
            score = st.slider(
                question, 1, 5, 3,
                key=f"interest_{interest}_{i}",
                help="1 = Not at all, 5 = Very much"
            )
            interest_score_list.append(score)
        
        interest_scores[interest] = np.mean(interest_score_list)
    
    if st.button("Complete Interest Assessment"):
        st.subheader("📈 Your Interest Profile")
        
        # Create interest bar chart
        interest_df = pd.DataFrame(list(interest_scores.items()), 
                                 columns=['Interest Type', 'Score'])
        
        fig = px.bar(interest_df, x='Interest Type', y='Score',
                     title="Career Interest Profile (RIASEC)",
                     color='Score',
                     color_continuous_scale='plasma')
        st.plotly_chart(fig, use_container_width=True)
        
        st.session_state.user_data['career_interests'] = interest_scores
        st.success("Career interest assessment completed!")

# Career Recommendations
def recommendations_page():
    st.title("🎯 Career Recommendations")
    
    if not all(key in st.session_state.user_data for key in ['technical_skills', 'personality_traits', 'career_interests']):
        st.warning("Please complete all assessments first!")
        return
    
    advisor = CareerAdvisor()
    
    # Get recommendations
    recommendations = advisor.calculate_career_match(
        st.session_state.user_data['technical_skills'],
        st.session_state.user_data['personality_traits'],
        st.session_state.user_data['career_interests']
    )
    
    st.subheader("🏆 Top Career Matches for You")
    
    for i, rec in enumerate(recommendations[:5]):
        with st.expander(f"#{i+1} {rec['career']} - Match Score: {rec['score']:.2f}/7"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Description:** {rec['details']['description']}")
                st.write(f"**Salary Range:** {rec['details']['salary_range']}")
                st.write(f"**Growth Rate:** {rec['details']['growth_rate']}")
                
            with col2:
                st.write(f"**Technical Match:** {rec['tech_match']:.1f}/7")
                st.write(f"**Personality Match:** {rec['personality_match']:.1f}/7")
                st.write("**Key Skills:**")
                for skill in rec['details']['key_skills']:
                    st.write(f"- {skill}")
    
    # Save recommendations to database
    if st.button("Save Recommendations"):
        save_assessment_to_db()
        st.success("Recommendations saved to your profile!")

def save_assessment_to_db():
    conn = sqlite3.connect('career_advisor.db')
    c = conn.cursor()
    
    user_data = st.session_state.user_data
    
    c.execute("""INSERT INTO assessments 
                 (user_id, technical_skills, personality_traits, career_interests, recommendations, created_at)
                 VALUES (?, ?, ?, ?, ?, ?)""",
              (st.session_state.user_id,
               json.dumps(user_data.get('technical_skills', {})),
               json.dumps(user_data.get('personality_traits', {})),
               json.dumps(user_data.get('career_interests', {})),
               json.dumps(user_data.get('recommendations', {})),
               datetime.now()))
    
    conn.commit()
    conn.close()

# Learning Resources
def learning_resources_page():
    st.title("📚 Personalized Learning Resources")
    
    if 'technical_skills' not in st.session_state.user_data:
        st.warning("Please complete the skills assessment first!")
        return
    
    # Identify skill gaps and recommend resources
    technical_skills = st.session_state.user_data['technical_skills']
    
    st.subheader("🎯 Recommended Learning Paths")
    
    # Skills that need improvement (score < 5)
    improvement_skills = {k: v for k, v in technical_skills.items() if v < 5}
    
    learning_resources = {
        "Python Programming": {
            "courses": ["Python for Everybody (Coursera)", "Complete Python Bootcamp (Udemy)"],
            "certifications": ["PCAP – Certified Associate in Python Programming"],
            "projects": ["Build a Web Scraper", "Create a Data Analysis Dashboard"]
        },
        "Machine Learning": {
            "courses": ["Machine Learning by Andrew Ng (Coursera)", "Fast.ai Practical Deep Learning"],
            "certifications": ["Google Machine Learning Engineer"],
            "projects": ["House Price Prediction", "Image Classification Model"]
        },
        "Web Development": {
            "courses": ["The Complete Web Developer Course (Udemy)", "Frontend Masters"],
            "certifications": ["AWS Certified Developer"],
            "projects": ["Personal Portfolio Website", "E-commerce Platform"]
        }
    }
    
    for skill, score in sorted(improvement_skills.items(), key=lambda x: x[1])[:5]:
        with st.expander(f"Improve {skill} (Current: {score}/7)"):
            if skill in learning_resources:
                resource = learning_resources[skill]
                
                st.write("**📖 Recommended Courses:**")
                for course in resource["courses"]:
                    st.write(f"- {course}")
                
                st.write("**🏆 Certifications:**")
                for cert in resource["certifications"]:
                    st.write(f"- {cert}")
                
                st.write("**🛠️ Practice Projects:**")
                for project in resource["projects"]:
                    st.write(f"- {project}")
            else:
                st.write("Customized learning plan coming soon!")

# Progress Tracking
def progress_tracking_page():
    st.title("📊 Progress Tracking")
    
    # Goal Setting
    st.subheader("🎯 Set Learning Goals")
    
    col1, col2 = st.columns(2)
    
    with col1:
        goal_type = st.selectbox("Goal Type", 
                                ["Skill Development", "Certification", "Project Completion", "Job Application"])
        goal_description = st.text_area("Goal Description")
        
    with col2:
        target_date = st.date_input("Target Date")
        priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    
    if st.button("Add Goal"):
        # Save goal to database
        conn = sqlite3.connect('career_advisor.db')
        c = conn.cursor()
        
        c.execute("""INSERT INTO progress 
                     (user_id, goal_type, goal_description, target_date, completion_status, created_at)
                     VALUES (?, ?, ?, ?, ?, ?)""",
                  (st.session_state.user_id, goal_type, goal_description, 
                   str(target_date), "In Progress", datetime.now()))
        
        conn.commit()
        conn.close()
        st.success("Goal added successfully!")
    
    # Display existing goals
    st.subheader("📋 Your Current Goals")
    
    conn = sqlite3.connect('career_advisor.db')
    goals_df = pd.read_sql_query("""SELECT * FROM progress 
                                   WHERE user_id = ? 
                                   ORDER BY created_at DESC""", 
                                conn, params=(st.session_state.user_id,))
    conn.close()
    
    if not goals_df.empty:
        for _, goal in goals_df.iterrows():
            with st.expander(f"{goal['goal_type']}: {goal['goal_description'][:50]}..."):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Target Date:** {goal['target_date']}")
                    st.write(f"**Status:** {goal['completion_status']}")
                
                with col2:
                    new_status = st.selectbox("Update Status", 
                                            ["In Progress", "Completed", "On Hold", "Cancelled"],
                                            key=f"status_{goal['id']}")
                
                with col3:
                    if st.button("Update", key=f"update_{goal['id']}"):
                        conn = sqlite3.connect('career_advisor.db')
                        c = conn.cursor()
                        c.execute("UPDATE progress SET completion_status = ? WHERE id = ?",
                                (new_status, goal['id']))
                        conn.commit()
                        conn.close()
                        st.success("Goal updated!")
                        st.rerun()

# Dashboard
def dashboard_page():
    st.title("📊 Career Development Dashboard")
    
    if not st.session_state.user_data:
        st.warning("Please complete your profile and assessments first!")
        return
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Skills Assessed", len(st.session_state.user_data.get('technical_skills', {})))
    
    with col2:
        avg_skill = np.mean(list(st.session_state.user_data.get('technical_skills', {1: 1}).values()))
        st.metric("Average Skill Level", f"{avg_skill:.1f}/7")
    
    with col3:
        # Count goals from database
        conn = sqlite3.connect('career_advisor.db')
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM progress WHERE user_id = ? AND completion_status = 'In Progress'",
                  (st.session_state.user_id,))
        active_goals = c.fetchone()[0]
        conn.close()
        st.metric("Active Goals", active_goals)
    
    with col4:
        st.metric("Profile Completion", "85%")
    
    # Skills overview chart
    if 'technical_skills' in st.session_state.user_data:
        st.subheader("🛠️ Skills Overview")
        
        skills_data = st.session_state.user_data['technical_skills']
        top_skills = dict(sorted(skills_data.items(), key=lambda x: x[1], reverse=True)[:8])
        
        fig = px.bar(x=list(top_skills.keys()), y=list(top_skills.values()),
                     title="Top Skills Proficiency",
                     labels={'x': 'Skills', 'y': 'Proficiency Level'},
                     color=list(top_skills.values()),
                     color_continuous_scale='viridis')
        if fig is not None:
           fig.update_xaxis(tickangle=45)

        st.plotly_chart(fig, use_container_width=True)
    
    # Recent activity
    st.subheader("📈 Recent Activity")
    st.write("- Completed Technical Skills Assessment")
    st.write("- Updated career interests profile")
    st.write("- Added new learning goal: Complete Python certification")

# Main Application Logic
def main():
    init_database()
    
    if not st.session_state.logged_in:
        authentication_page()
        return
    
    # Sidebar navigation
    st.sidebar.title(f"Welcome, {st.session_state.username}!")
    st.sidebar.markdown("---")
    
    page = st.sidebar.selectbox("Navigation", [
        "🏠 Dashboard",
        "👤 Profile",
        "🛠️ Skills Assessment", 
        "🧠 Personality Test",
        "🎯 Career Interests",
        "🏆 Recommendations",
        "📚 Learning Resources",
        "📊 Progress Tracking"
    ])
    
    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_data = {}
        st.rerun()
    
    # Page routing
    if page == "🏠 Dashboard":
        dashboard_page()
    elif page == "👤 Profile":
        profile_page()
    elif page == "🛠️ Skills Assessment":
        skills_assessment_page()
    elif page == "🧠 Personality Test":
        personality_assessment_page()
    elif page == "🎯 Career Interests":
        career_interest_page()
    elif page == "🏆 Recommendations":
        recommendations_page()
    elif page == "📚 Learning Resources":
        learning_resources_page()
    elif page == "📊 Progress Tracking":
        progress_tracking_page()

if __name__ == "__main__":
    main()
# 🎓 AI Career and Skills Advisor

An intelligent career guidance system built with Streamlit that helps users discover their ideal career paths through comprehensive assessments and personalized recommendations.

## ✨ Features

- **User Authentication**: Secure login and registration system
- **Skills Assessment**: Technical skills proficiency evaluation
- **Personality Testing**: Big Five personality traits analysis
- **Career Interest Assessment**: RIASEC career interest model
- **AI-Powered Recommendations**: Personalized career suggestions
- **Learning Resources**: Customized learning paths and resources
- **Progress Tracking**: Goal setting and achievement monitoring
- **Interactive Dashboard**: Visual analytics and progress overview

## 🚀 Live Demo

[Visit the live application](your-deployed-url-here)

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: SQLite
- **Data Visualization**: Plotly, Matplotlib
- **Machine Learning**: Scikit-learn
- **Data Processing**: Pandas, NumPy

## 📋 Prerequisites

- Python 3.8 or higher
- pip package manager

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-career-advisor.git
cd ai-career-advisor
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

1. Run the application:
```bash
streamlit run main_app.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. Create an account or log in to start your career assessment journey

## 📊 How It Works

1. **Registration/Login**: Create your account and log in securely
2. **Profile Setup**: Complete your personal and academic information
3. **Skills Assessment**: Rate your proficiency in various technical skills
4. **Personality Test**: Answer questions to determine your personality traits
5. **Interest Assessment**: Discover your career interests using the RIASEC model
6. **Get Recommendations**: Receive personalized career suggestions with match scores
7. **Learning Path**: Access customized learning resources and set goals
8. **Track Progress**: Monitor your learning journey and achievements

## 🎯 Career Paths Supported

- Software Developer
- Data Scientist
- Cybersecurity Analyst
- AI Engineer
- Full Stack Developer
- Product Manager

## 📁 Project Structure

```
ai-career-advisor/
├── main_app.py              # Main Streamlit application
├── requirements.txt         # Python dependencies
├── career_advisor.db        # SQLite database (auto-created)
├── .streamlit/
│   └── config.toml         # Streamlit configuration
├── Dockerfile              # Docker configuration
├── Procfile               # Heroku deployment
├── setup.sh               # Heroku setup script
└── README.md              # Project documentation
```

## 🚀 Deployment

### Streamlit Community Cloud
1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy with one click

### Docker
```bash
docker build -t career-advisor .
docker run -p 8501:8501 career-advisor
```

### Heroku
```bash
heroku create your-app-name
git push heroku main
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- Streamlit team for the amazing framework
- Plotly for interactive visualizations
- Scikit-learn for machine learning capabilities
- The open-source community for inspiration and resources

## 📧 Contact

For questions or suggestions, please reach out:
- Email: your.email@example.com
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- GitHub: [@yourusername](https://github.com/yourusername)

---

⭐ **Star this repository if you found it helpful!**
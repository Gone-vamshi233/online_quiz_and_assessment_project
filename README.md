# online_quiz_and_assessment_project
# AI Quiz & Assessment Platform

## Overview

AI Quiz & Assessment Platform is a Flask-based web application that allows administrators to create assessments and students to take quizzes. The platform uses Google Gemini AI to generate quiz questions automatically.

## Features

### Admin

* Admin Login
* Create Assessments
* Generate Assessment Codes
* AI-Based Question Generation
* View Student Results
* Manage Assessments

### Student

* Registration & Login
* Take Assessments Using Assessment Code
* AI Quiz Generation
* Automatic Evaluation
* Score & Percentage Calculation
* Performance Dashboard
* Quiz History Tracking
* Assessment Timer

## Technologies Used

* Python
* Flask
* SQLite
* HTML
* CSS
* Bootstrap 5
* Google Gemini AI
* Jinja2

## Project Structure

ai_quiz/
│
├── app.py
├── quiz.db
├── requirements.txt
├── Procfile
├── templates/
├── static/
└── README.md

## Installation

1. Clone the repository

git clone <repository-url>

2. Install dependencies

pip install -r requirements.txt

3. Create a .env file

GEMINI_API_KEY=your_api_key

4. Run the application

python app.py

## Future Enhancements

* Leaderboard System
* Certificate Generation
* Email Notifications
* Advanced Analytics
* PostgreSQL Integration

## Author

Gone Vamshi

## License

This project is developed for educational and learning purposes.

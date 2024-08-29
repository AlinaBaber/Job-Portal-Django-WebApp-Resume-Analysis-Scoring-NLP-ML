# Job Portal Django WebApp: Resume Analysis & Scoring with NLP and ML

This project is a Django-based web application that focuses on resume analysis and scoring using advanced Natural Language Processing (NLP) techniques and machine learning models, including LSTM-based classification. The web application allows users to upload resumes, which are then analyzed and scored based on their relevance to job descriptions.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [NLP and Machine Learning](#nlp-and-machine-learning)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

In the competitive job market, ensuring that a resume stands out is crucial. This web application automates the process of resume screening by leveraging NLP and machine learning techniques. It analyzes the content of resumes, compares them against job descriptions, and assigns a relevance score. The core of the application is built using Django, with backend processing powered by NLP and LSTM-based models.

## Features
- **Employer/Candidate Account**: Users can create account as employer or Candidate add their information.
- **Employer Dasboard**: Employer can post a job with job description and can create Interview quiz.
- **Candidate Dasboard**: Candidate can add information and search and apply for job and give Interview quiz of that job.
- **Resume Upload**: Users can upload resumes in various formats (PDF, DOCX, etc.).
- **Job Description Matching**: The system compares the uploaded resume with predefined job descriptions.
- **NLP-Based Analysis**: Text analysis is performed using NLP techniques to extract relevant features.
- **LSTM-Based Classification**: A Long Short-Term Memory (LSTM) neural network model classifies resumes based on their relevance.
- **Scoring System**: Resumes are scored based on how well they match the job description and what is the score of the interview quiz given by candidate.
- **User-Friendly Interface**: A simple and intuitive web interface built with Django.

## Technology Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (default) and MySQL (optional, configurable)
- **NLP Libraries**: NLTK, spaCy
- **Machine Learning**: TensorFlow, Keras (for LSTM)
- **Others**: Celery (for background task processing), Redis (as a message broker)

## NLP and Machine Learning

### Natural Language Processing (NLP)

The application uses NLP techniques to parse and analyze the text in resumes. Key steps include:

- **Tokenization**: Breaking down the text into individual words or tokens.
- **Lemmatization**: Reducing words to their base or root form.
- **Vectorization**: Converting text into numerical representations using techniques like TF-IDF.

### LSTM-Based Classification

The core of the resume analysis lies in the LSTM model, which is used to classify resumes based on their relevance to job descriptions. The model is trained on a dataset of resumes and job descriptions, learning patterns that indicate a good match. The scoring system then ranks resumes based on their predicted relevance.

## Installation

To get started with the project:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Job-Portal-Django-WebApp-Resume-Analysis-Scoring-NLP-ML.git
2. Navigate to the project directory:
   ```bash
   cd Job-Portal-Django-WebApp-Resume-Analysis-Scoring-NLP-ML
3. Create and activate a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
5. Configure the database:
SQLite: No additional configuration is required.
MySQL: Update the DATABASES setting in settings.py with your MySQL credentials.
6. Apply migrations to set up the database:
   ```bash
   python manage.py migrate
7. Start the Django development server:
   ```bash
   python manage.py runserver
## Usage
1. Visit the web application in your browser at http://localhost:8000/.
2. Upload a resume and select a job description to compare it against.
3. View the analysis results, including the relevance score and detailed breakdown.

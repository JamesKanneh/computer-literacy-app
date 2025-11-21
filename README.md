# Computer Literacy CLI App 
A beginner-friendly command-line learning tool that teaches computer literacy concepts through interactive lessons, quizzes, and progress tracking.
Includes user accounts, guest mode, multi-level resources, and a rating/feedback system.

## Features

### User System

 Sign Up and securely create an account
 Login with password hashing (SHA-256)
 Guest Mode (no account required)
 Automatic creation of users.json and progress.json

### Learning Resources

#### Three difficulty tiers:

 A - Beginner: Computer basics, input/output devices, OS, memory, internet fundamentals
 B - Intermediate: Networks, storage, CPU, file systems, security
 C - Advanced: Protocols, databases, cybersecurity, virtualization, cloud computing

Each topic includes an easy-to-read explanation and real-world examples.

### Interactive Quizzes

 Separate quiz sets for each difficulty level
 Instant feedback on correct/incorrect answers
 Save quiz scores per user (except Guest mode)
 Ability to exit quizzes midway

#### Progress Tracking

Your latest quiz scores are stored in progress.json so you can track improvement over time.

### Rating & Feedback

At the end of the app, users can:
 Rate the app (1-5)
 Provide suggestions for improvement
 Receive personalized responses based on their rating

## Installation

- Clone GitHub Repo:
 https://github.com/your-username/your-repo-name

- Requirements

 Python 3
 No external libraries required (standard library only)

- Run the Application
   python3 comp_lit_app.py

The app will automatically generate required data files on first run.

## How to Use

- Launch the App

Choose:

 Sign Up -- create a new account
 Login -- access your saved progress
 Guest Mode -- explore without saving
 Exit

- Main Menu

Once logged in or in guest mode:

1) View Resources  
2) Take Quiz  
3) Logout  
4) Exit

- Learning Resources

Select a difficulty - choose a topic - read notes.

- Quizzes

Pick a difficulty - answer multiple-choice questions - view score - progress is saved (unless guest).

- Rate the App

After closing the program:
 Enter a rating (1-5)
 Optionally provide feedback
 Enjoy the closing message

 ### Security

 Passwords are stored hashed with SHA-256 (never in plain text).
User data is stored locally on your machine in JSON format.
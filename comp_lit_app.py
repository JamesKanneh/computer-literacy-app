#!/usr/bin/env python3
"""
Computer Literacy CLI App - Mini Course Version
Includes guest mode, quizzes, and enriched resources.
"""

import json
import os
import hashlib
import getpass
import datetime

USERS_FILE = "users.json"
PROGRESS_FILE = "progress.json"

# Resources and Quiz content
RESOURCES = {
    "A": [  # Beginner
        {"title": "What is a Computer?", 
         "notes": "A computer is a device that processes information and performs tasks according to instructions. "
                  "It can store, retrieve, and manipulate data.\n\n"
                  "Example: Using a calculator app to add numbers is an example of a computer processing input to give output."},

        {"title": "Input Devices", 
         "notes": "Devices like Keyboard, Mouse, and Scanner allow users to input data into a computer. Each has a specific purpose.\n\n"
                  "Example: Typing a document uses a keyboard as input; clicking icons uses a mouse."},

        {"title": "Output Devices", 
         "notes": "Devices like Monitor, Printer, and Speakers display or produce results from a computer.\n\n"
                  "Example: Watching a video on a monitor or printing a photo are output tasks."},

        {"title": "Memory Basics", 
         "notes": "RAM (Random Access Memory) stores data temporarily for programs currently running. ROM (Read-Only Memory) stores essential instructions permanently.\n\n"
                  "Example: Opening a web browser uses RAM, while your computer BIOS is stored in ROM."},

        {"title": "Operating System", 
         "notes": "OS is system software that manages hardware and software resources, enabling programs to run.\n\n"
                  "Example: Windows, macOS, and Linux manage files, run apps, and control the keyboard/mouse."},

        {"title": "File and Folder Basics", 
         "notes": "Files store data; folders organize files to make them easier to access.\n\n"
                  "Example: A Word document is a file, while a folder may contain multiple documents organized by topic."},

        {"title": "Basic Internet Concepts", 
         "notes": "The internet is a global network connecting millions of computers for communication and data sharing.\n\n"
                  "Example: Sending an email uses the internet to transmit your message to another user."}
    ],
    "B": [  # Intermediate
        {"title": "Computer Networks", 
         "notes": "LAN (Local Area Network) and WAN (Wide Area Network) connect computers to share data and resources.\n\n"
                  "Example: Office computers connected to a printer form a LAN; accessing a website is using WAN."},

        {"title": "File Systems", 
         "notes": "File systems like NTFS, FAT32, and ext4 determine how data is stored and retrieved on disks.\n\n"
                  "Example: NTFS supports large files and security permissions, while FAT32 is compatible with older devices."},

        {"title": "Software Types", 
         "notes": "System software like OS manages hardware; application software like Word or Chrome perform specific tasks.\n\n"
                  "Example: Windows is system software, while Microsoft Word is application software."},

        {"title": "CPU Basics", 
         "notes": "CPU executes instructions. Its speed (GHz), cores, and cache size affect performance.\n\n"
                  "Example: A quad-core CPU can handle multiple applications simultaneously better than a single-core CPU."},

        {"title": "Data Storage", 
         "notes": "HDD, SSD, and Cloud Storage store data differently. HDD is mechanical and slower; SSD is faster; cloud stores online.\n\n"
                  "Example: Saving a file to Google Drive is using cloud storage; saving to your PC is local storage."},

        {"title": "Security Essentials", 
         "notes": "Use strong passwords, antivirus, and avoid suspicious links to protect your computer.\n\n"
                  "Example: Never open email attachments from unknown sources to prevent malware."},

        {"title": "Basic Troubleshooting", 
         "notes": "Restarting, checking connections, and reading error messages can fix many issues.\n\n"
                  "Example: If Wi-Fi doesn't work, check your router, reconnect, and restart the device."}
    ],
    "C": [  # Advanced
        {"title": "Networking Protocols", 
         "notes": "Protocols like TCP/IP, HTTP, and FTP define rules for device communication.\n\n"
                  "Example: Browsing a website uses HTTP/HTTPS, while transferring files between computers can use FTP."},

        {"title": "Databases", 
         "notes": "SQL (relational) and NoSQL (non-relational) databases organize and manage data efficiently.\n\n"
                  "Example: A library catalog may use SQL tables; a social media feed may use NoSQL for dynamic posts."},

        {"title": "Programming Basics", 
         "notes": "Programming uses variables, loops, functions, and algorithms to tell computers what to do.\n\n"
                  "Example: A Python program that calculates the sum of numbers in a list demonstrates a loop and function."},

        {"title": "Cybersecurity", 
         "notes": "Cybersecurity protects data via firewalls, encryption, and authentication.\n\n"
                  "Example: Two-factor authentication adds an extra security step when logging into your email."},

        {"title": "Computer Architecture", 
         "notes": "Architecture includes CPU, GPU, ALU, registers, and pipelines; it determines execution efficiency.\n\n"
                  "Example: GPUs speed up graphics rendering; CPU ALU handles arithmetic operations."},

        {"title": "Cloud Computing", 
         "notes": "Cloud computing offers servers, storage, databases, and software over the Internet.\n\n"
                  "Example: Google Docs lets you create and store documents online without local installation."},

        {"title": "Virtualization", 
         "notes": "Virtualization allows one physical machine to run multiple virtual machines.\n\n"
                  "Example: Using VirtualBox to run Linux on a Windows PC for testing software."}
    ]
}


QUIZZES = {
    "A": [
        {"q": "What is a computer?", "options": ["A device to process information", "A type of phone", "A kitchen appliance"], "ans": 1},
        {"q": "Which is an input device?", "options": ["Monitor", "Printer", "Keyboard"], "ans": 3},
        {"q": "Which is an output device?", "options": ["Mouse", "Printer", "Keyboard"], "ans": 2},
        {"q": "RAM stands for?", "options": ["Random Access Memory", "Read After Memory", "Run All Modules"], "ans": 1},
        {"q": "What does OS stand for?", "options": ["Open Software", "Output Signal", "Operating System" ], "ans": 3},
    ],
    "B": [
        {"q": "What is LAN?", "options": ["Large Access Node", "Long Application Network", "Local Area Network"], "ans": 3},
        {"q": "Which is system software?", "options": ["Microsoft Word", "Windows OS", "Chrome"], "ans": 2},
        {"q": "Which is permanent storage?", "options": ["RAM", "HDD", "Cache"], "ans": 2},
        {"q": "CPU stands for?", "options": ["Central Processing Unit", "Computer Power Unit", "Control Processing Utility"], "ans": 1},
        {"q": "SSD is?", "options": ["Temporary storage", "Solid State Drive", "Software Storage Device"], "ans": 2},
    ],
    "C": [
        {"q": "What is TCP/IP used for?", "options": ["Storage","Networking", "Programming"], "ans": 2},
        {"q": "SQL is used for?", "options": ["Database queries", "Memory management", "Networking"], "ans": 1},
        {"q": "What is encryption?", "options": ["Data encoding for security", "Virus software", "Hardware device"], "ans": 1},
        {"q": "CPU contains?", "options": ["ALU", "Registers", "Both ALU and Registers"], "ans": 3},
        {"q": "Firewall is used for?", "options": ["Data storage","Security", "Processing"], "ans": 2},
    ]
}

# Helper functions
def ensure_files():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)
    if not os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "w") as f:
            json.dump({}, f)

def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def load_progress():
    with open(PROGRESS_FILE, "r") as f:
        return json.load(f)

def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)

def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

# Authentication functions
def signup():
    users = load_users()
    print("\n=== Sign Up ===")
    username = input("Choose a username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return None
    if username in users:
        print("Username exists. Try login.")
        return None
    pw = getpass.getpass("Choose password: ").strip()
    if not pw:
        print("Password cannot be empty.")
        return None
    pw2 = getpass.getpass("Confirm password: ").strip()
    if pw != pw2:
        print("Passwords did not match.")
        return None
    users[username] = {"password": hash_password(pw), "created_at": datetime.datetime.utcnow().isoformat()+"Z"}
    save_users(users)
    print(f"Account created for '{username}'. You can now log in.")

def login():
    users = load_users()
    print("\n=== Login ===")
    username = input("Username: ").strip()
    if username not in users:
        print("No such user. Please sign up first.")
        return None
    pw = getpass.getpass("Password: ").strip()
    if hash_password(pw) == users[username]["password"]:
        print(f"Welcome, {username}!")
        return username
    else:
        print("Incorrect password.")
        return None

# Accessing Resources
def view_resources():
    while True:
        print("\n=== Learning Resources ===")
        print("Choose difficulty (or type 'exit' to go back):")
        print("A) Beginner  B) Intermediate  C) Advanced")
        diff = input("Your choice: ").strip().upper()
        if diff.lower() == "exit":
            break
        if diff not in RESOURCES:
            print("Invalid choice.")
            continue

        topics = RESOURCES[diff]
        while True:
            print(f"\n=== {diff} Level Resources ===")
            for idx, t in enumerate(topics, 1):
                print(f"{idx}. {t['title']}")
            choice = input("Enter resource ID to read or type 'exit' to go back: ").strip()
            if choice.lower() == "exit":
                break
            if choice.isdigit():
                idx = int(choice)-1
                if 0 <= idx < len(topics):
                    print(f"\n{topics[idx]['title']}:\n{topics[idx]['notes']}")
                else:
                    print("Invalid resource number.")
            else:
                print("Invalid input.")

# Accessing Quiz 
def take_quiz(current_user):
    print("\nChoose difficulty for quiz: A) Beginner  B) Intermediate  C) Advanced")
    diff = input("Your choice: ").strip().upper()
    if diff not in QUIZZES:
        print("Invalid choice.")
        return
    quiz = QUIZZES[diff]
    score = 0
    print("Type 'exit' at any time to go back to the main menu.\n")
    
    for q in quiz:
        print(f"\n{q['q']}")
        for i, opt in enumerate(q['options'], 1):
            print(f"{i}. {opt}")
        ans = input("Your answer (1-3): ").strip()
        
        if ans.lower() == "exit":
            print("Exiting quiz...")
            break
        
        if ans.isdigit() and int(ans) == q['ans']:
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! Correct answer: {q['ans']}. {q['options'][q['ans']-1]}")
    
    print(f"\nYour score: {score}/{len(quiz)} (partial if exited early)")
    
    if current_user != "Guest":
        progress = load_progress()
        user_progress = progress.get(current_user, {})
        user_progress[diff] = score
        progress[current_user] = user_progress
        save_progress(progress)
        print("Progress saved.")

# User Menu 
def main_menu():
    ensure_files()
    current_user = None
    while True:
        print("\n=== Computer Literacy Hub ===")
        if current_user:
            print(f"Logged in as: {current_user}")
            print("1) View Resources")
            print("2) Take Quiz")
            print("3) Logout")
            print("4) Exit")
            choice = input("Choose (1-4): ").strip()
            if choice == "1":
                view_resources()
            elif choice == "2":
                take_quiz(current_user)
            elif choice == "3":
                print(f"User '{current_user}' logged out.")
                current_user = None
            elif choice == "4":
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
        else:
            print("1) Sign Up")
            print("2) Login")
            print("3) Continue as Guest")
            print("4) Exit")
            choice = input("Choose (1-4): ").strip()
            if choice == "1":
                signup()
            elif choice == "2":
                user = login()
                if user:
                    current_user = user
            elif choice == "3":
                current_user = "Guest"
                print("Continuing as Guest...")
            elif choice == "4":
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting. Goodbye!")

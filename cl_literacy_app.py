#!/usr/bin/env python3
"""
cl_literacy_app.py
Menu-driven command-line app to educate the young generation on computer literacy.
Features:
 - Sign up / Login (password hashed)
 - Add resource (title, description, level, tags)
 - View all resources
 - Search by level or tag
 - Simple JSON persistence: users.json, resources.json
"""

import json
import os
import hashlib
import getpass
import datetime
from typing import Dict, List

USERS_FILE = "users.json"
RESOURCES_FILE = "resources.json"

"""
cl_literacy_app.py
Menu-driven command-line app to educate the young generation on computer literacy.
Features:
 - Sign up / Login (password hashed)
 - Add resource (title, description, level, tags)
 - View all resources
 - Search by level or tag
 - Simple JSON persistence: users.json, resources.json

Edited by Nziza
"""


def load_users() -> Dict[str, dict]:
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(users: Dict[str, dict]):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def load_resources() -> List[dict]:
    with open(RESOURCES_FILE, "r") as f:
        return json.load(f)


def save_resources(resources: List[dict]):
    with open(RESOURCES_FILE, "w") as f:
        json.dump(resources, f, indent=2)


def hash_password(password: str) -> str:
    # Simple sha256 hashing. For production use a stronger scheme (bcrypt/scrypt) + salt.
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def signup():
    users = load_users()
    print("\n=== Sign Up ===")
    username = input("Choose a username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return None
    if username in users:
        print("That username already exists. Try logging in or choose another username.")
        return None
    # Use getpass so password not echoed where supported
    pw = getpass.getpass("Choose a password: ").strip()
    if not pw:
        print("Password cannot be empty.")
        return None
    pw2 = getpass.getpass("Confirm password: ").strip()
    if pw != pw2:
        print("Passwords did not match.")
        return None
    users[username] = {
        "password": hash_password(pw),
        "created_at": datetime.datetime.utcnow().isoformat() + "Z"
    }
    save_users(users)
    print(f"Account created for '{username}'. You can now log in.")
    return None


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
"""
    Prompt the user to log in.
    Returns the username if successful; otherwise, returns None.
    """

def add_resource(current_user: str):
    if not current_user:
        print("You must be logged in to add resources.")
        return
    print("\n=== Add a Computer Literacy Resource ===")
    title = input("Title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    description = input("Short description (one or two lines): ").strip()
    level = input("Level (Beginner / Intermediate / Advanced): ").strip().capitalize()
    tags_raw = input("Tags (comma-separated, e.g. typing,hardware): ").strip()
    tags = [t.strip().lower() for t in tags_raw.split(",") if t.strip()]
    resources = load_resources()
    new_res = {
        "id": len(resources) + 1,
        "title": title,
        "description": description,
        "level": level or "Beginner",
        "tags": tags,
        "author": current_user,
        "created_at": datetime.datetime.utcnow().isoformat() + "Z"
    }
    resources.append(new_res)
    save_resources(resources)
    print(f"Resource '{title}' added. (id={new_res['id']})")


def view_resources():
    print("\n=== All Resources ===")
    resources = load_resources()
    if not resources:
        print("No resources saved yet.")
        return
    for r in resources:
        print(f"\nID: {r['id']}")
        print(f"Title: {r['title']}")
        print(f"Level: {r.get('level','')}")
        print(f"Author: {r.get('author','')}")
        print(f"Tags: {', '.join(r.get('tags',[]))}")
        print(f"Description: {r.get('description','')}")
        print(f"Added: {r.get('created_at','')}")


def search_resources():
    resources = load_resources()
    if not resources:
        print("No resources saved yet.")
        return
    print("\nSearch by: 1) Level  2) Tag  3) Author")
    choice = input("Choose (1/2/3): ").strip()
    if choice == "1":
        level = input("Enter level (Beginner / Intermediate / Advanced): ").strip().capitalize()
        matches = [r for r in resources if r.get("level","").lower() == level.lower()]
    elif choice == "2":
        tag = input("Enter tag (e.g. typing): ").strip().lower()
        matches = [r for r in resources if tag in [t.lower() for t in r.get("tags",[])]]
    elif choice == "3":
        author = input("Enter author username: ").strip()
        matches = [r for r in resources if r.get("author","") == author]
    else:
        print("Invalid choice.")
        return

    if not matches:
        print("No resources matched your search.")
        return
    print(f"\nFound {len(matches)} match(es):")
    for r in matches:
        print(f"- [{r['id']}] {r['title']} (Level: {r.get('level')}) by {r.get('author')}")




if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting. Goodbye!")

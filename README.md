# 📀 MySQL Database Cloner

A Python-based command-line tool to **clone and recreate MySQL databases** without relying on paid cloud hosting.  
It generates a standalone Python script containing all the necessary MySQL connectivity and SQL queries to rebuild the database anywhere.

---

## 🚀 Features

- **Cross-System Database Transfer** – Move databases between machines without hosting.
- **Full Backup in a Python File** – Generates a `.py` file that can recreate your database from scratch.
- **Custom Save Location** – Save the generated file in the current directory or a user-specified path.
- **Credential Customization** – Embed `host`, `user`, and `password` directly into the generated script.
- **MySQL Integration** – Works with existing MySQL servers and databases.

---

## 📌 Use Case

Originally designed to solve a personal problem during my **12th-grade Computer Science project**:  
Our school computers had the updated database, but I couldn’t work on it at home without setting up costly online hosting.  
The solution? Generate a Python file containing the database so I could **email it** to myself, run it at home, and restore my work instantly.

---

## 🛠️ Technologies Used

- **Python** – CLI frontend
- **MySQL** – Database backend
- **MySQL Connector/Python** – For database connectivity
- **File Handling** – To write the generated script

---

## 📋 Prerequisites

Before running Database Cloner, ensure you have:

- **Python 3.6+**
- **MySQL Server** (installed and running locally or remotely)
- **mysql-connector-python** module:
  ```bash
  pip install mysql-connector-python

---

## 📂 How It Works
 - 1. Prompt for Database Name – Checks if it exists.
 - 2. Ask for Save Location
      - 1. Current directory
      - 2. Fully-specified custom path
 - 3. Generate Python File – Embeds:
      - 1. MySQL connection setup
      - 2. All table creation & insertion queries
 - 4. Run Anywhere – Execute the generated file to recreate the database.
---

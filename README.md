# Data Bridge 🚀  

**Data Bridge** is a developer-friendly utility that simplifies moving data between **CSV files, MySQL databases, and Python connectivity files**.  

It started from a classroom curiosity and grew into a complete tool with logging support for faster debugging.

---

## ✨ Features  

- **CSV → Python connectivity file**  
  - Uses the first row as column headings and subsequent rows as records.  
  - Infers datatypes by checking column values.  
  - If all values are `NULL`, defaults to `VARCHAR(20)`.  
  - Ignores constraints, focuses only on column names and values.  

- **MySQL ↔ CSV**  
  - Export a MySQL table into a CSV file.  
  - Import a CSV file into a MySQL table in the specified database.  

- **Database ↔ ZIP**  
  - Export a database as a `.zip` (each table saved as `table_name.csv`).  
  - Import a `.zip` back into a MySQL database.  

- **ZIP → Python connectivity file**  
- **MySQL database → Python connectivity file**  

- **Error handling in imports**  
  - If no valid records are found to infer datatypes, Data Bridge prompts the user:  
    - *Enter datatypes manually* (with size).  
    - *Skip the file* and move on.  

- **Logging system (`dataBridge.log`)**  
  - Tracks all files created by the utility.  
  - Logs errors with timestamps.  
  - Helps developers debug faster instead of manually searching for issues.
 
## 📋 Prerequisites

Before running Database Cloner, ensure you have:

- **Python 3.6+**
- **MySQL Server** (installed and running locally or remotely)
- **mysql-connector-python** module:
  ```bash
  pip install mysql-connector-python
- **tabulate** module:
  ```bash
  pip install tabulate


---

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

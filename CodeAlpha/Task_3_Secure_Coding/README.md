# 💻 TASK 03: SECURE CODING REVIEW & VULNERABILITY REMEDIATION 🛡️

## 📝 Project Overview
In the modern threat landscape, writing code that "just works" is not enough. This project demonstrates a **Secure Coding Review** of an authentication system. The goal was to identify critical vulnerabilities such as **SQL Injection (SQLi)** and implement robust countermeasures to protect user data integrity.

---

## 🛠️ How It Works (Technical Defense)
The implementation focuses on moving away from insecure, dynamic queries to a more resilient architecture:

1. **Parameterized Queries:** We eliminated SQL Injection by using placeholders (`?`) instead of string formatting, ensuring the database treats input as data, not executable code.
2. **Static Analysis:** Conducted a manual audit of the authentication logic to identify logic flaws.
3. **Database Security:** Designed a secure interaction layer for the `frank_vault.db` using SQLite3 best practices.

---

## 🏗️ Technical Architecture:
| Component | Security Feature |
| :--- | :--- |
| **Authentication Engine** | Parameterized SQL to block Injection attacks. |
| **Security Test Suite** | Automated scripts to verify login security. |
| **Data Storage** | Structured SQLite database with restricted access logic. |

---

## 🚀 Key Files & Usage:
- `frank_secure_auth.py`: The core secure authentication logic.
- `frank_security_test.py`: Automated security testing script.
- `from frank_secure_auth import app`: Integration bridge for the application.

---

## 👤 Project Developed By:
- **Name:** Frank Karani 🏆
- **Title:** Cybersecurity Developer & Analyst
- **Institution:** Institute of Accountancy Arusha (IAA)
- **Email:** frankkarani146@gmail.com 📧
- **LinkedIn:** [Frank Karani Profile](https://www.linkedin.com/in/frank-karani-47971b3b5) 🔗

---
> *"Code is either secure by design or insecure by default. I choose design."* 🛡️💻

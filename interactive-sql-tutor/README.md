# SQL Practice Platform

This is a full-stack web application designed to provide a LeetCode-like experience for practicing SQL problems. It allows students to submit SQL queries, get instant feedback, view hints, and track their progress.

## 🌐 Live Deployment

Frontend: [https://main.dz7dhpwoo2vvg.amplifyapp.com](https://main.dz7dhpwoo2vvg.amplifyapp.com)  
Backend API: [https://db-group7-451621.uw.r.appspot.com](https://db-group7-451621.uw.r.appspot.com)

## 🚀 Features

- 🔒 JWT authentication using SimpleJWT
- 🧠 Role-based access control (`Student`, `Instructor`, `Admin`)
- 🧩 Dynamic SQL sandbox to safely validate queries
- 📦 Problem/hint management for instructors
- 📈 User submission tracking and scoring
- 🌍 Deployed on **Google Cloud Platform** (App Engine + Cloud SQL)
- 🎯 Frontend hosted via **AWS Amplify**

## 🧱 Tech Stack

- **Backend:** Django, Django REST Framework
- **Frontend:** React (hosted externally)
- **Database:** MySQL (GCP Cloud SQL)
- **Auth:** JWT (via `rest_framework_simplejwt`)
- **Deployment:** GCP App Engine, GCP SQL, AWS Amplify

## 🗂️ Project Structure
```bash
project/
├── users/           # Custom user model and authentication logic
├── sql_app/         # Models and logic for SQL problems, query sandbox execution
├── llm/             # Modles and logic for AI chat box and AI hint
├── analytics/       # Tracks user attempts, scores, and performance data
├── config/          # Database config utilities and environment loading helpers
├── scripts/         # Admin utilities for importing and managing SQL problems
├── problems/        # Individual SQL problem folders (metadata, problem.sql, solution.sql)
├── requirements.txt # Python dependencies
├── app.yaml         # GCP App Engine deployment configuration
```

## 🧪 Sample SQL Problem Format

* Each SQL problem is stored under `problems/{id}`/ with:

* `metadata.json`: problem description, hints, table schema

* `problem.sql`: DDL + sample data (used in sandbox)

* `solution.sql`: the correct query for comparison

## 📚 References

- [Django REST Framework](https://www.django-rest-framework.org/)
- [JWT Authentication](https://medium.com/swlh/all-you-need-to-know-about-json-web-token-jwt-8a5d6131157f)
- [GCP Full-Stack Deployment](https://faun.pub/deploying-a-full-stack-app-on-google-cloud-platform-a-step-by-step-guide-c69154770705)

## 🧠 Future Improvements

* CI/CD pipeline with GitHub Actions

* Rate limiting to prevent abuse

* Admin dashboard for submission analytics

* Public problem repository export

## 📜 License
* This repository is intended solely for educational and academic purposes. Commercial use, reproduction, or distribution is not permitted without explicit permission.
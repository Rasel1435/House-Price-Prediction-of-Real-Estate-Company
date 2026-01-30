---
title: House Price Prediction
emoji: 🏠
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
description: A data science project to build a real estate price prediction website using machine learning and web development technologies.
---

[![CI/CD to Docker Hub](https://github.com/Rasel1435/House-Price-Prediction-of-Real-Estate-Company/actions/workflows/main.yml/badge.svg)](https://github.com/Rasel1435/House-Price-Prediction-of-Real-Estate-Company/actions)
[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/rasel1435/house-price-prediction)

# LuxEstate: House Price Prediction

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

> 🚀 **Live Demo:** [Try LuxEstate on Hugging Face Spaces](https://huggingface.co/spaces/rasel1435/house-price-prediction)

> A comprehensive end-to-end machine learning pipeline that predicts real estate prices in Bangalore using Linear Regression. Features a sleek web interface and a fully automated DevOps pipeline.

## 🚀 Quick Start (Docker)

The fastest way to run this predictor locally is using Docker. No Python installation required:

```bash
docker pull rasel143x/house-price-prediction:latest
docker run -p 8000:7860 rasel143x/house-price-prediction:latest
```

**Then open your browser and go to** `http://localhost:8000`.

## 📌 Project Overview

This project predicts home prices based on square footage, number of bedrooms (BHK), and location.

- Model: Linear Regression trained on the Bangalore Home Prices dataset.
- Workflow: Data cleaning, outlier removal (price per sqft & BHK), and hyperparameter tuning via GridSearchCV.
- Pipeline: Automated ETL and model artifact generation.

## 🏗️ DevOps & Automation

This project is fully automated using CI/CD:

- GitHub Actions: Automatically builds Docker images on every push.
- Docker Hub: Fresh images are pushed to rasel143x/house-price-prediction.
- Hugging Face Sync: Automated deployment to Spaces via Git integration.

## 🛠️ Tech Stack

- Language: Python 3.10
- Libraries: Pandas, Numpy, Matplotlib, Scikit-Learn
- Server: Flask + Gunicorn
- Containerization: Docker
- CI/CD: GitHub Actions

## ⚙️ Installation & Setup

1. Clone & Environment

```bash
git clone https://github.com/Rasel1435/House-Price-Prediction-of-Real-Estate-Company.git
cd House-Price-Prediction-of-Real-Estate-Company
python3 -m venv venv
source venv/bin/activate
```
2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 📊 Model Performance

The model was optimized using ShuffleSplit cross-validation and GridSearchCV.

- Primary Model: Linear Regression
- Accuracy: ~85% R² score on test data.

## 🤝 Contact

Created by Sheikh Rasel Ahmed

- LinkedIn: Sheikh Rasel Ahmed: [https://www.linkedin.com/in/shekhnirob1](https://www.linkedin.com/in/shekhnirob1)
- Portfolio: Website: [https://rasel1435.github.io/Sheikh-Rasel-Ahmed-Resume](https://rasel1435.github.io/Sheikh-Rasel-Ahmed-Resume/)

---

### 🚀 How to Save and Update

1. **Open your local `README.md`** and replace everything with the text above.
2. **Push to GitHub & Hugging Face**:
```bash
git add README.md
git commit -m "style: revamp README with professional badges and HF metadata"
git push origin main
git push hf main --force
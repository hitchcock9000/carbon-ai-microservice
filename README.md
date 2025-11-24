# 🌍 Carbon Footprint AI Microservice

> **End-to-End Data Science & Machine Learning Project**  
> Intelligent carbon emissions prediction and sustainability optimization system

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Business Problem](#-business-problem)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Models & Methodology](#-models--methodology)
- [Results](#-results)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Project Overview

This project is a comprehensive **AI-powered microservice** that predicts carbon emissions and provides intelligent sustainability recommendations for hotels and businesses. It combines **Machine Learning**, **Deep Learning**, and **Generative AI** to deliver actionable insights for reducing environmental impact.

### Key Objectives

✅ Predict carbon emissions based on operational metrics  
✅ Classify businesses by sustainability performance  
✅ Forecast future emission trends using time-series analysis  
✅ Provide AI-powered recommendations via RAG chatbot  
✅ Analyze building efficiency through computer vision  
✅ Generate automated sustainability reports  

---

## 💼 Business Problem

**Challenge**: Hotels and businesses struggle to accurately predict their carbon footprint and identify effective reduction strategies.

**Solution**: An intelligent microservice that:
- Predicts emissions with high accuracy using ML/DL models
- Provides personalized, data-driven sustainability recommendations
- Enables real-time monitoring and forecasting
- Offers an AI chatbot for instant sustainability guidance

**Impact**: Help organizations reduce their carbon footprint by 15-30% through data-driven decision making.

---

## ✨ Features

### 🤖 Machine Learning
- **Regression Models**: Predict carbon emissions (Random Forest, XGBoost, LightGBM)
- **Classification**: Categorize sustainability levels (A-F rating)
- **Time Series**: ARIMA, Prophet, and LSTM for emission forecasting
- **Clustering**: K-Means for consumption pattern analysis

### 🧠 Deep Learning
- **LSTM Networks**: Advanced time-series prediction
- **CNN for Computer Vision**: Building efficiency analysis from images
- **Transformer Models**: State-of-the-art forecasting
- **Anomaly Detection**: Identify unusual consumption patterns

### 💬 Generative AI
- **RAG Chatbot**: LangChain-powered sustainability assistant
- **LLM Recommendations**: GPT-4 powered personalized strategies
- **Automated Reports**: Generate comprehensive sustainability reports
- **Voice Interface**: Speech-to-text and text-to-speech capabilities

### 📊 Data & Visualization
- **Tableau Dashboard**: Interactive insights and KPIs
- **SQL Database**: Structured data storage and queries
- **RESTful API**: FastAPI endpoints for easy integration
- **Real-time Analytics**: Live prediction and monitoring

---

## 🛠️ Tech Stack

### Core Technologies
- **Python 3.9+**: Primary programming language
- **FastAPI**: High-performance REST API framework
- **PostgreSQL**: Relational database for structured data
- **Docker**: Containerization for deployment

### Machine Learning & Data Science
- **scikit-learn**: Traditional ML algorithms
- **XGBoost / LightGBM**: Gradient boosting models
- **TensorFlow / Keras**: Deep learning framework
- **PyTorch**: Alternative DL framework
- **Prophet**: Time-series forecasting
- **Pandas / NumPy**: Data manipulation
- **Matplotlib / Seaborn / Plotly**: Visualization

### Generative AI
- **LangChain**: LLM orchestration framework
- **OpenAI GPT-4**: Language model for recommendations
- **Hugging Face Transformers**: Open-source models
- **ChromaDB / FAISS**: Vector database for RAG
- **Whisper**: Speech-to-text
- **ElevenLabs / gTTS**: Text-to-speech

### DevOps & Tools
- **Git / GitHub**: Version control
- **Jupyter Notebooks**: Exploratory data analysis
- **Tableau**: Business intelligence visualization
- **pytest**: Testing framework
- **Docker Compose**: Multi-container orchestration

---

## 📁 Project Structure

```
carbon-ai-microservice/
│
├── 📊 data/                          # Data storage
│   ├── raw/                          # Original, immutable data
│   ├── processed/                    # Cleaned and transformed data
│   └── external/                     # External datasets (weather, etc.)
│
├── 📓 notebooks/                     # Jupyter notebooks
│   ├── 01_eda/                       # Exploratory Data Analysis
│   ├── 02_preprocessing/             # Data cleaning and feature engineering
│   ├── 03_modeling/                  # Model training and experimentation
│   └── 04_evaluation/                # Model evaluation and comparison
│
├── 🤖 models/                        # Trained models
│   ├── ml/                           # Machine learning models
│   ├── dl/                           # Deep learning models
│   └── genai/                        # GenAI models and embeddings
│
├── 🔬 src/                           # Source code
│   ├── data_processing/              # ETL pipelines
│   │   ├── __init__.py
│   │   ├── data_loader.py
│   │   ├── preprocessing.py
│   │   └── feature_engineering.py
│   │
│   ├── ml_models/                    # ML model implementations
│   │   ├── __init__.py
│   │   ├── regression.py
│   │   ├── classification.py
│   │   ├── time_series.py
│   │   └── clustering.py
│   │
│   ├── dl_models/                    # Deep learning models
│   │   ├── __init__.py
│   │   ├── lstm.py
│   │   ├── cnn_vision.py
│   │   └── transformer.py
│   │
│   ├── genai/                        # Generative AI components
│   │   ├── __init__.py
│   │   ├── rag_chatbot.py
│   │   ├── llm_recommendations.py
│   │   ├── report_generator.py
│   │   └── voice_interface.py
│   │
│   └── api/                          # FastAPI application
│       ├── __init__.py
│       ├── main.py
│       ├── routes/
│       ├── schemas/
│       └── dependencies.py
│
├── 🗄️ database/                      # Database files
│   ├── schemas/                      # SQL schemas
│   └── migrations/                   # Database migrations
│
├── 📊 tableau/                       # Tableau workbooks
│   └── carbon_insights.twb
│
├── 🎨 webapp/                        # Optional frontend
│   └── (Streamlit or React app)
│
├── 🐳 docker/                        # Docker configurations
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── 📋 tests/                         # Unit and integration tests
│   ├── test_data_processing.py
│   ├── test_models.py
│   └── test_api.py
│
├── 🎯 presentation/                  # Final presentation materials
│   ├── slides.pdf
│   └── demo_screenshots/
│
├── 📄 .gitignore                     # Git ignore file
├── 📄 requirements.txt               # Python dependencies
├── 📄 README.md                      # This file
└── 📄 LICENSE                        # MIT License

```

---

## 🚀 Installation

### Prerequisites
- Python 3.9 or higher
- PostgreSQL 13+ (optional, for database features)
- Git

### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/carbon-ai-microservice.git
cd carbon-ai-microservice
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys and configurations
```

5. **Initialize database** (optional)
```bash
python src/database/init_db.py
```

6. **Run the API**
```bash
uvicorn src.api.main:app --reload
```

The API will be available at `http://localhost:8000`

---

## 📖 Usage

### Running Jupyter Notebooks

```bash
jupyter notebook notebooks/
```

Start with `01_eda/exploratory_analysis.ipynb` for data exploration.

### Making API Requests

**Predict Emissions**
```bash
curl -X POST "http://localhost:8000/api/v1/predict/emissions" \
  -H "Content-Type: application/json" \
  -d '{
    "energy_consumption": 15000,
    "building_size": 5000,
    "occupancy_rate": 0.75,
    "temperature": 22
  }'
```

**Get AI Recommendations**
```bash
curl -X GET "http://localhost:8000/api/v1/recommendations/hotel_123"
```

**Chat with AI Assistant**
```bash
curl -X POST "http://localhost:8000/api/v1/chat/sustainability" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How can I reduce my hotel carbon footprint?"
  }'
```

---

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Main Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/predict/emissions` | Predict carbon emissions |
| POST | `/api/v1/analyze/building` | Analyze building image |
| POST | `/api/v1/chat/sustainability` | Chat with AI assistant |
| GET | `/api/v1/recommendations/{id}` | Get personalized recommendations |
| GET | `/api/v1/insights/trends` | Get emission trends |
| POST | `/api/v1/reports/generate` | Generate sustainability report |

---

## 🧪 Models & Methodology

### 1. Data Collection
- **Energy consumption data**: Electricity, gas, water usage
- **Building characteristics**: Size, type, age, location
- **Weather data**: Temperature, humidity, seasonal patterns
- **Occupancy metrics**: Guest counts, room utilization

**Sources**: Kaggle, UCI ML Repository, public utility datasets

### 2. Data Preprocessing
- Handling missing values and outliers
- Feature engineering (time-based features, ratios, aggregations)
- Normalization and scaling
- Train/validation/test split (70/15/15)

### 3. Model Development

#### Machine Learning Models
- **Random Forest Regressor**: Baseline model
- **XGBoost**: Gradient boosting for better accuracy
- **LightGBM**: Fast and efficient alternative
- **Linear Regression**: Interpretable baseline

#### Deep Learning Models
- **LSTM**: Sequential pattern learning
- **CNN**: Image-based efficiency analysis
- **Transformer**: Attention-based forecasting

#### Evaluation Metrics
- **Regression**: RMSE, MAE, R² score
- **Classification**: Accuracy, F1-score, Confusion Matrix
- **Time Series**: MAPE, SMAPE

### 4. Generative AI Integration
- **RAG Pipeline**: LangChain + ChromaDB for context-aware responses
- **Prompt Engineering**: Optimized prompts for recommendations
- **Fine-tuning**: Custom model adaptation (if needed)

---

## 📊 Results

> **Note**: Results will be updated after model training and evaluation.

### Model Performance (Preliminary)

| Model | RMSE | MAE | R² Score |
|-------|------|-----|----------|
| Random Forest | TBD | TBD | TBD |
| XGBoost | TBD | TBD | TBD |
| LSTM | TBD | TBD | TBD |

### Key Insights
- TBD after EDA completion
- Feature importance analysis
- Seasonal patterns identified
- Anomaly detection results

---

## 🗺️ Roadmap

### Phase 1: Foundation ✅
- [x] Project structure setup
- [ ] Data collection and exploration
- [ ] Initial EDA notebooks
- [ ] Database schema design

### Phase 2: Model Development 🔄
- [ ] Baseline ML models
- [ ] Advanced ML models (XGBoost, LightGBM)
- [ ] Deep learning models (LSTM, CNN)
- [ ] Model evaluation and comparison

### Phase 3: GenAI Integration 📅
- [ ] RAG chatbot implementation
- [ ] LLM-powered recommendations
- [ ] Report generation system
- [ ] Voice interface (optional)

### Phase 4: API & Deployment 📅
- [ ] FastAPI implementation
- [ ] API testing and documentation
- [ ] Docker containerization
- [ ] Cloud deployment (optional)

### Phase 5: Visualization & Presentation 📅
- [ ] Tableau dashboard creation
- [ ] Streamlit web app (optional)
- [ ] Final presentation preparation
- [ ] Documentation completion

---

## 🤝 Contributing

This is an individual bootcamp project, but feedback and suggestions are welcome!

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Your Name**  
Data Science Bootcamp - Ironhack  
📧 Email: your.email@example.com  
🔗 LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)  
💼 Portfolio: [Your Website](https://yourwebsite.com)

---

## 🙏 Acknowledgments

- Ironhack Data Science Bootcamp instructors and mentors
- Open-source community for amazing tools and libraries
- Dataset providers (Kaggle, UCI ML Repository)

---

**⭐ If you find this project useful, please consider giving it a star!**

---

*Last Updated: November 2025*

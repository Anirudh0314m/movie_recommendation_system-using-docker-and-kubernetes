# Movie Recommendation System

## Overview
A containerized movie recommendation system that uses machine learning to suggest movies based on user preferences. This project demonstrates modern software engineering practices in AI systems, including containerization, orchestration, and CI/CD.

![Movie Recommendation](https://img.shields.io/badge/AI-Movie%20Recommendations-blue)
![Kubernetes](https://img.shields.io/badge/Deployment-Kubernetes-brightgreen)
![Docker](https://img.shields.io/badge/Container-Docker-blue)
![CI/CD](https://img.shields.io/badge/Pipeline-GitHub%20Actions-orange)

## Features
- Content-based movie recommendations using similarity matrices
- Interactive web interface using Streamlit
- Real-time movie data from TMDB API
- Containerized for consistent deployment
- Kubernetes orchestration for scalability
- CI/CD pipeline for automated testing and deployment

## Technology Stack
- **Frontend**: Streamlit
- **Backend**: Python, scikit-learn
- **API Integration**: TMDB Movie Database
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **CI/CD**: GitHub Actions

## Setup Instructions

### Prerequisites
- Python 3.9+
- Docker
- Kubernetes (Docker Desktop or Minikube)
- TMDB API key

### Local Development
```bash
# Clone the repository
git clone https://github.com/your-username/movie-recommendation-system.git
cd movie-recommendation-system

# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py
```

### Docker Deployment
```bash
# Build Docker image
docker build -t movie-recommender:latest .

# Run container
docker run -p 8501:8501 movie-recommender
```

### Kubernetes Deployment
```bash
# Create Kubernetes secret for API key
kubectl create secret generic movie-api-secrets --from-literal=tmdb-api-key=your-api-key-here

# Deploy to Kubernetes
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Forward port for local access
kubectl port-forward service/movie-recommender 8080:80
```

## CI/CD Pipeline

This project implements a full CI/CD pipeline using GitHub Actions:

1. **Continuous Integration**:
   - Automated testing on push
   - Code quality checks

2. **Continuous Deployment**:
   - Automatic Docker image building
   - Push to Docker Hub registry
   - Deployment to Kubernetes cluster

## Project Structure
```
movie_recommendation_system/
├── .github/
│   └── workflows/
│       └── ci-cd.yml         # CI/CD pipeline configuration
├── app.py                    # Main Streamlit application
├── k8s/                      # Kubernetes manifests
│   ├── deployment.yaml
│   └── service.yaml
├── deploy/                   # Deployment scripts
│   └── aws.py               
├── data/                     # Movie dataset files
├── Dockerfile                # Container definition
├── requirements.txt          # Python dependencies
└── README.md
```

## How It Works

The system uses a content-based recommendation algorithm:

1. **Data Processing**: Movies are processed to extract features like genre, cast, and keywords
2. **Vectorization**: Features are converted to vector representations
3. **Similarity Calculation**: Cosine similarity measures movie relationships
4. **Recommendation**: When a user selects a movie, the system finds similar movies

## Future Enhancements
- User authentication and personalized recommendations
- Collaborative filtering based on user ratings
- A/B testing for recommendation algorithms
- Real-time model retraining
- Enhanced visualization of recommendation explanations

## Contributors
- Anirudh.M - Initial work and main developer

## Acknowledgments
- TMDB API for providing movie data
- Streamlit for the interactive web framework

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'final-year-project-secret-key-2024'
    
    # Base directory
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Database
    DATABASE = os.path.join(BASE_DIR, 'database', 'attendance.db')
    
    # Upload folders
    DATASET_DIR = os.path.join(BASE_DIR, 'dataset')
    REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
    
    # Face Recognition
    MODEL_NAME = 'Facenet'
    DETECTOR_BACKEND = 'mtcnn'  # or 'opencv'
    SIMILARITY_THRESHOLD = 0.70  # Cosine similarity threshold for matching
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max-limit
    
    @staticmethod
    def init_app(app):
        # Create downloads directory if it doesn't exist
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
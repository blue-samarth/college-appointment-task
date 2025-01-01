import os
from secrets import token_urlsafe

class Config:
    """
    It is a class that contains secret key for secret key generation
    """
    def __init__(self):
        """
        It is a constructor that initializes the secret key
        """
        self.SECRET_KEY = os.getenv("SECRET_KEY", token_urlsafe(32))

    def generate_secret_key(self) -> str:
        """
        It is a method that generates secret key
        """
        return self.SECRET_KEY
    
    def add_in_env(self) -> None:
        """
        It is a method that adds secret key in environment
        """
        if not os.path.exists('core/.env'):
            with open('core/.env', 'w') as f:
                f.write(f'SECRET_KEY={self.SECRET_KEY}')


if __name__ == "__main__":
    config = Config()
    config.add_in_env()
    config.generate_secret_key()
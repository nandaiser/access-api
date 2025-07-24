
# app/jwt_keys.py
import os
from pathlib import Path
import string
import secrets

def generate_jwt_key(length=32):
    """Generate a secure JWT key."""
    alphabet = string.ascii_letters + string.digits
    
    while True:
        key = ''.join(secrets.choice(alphabet) for i in range(length))
        if (any(c.islower() for c in key) and 
            any(c.isupper() for c in key) and 
            sum(c.isdigit() for c in key) >= 4):
            return key

# Create the env file when module is imported
if __name__ == "__main__":
    # Ensure instance directory exists
    Path("instance").mkdir(exist_ok=True)
    
    key = generate_jwt_key(32)
    env_path = os.path.join("instance", ".env")
    
    with open(env_path, "w") as f:
        f.write(f"JWT_SECRET_KEY={key}\n")
    
    print(f"JWT key generated: {env_path}")
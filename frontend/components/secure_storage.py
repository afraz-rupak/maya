"""
Secure Storage for Face Authentication Data
Encrypted storage for embeddings and PIN
"""

import os
import json
import pickle
import hashlib
from pathlib import Path
from cryptography.fernet import Fernet


class SecureStorage:
    """Secure storage for face embeddings and PIN"""
    
    def __init__(self, storage_path=None):
        self.storage_path = storage_path or self._get_default_path()
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Set restrictive permissions on directory
        os.chmod(self.storage_path, 0o700)
        
        self.key = self._get_or_create_key()
        self.cipher = Fernet(self.key)
    
    def _get_default_path(self):
        """Get default secure storage path"""
        return Path.home() / ".maya" / "secure"
    
    def _get_or_create_key(self):
        """Get or create encryption key"""
        key_file = self.storage_path / ".key"
        
        if key_file.exists():
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            # Generate new key
            key = Fernet.generate_key()
            
            with open(key_file, 'wb') as f:
                f.write(key)
            
            # Set owner-only permissions
            os.chmod(key_file, 0o600)
            
            return key
    
    def save_embeddings(self, embeddings_dict):
        """
        Save face embeddings (encrypted)
        Args:
            embeddings_dict: {name: embedding_array}
        """
        embeddings_file = self.storage_path / "embeddings.enc"
        
        try:
            # Serialize embeddings
            data = pickle.dumps(embeddings_dict)
            
            # Encrypt
            encrypted_data = self.cipher.encrypt(data)
            
            # Write to file
            with open(embeddings_file, 'wb') as f:
                f.write(encrypted_data)
            
            # Set permissions
            os.chmod(embeddings_file, 0o600)
            
            print(f"✓ Saved {len(embeddings_dict)} face embeddings (encrypted)")
            return True
            
        except Exception as e:
            print(f"Error saving embeddings: {e}")
            return False
    
    def load_embeddings(self):
        """
        Load face embeddings (decrypt)
        Returns: {name: embedding_array} or {}
        """
        embeddings_file = self.storage_path / "embeddings.enc"
        
        if not embeddings_file.exists():
            return {}
        
        try:
            # Read encrypted data
            with open(embeddings_file, 'rb') as f:
                encrypted_data = f.read()
            
            # Decrypt
            data = self.cipher.decrypt(encrypted_data)
            
            # Deserialize
            embeddings_dict = pickle.loads(data)
            
            print(f"✓ Loaded {len(embeddings_dict)} face embeddings")
            return embeddings_dict
            
        except Exception as e:
            print(f"Error loading embeddings: {e}")
            return {}
    
    def save_pin(self, pin):
        """
        Save PIN (hashed with salt)
        Args:
            pin: 4-digit PIN string
        Returns: bool
        """
        pin_file = self.storage_path / "pin.json"
        
        try:
            # Generate salt
            salt = os.urandom(32)
            
            # Hash PIN
            pin_hash = hashlib.pbkdf2_hmac(
                'sha256',
                pin.encode('utf-8'),
                salt,
                100000  # iterations
            )
            
            # Store salt and hash
            data = {
                'salt': salt.hex(),
                'hash': pin_hash.hex()
            }
            
            with open(pin_file, 'w') as f:
                json.dump(data, f)
            
            # Set permissions
            os.chmod(pin_file, 0o600)
            
            print("✓ PIN saved securely")
            return True
            
        except Exception as e:
            print(f"Error saving PIN: {e}")
            return False
    
    def verify_pin(self, pin):
        """
        Verify PIN against stored hash
        Args:
            pin: 4-digit PIN string
        Returns: bool
        """
        pin_file = self.storage_path / "pin.json"
        
        if not pin_file.exists():
            # No PIN set, accept default "1234" for demo
            return pin == "1234"
        
        try:
            # Load stored hash
            with open(pin_file, 'r') as f:
                data = json.load(f)
            
            salt = bytes.fromhex(data['salt'])
            stored_hash = bytes.fromhex(data['hash'])
            
            # Hash provided PIN
            pin_hash = hashlib.pbkdf2_hmac(
                'sha256',
                pin.encode('utf-8'),
                salt,
                100000
            )
            
            # Compare
            return pin_hash == stored_hash
            
        except Exception as e:
            print(f"Error verifying PIN: {e}")
            return False
    
    def save_config(self, config_dict):
        """
        Save configuration settings
        Args:
            config_dict: Configuration dictionary
        """
        config_file = self.storage_path / "config.json"
        
        try:
            with open(config_file, 'w') as f:
                json.dump(config_dict, f, indent=2)
            
            os.chmod(config_file, 0o600)
            print("✓ Configuration saved")
            return True
            
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def load_config(self):
        """
        Load configuration settings
        Returns: dict or default config
        """
        config_file = self.storage_path / "config.json"
        
        default_config = {
            "enabled": True,
            "similarity_threshold": 0.6,
            "consecutive_matches_required": 3,
            "timeout_seconds": 30,
            "max_attempts": 5,
            "fallback_to_pin": True,
            "owner_name": "Afraz"
        }
        
        if not config_file.exists():
            return default_config
        
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            # Merge with defaults (for new keys)
            return {**default_config, **config}
            
        except Exception as e:
            print(f"Error loading config: {e}")
            return default_config
    
    def delete_all_data(self):
        """Delete all stored face and PIN data"""
        try:
            files = [
                self.storage_path / "embeddings.enc",
                self.storage_path / "pin.json",
                self.storage_path / "config.json"
            ]
            
            for file in files:
                if file.exists():
                    file.unlink()
            
            print("✓ Deleted all face authentication data")
            return True
            
        except Exception as e:
            print(f"Error deleting data: {e}")
            return False
    
    def check_first_time_setup(self):
        """
        Check if this is first-time setup
        Returns: bool (True if no embeddings exist)
        """
        embeddings_file = self.storage_path / "embeddings.enc"
        return not embeddings_file.exists()

import configparser
import os
from pathlib import Path

class ConfigReader:
    _config = None
    
    @classmethod
    def get_config(cls):
        """Get the configuration, loading it if necessary"""
        if cls._config is None:
            cls._config = cls.read_config()
        return cls._config
    
    @staticmethod
    def read_config():
        """Read and return the configuration from config.ini"""
        config = configparser.ConfigParser()
        
        # Get the absolute path to the config file
        base_dir = Path(__file__).parent.parent
        config_path = os.path.join(base_dir, 'config', 'config.ini')
        
        # Read the config file
        config.read(config_path)
        return config
    
    @classmethod
    def get_base_url(cls):
        """Get the base URL for the current environment"""
        config = cls.get_config()
        
        # Get the current environment
        current_env = config.get('Environments', 'base')
        
        # Get the URL for the current environment
        if current_env == 'base':
            return config.get('Environments', 'base_url')
        else:
            url_key = f"{current_env}_url"
            return config.get('Environments', url_key)
    
    @classmethod
    def get_browser_config(cls):
        """Get the browser configuration"""
        config = cls.get_config()
        return {
            'browser': config.get('Browsers', 'browser'),
            'headless': config.getboolean('Browsers', 'headless')
        }
    
    @classmethod
    def get_wait_times(cls):
        """Get the wait times configuration"""
        config = cls.get_config()
        return {
            'implicit_wait': config.getint('Test', 'implicit_wait'),
            'explicit_wait': config.getint('Test', 'explicit_wait')
        }
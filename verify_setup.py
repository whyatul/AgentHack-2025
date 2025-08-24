#!/usr/bin/env python3
"""
Comprehensive project verification script for AI Meme Stock Predictor
"""

import sys
import os
import subprocess
import importlib
from typing import List, Dict, Tuple
import requests

class Checkpoint:
    """Represents a verification checkpoint"""
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.status = "PENDING"
        self.details = ""

class ProjectVerifier:
    def __init__(self):
        self.checkpoints: List[Checkpoint] = []
        self.results: Dict[str, bool] = {}
        
    def add_checkpoint(self, name: str, description: str) -> Checkpoint:
        checkpoint = Checkpoint(name, description)
        self.checkpoints.append(checkpoint)
        return checkpoint
    
    def run_checkpoint(self, checkpoint: Checkpoint, test_func) -> bool:
        try:
            result = test_func()
            checkpoint.status = "✅ PASSED" if result else "❌ FAILED"
            self.results[checkpoint.name] = result
            return result
        except Exception as e:
            checkpoint.status = "❌ ERROR"
            checkpoint.details = str(e)
            self.results[checkpoint.name] = False
            return False
    
    def print_summary(self):
        print("\n" + "="*60)
        print("PROJECT SETUP VERIFICATION SUMMARY")
        print("="*60)
        
        for checkpoint in self.checkpoints:
            print(f"{checkpoint.status} {checkpoint.name}")
            if checkpoint.description:
                print(f"   Description: {checkpoint.description}")
            if checkpoint.details:
                print(f"   Details: {checkpoint.details}")
            print()
        
        passed = sum(1 for result in self.results.values() if result)
        total = len(self.results)
        print(f"Overall: {passed}/{total} checkpoints passed")
        
        if passed == total:
            print("🎉 All checkpoints passed! Project is ready to use.")
        else:
            print("❌ Some checkpoints failed. Check the details above.")

def main():
    verifier = ProjectVerifier()
    
    # Checkpoint 1: Python Environment
    checkpoint = verifier.add_checkpoint("Python Environment", "Check Python version and virtual environment")
    def check_python():
        python_version = sys.version_info
        if python_version.major != 3 or python_version.minor < 8:
            checkpoint.details = f"Python {python_version.major}.{python_version.minor} found, need 3.8+"
            return False
        
        # Check if we're in a virtual environment
        in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
        checkpoint.details = f"Python {python_version.major}.{python_version.minor}.{python_version.micro}, venv: {in_venv}"
        return True
    
    verifier.run_checkpoint(checkpoint, check_python)
    
    # Checkpoint 2: Required Dependencies
    checkpoint = verifier.add_checkpoint("Core Dependencies", "Check essential Python packages")
    def check_dependencies():
        required_packages = [
            ('fastapi', 'fastapi'),
            ('uvicorn', 'uvicorn'),
            ('pydantic', 'pydantic'),
            ('praw', 'praw'),
            ('tweepy', 'tweepy'),
            ('vaderSentiment', 'vaderSentiment'),
            ('python-telegram-bot', 'telegram'),
            ('requests', 'requests')
        ]
        missing = []
        for package_name, import_name in required_packages:
            try:
                importlib.import_module(import_name)
            except ImportError:
                missing.append(package_name)
        
        if missing:
            checkpoint.details = f"Missing packages: {', '.join(missing)}"
            return False
        
        checkpoint.details = "All core dependencies found"
        return True
    
    verifier.run_checkpoint(checkpoint, check_dependencies)
    
    # Checkpoint 3: Project Structure
    checkpoint = verifier.add_checkpoint("Project Structure", "Verify all required files and directories exist")
    def check_structure():
        required_paths = [
            'cli.py',
            'requirements.txt',
            'src/ai_meme_stock_predictor/agent/portia_agent.py',
            'src/ai_meme_stock_predictor/web/app.py',
            'src/ai_meme_stock_predictor/web/telegram_bot.py',
            'src/ai_meme_stock_predictor/utils/config.py'
        ]
        
        missing = []
        for path in required_paths:
            if not os.path.exists(path):
                missing.append(path)
        
        if missing:
            checkpoint.details = f"Missing files: {', '.join(missing)}"
            return False
        
        checkpoint.details = "All required files found"
        return True
    
    verifier.run_checkpoint(checkpoint, check_structure)
    
    # Checkpoint 4: Import Test
    checkpoint = verifier.add_checkpoint("Module Imports", "Test importing core modules")
    def check_imports():
        try:
            from src.ai_meme_stock_predictor.agent.portia_agent import PortiaMemeAgent
            from src.ai_meme_stock_predictor.web.app import app
            from src.ai_meme_stock_predictor.utils.config import get_settings
            checkpoint.details = "Core modules import successfully"
            return True
        except Exception as e:
            checkpoint.details = f"Import error: {str(e)}"
            return False
    
    verifier.run_checkpoint(checkpoint, check_imports)
    
    # Checkpoint 5: CLI Test
    checkpoint = verifier.add_checkpoint("CLI Interface", "Test command-line interface")
    def check_cli():
        try:
            result = subprocess.run([sys.executable, 'cli.py', '--help'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0 and 'usage' in result.stdout.lower():
                checkpoint.details = "CLI responds to --help"
                return True
            else:
                checkpoint.details = f"CLI error: {result.stderr or result.stdout}"
                return False
        except Exception as e:
            checkpoint.details = f"CLI test failed: {str(e)}"
            return False
    
    verifier.run_checkpoint(checkpoint, check_cli)
    
    # Checkpoint 6: FastAPI Server (quick test)
    checkpoint = verifier.add_checkpoint("FastAPI Server", "Test FastAPI server startup")
    def check_fastapi():
        try:
            # Start server in background
            process = subprocess.Popen([
                sys.executable, '-m', 'uvicorn', 
                'src.ai_meme_stock_predictor.web.app:app',
                '--port', '8001'  # Use different port to avoid conflicts
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait a moment for startup
            import time
            time.sleep(3)
            
            # Test health endpoint
            try:
                response = requests.get('http://127.0.0.1:8001/health', timeout=5)
                if response.status_code == 200:
                    checkpoint.details = "FastAPI server started and health endpoint responsive"
                    result = True
                else:
                    checkpoint.details = f"Health endpoint returned status {response.status_code}"
                    result = False
            except requests.exceptions.RequestException as e:
                checkpoint.details = f"Failed to connect to server: {str(e)}"
                result = False
            finally:
                # Clean up process
                process.terminate()
                process.wait(timeout=5)
            
            return result
            
        except Exception as e:
            checkpoint.details = f"Server test failed: {str(e)}"
            return False
    
    verifier.run_checkpoint(checkpoint, check_fastapi)
    
    # Checkpoint 7: Configuration
    checkpoint = verifier.add_checkpoint("Configuration", "Check configuration setup")
    def check_config():
        try:
            from src.ai_meme_stock_predictor.utils.config import get_settings
            settings = get_settings()
            
            # Check if basic config structure is there
            config_fields = ['alphavantage_api_key', 'reddit_client_id', 'telegram_bot_token']
            has_fields = all(hasattr(settings, field) for field in config_fields)
            
            if not has_fields:
                checkpoint.details = "Missing configuration fields"
                return False
            
            # Count configured APIs
            configured_apis = []
            if settings.alphavantage_api_key:
                configured_apis.append("AlphaVantage")
            if settings.reddit_client_id and settings.reddit_client_secret:
                configured_apis.append("Reddit")
            if settings.twitter_bearer_token:
                configured_apis.append("Twitter")
            if settings.telegram_bot_token:
                configured_apis.append("Telegram")
            
            if configured_apis:
                checkpoint.details = f"Configuration ready. Configured APIs: {', '.join(configured_apis)}"
            else:
                checkpoint.details = "Configuration structure ready but no API keys set"
            
            return True
            
        except Exception as e:
            checkpoint.details = f"Configuration test failed: {str(e)}"
            return False
    
    verifier.run_checkpoint(checkpoint, check_config)
    
    # Checkpoint 8: Agent Initialization
    checkpoint = verifier.add_checkpoint("Agent Initialization", "Test creating PortiaMemeAgent instance")
    def check_agent():
        try:
            from src.ai_meme_stock_predictor.agent.portia_agent import PortiaMemeAgent
            agent = PortiaMemeAgent()
            checkpoint.details = "PortiaMemeAgent created successfully"
            return True
        except Exception as e:
            checkpoint.details = f"Agent creation failed: {str(e)}"
            return False
    
    verifier.run_checkpoint(checkpoint, check_agent)
    
    # Print final summary
    verifier.print_summary()
    
    # Exit with appropriate code
    if all(verifier.results.values()):
        print("\n✅ Project verification completed successfully!")
        print("You can now:")
        print("1. Run CLI: python cli.py TSLA")
        print("2. Start FastAPI server: uvicorn src.ai_meme_stock_predictor.web.app:app --reload")
        print("3. Configure API keys in .env file for full functionality")
        sys.exit(0)
    else:
        print("\n❌ Some verifications failed. Please address the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()

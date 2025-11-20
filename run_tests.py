import subprocess
import sys

def run_tests():
    """Запуск всех тестов"""
    print("Запуск всех тестов...")
    result = subprocess.run([sys.executable, "-m", "pytest", "-v"])
    return result.returncode

if __name__ == "__main__":
    sys.exit(run_tests())
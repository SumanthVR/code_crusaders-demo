import subprocess

# List of required packages
packages = [
    "flask==2.3.3",
    "python-dotenv==1.0.0",
    "google-generativeai==0.3.1",
    "numpy==1.24.3",
    "pandas==2.0.3",
    "matplotlib==3.7.2",
    "gunicorn==21.2.0",
    "yfinance==0.2.28",
    "nsepython==0.0.973"
]

# Function to install each package
def install_package(package):
    try:
        print(f"\n🔹 Installing {package}...")
        subprocess.check_call(["pip", "install", package])
        print(f"✅ Successfully installed {package}\n")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package}\n")

# Install all packages
for package in packages:
    install_package(package)

print("🚀 All dependencies installed!")

# init.ps1
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# 1️⃣ Create virtual environment if it doesn't exist
if (-Not (Test-Path -Path "venv")) {
    Write-Host "🔹 Creating virtual environment..."
    python -m venv venv
    Write-Host "✅ Virtual environment created!"
}

# 2️⃣ Activate virtual environment
Write-Host "🔹 Activating virtual environment..."
# For PowerShell, activation script is different
& .\venv\Scripts\Activate.ps1
Write-Host "✅ Virtual environment activated!"

# 3️⃣ Install required packages
Write-Host "🔹 Installing packages..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Write-Host "✅ Packages installed!"

Write-Host "🚀 Setup complete! You can activate the virtual environment using '.\venv\Scripts\Activate.ps1' "


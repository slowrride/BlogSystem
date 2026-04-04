# Django Database Setup Script
# Usage: Right-click and "Run with PowerShell"

Set-Location -Path $PSScriptRoot

Write-Host "Current directory: $(Get-Location)" -ForegroundColor Yellow
Write-Host ""

Write-Host "[Step 1/3] Deleting old database..." -ForegroundColor Cyan
Remove-Item -Path "db.sqlite3" -Force -ErrorAction SilentlyContinue
Write-Host "[OK] Done" -ForegroundColor Green

Write-Host ""
Write-Host "[Step 2/3] Generating migrations..." -ForegroundColor Cyan
python manage.py makemigrations
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to generate migrations" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[Step 3/3] Applying migrations..." -ForegroundColor Cyan
python manage.py migrate
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to apply migrations" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[SUCCESS] Database setup completed!" -ForegroundColor Green
Write-Host "Now run: python manage.py createsuperuser" -ForegroundColor Green
Read-Host "Press Enter to exit"

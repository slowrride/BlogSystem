# Django Migration Script

Write-Host "Starting Django migration..." -ForegroundColor Cyan

Set-Location "d:\codes_py\BlogSystem"

Write-Host "Current directory: $(Get-Location)" -ForegroundColor Yellow

Write-Host "Running migrations..." -ForegroundColor Cyan
python manage.py migrate --no-input

if ($LASTEXITCODE -eq 0) {
    Write-Host "Migration successful!" -ForegroundColor Green
    Write-Host "You can now create superuser: python manage.py createsuperuser" -ForegroundColor Green
} else {
    Write-Host "Migration failed!" -ForegroundColor Red
    exit 1
}

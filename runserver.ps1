# Script para iniciar Django y abrir Swagger automáticamente

# Activar venv
& ".\venv\Scripts\Activate.ps1"

# Iniciar Django en background
Write-Host "Iniciando servidor Django..." -ForegroundColor Green
$process = Start-Process python -ArgumentList "manage.py runserver" -PassThru

# Esperar 3 segundos a que inicie
Start-Sleep -Seconds 3

# Abrir Swagger en el navegador
Write-Host "Abriendo Swagger..." -ForegroundColor Green
Start-Process "http://localhost:8000/swagger/"

# Mostrar mensaje
Write-Host "✓ Servidor Django iniciado en http://localhost:8000" -ForegroundColor Green
Write-Host "✓ Swagger abierto en http://localhost:8000/swagger/" -ForegroundColor Green
Write-Host "✓ Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow

# Esperar a que el usuario detiene el proceso
$process | Wait-Process

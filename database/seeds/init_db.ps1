# init_db.ps1
# Forzar a PowerShell a comunicarse internamente usando codificación UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
Write-Host "Creando base de datos si no existe..." -ForegroundColor Cyan
docker exec -i postgres psql -U admin -c "CREATE DATABASE prosperapp_db;" 2>$null
Write-Host "Estructurando tablas..." -ForegroundColor Cyan
Get-Content -Encoding UTF8 -Raw database/scripts/create_tables.sql | docker exec -i postgres psql -U admin -d prosperapp_db
Write-Host "Insertando registros de prueba..." -ForegroundColor Cyan
Get-Content -Encoding UTF8 -Raw database/seeds/seed_data.sql | docker exec -i postgres psql -U admin -d prosperapp_db
Write-Host "¡Base de datos lista para ProsperApp!" -ForegroundColor Green
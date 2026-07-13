# ProsperApp
Proyecto Final - Bases de Datos - Universidad del Valle

# 🚀 ProsperApp
Software para gestión de proyectos de software personales.

**Curso:** Bases de Datos — Universidad del Valle  
**Profesor:** Jefferson A. Peña Torres  
**Integrantes:** 
LAURA DAYANA TASCON VELASCO - 2438545
GERALDIN GUERRERO - 2436674
ENRIQUE LOZANO ABELLA - 2436032


---

## 🛠️ Tecnologías
- Python + Flask
- PostgreSQL (Docker)
- HTML + CSS

---

## ⚙️ Cómo correr el proyecto

# 1. Clonar
git clone https://github.com/LauraDayanaT/ProsperApp.git

# 2. Instalar dependencias
pip install flask psycopg2-binary

# 3. Levantar Docker y la base de datos
docker run --name postgres -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin -p 5432:5432 -d postgres

docker run --name pgadmin -p 5050:80 -e PGADMIN_DEFAULT_EMAIL=admin@admin.com -e PGADMIN_DEFAULT_PASSWORD=pg123 -d dpage/pgadmin4

 powershell -ExecutionPolicy Bypass -File .\init_db.ps1


# 4. Correr la app
cd app
python app.py

# 5. Ingresa a
 Running on all addresses (0.0.0.0)
 Running on http://127.0.0.1:5001
 Running on http://192.168.1.36:5001


## 🔑 Usuarios de prueba
| Usuario | Email | Contraseña |
|---|---|---|
| Laura Dayana | laura@email.com | 1234 |
| Ceir Enrique | enrique@email.com | 1234 |
| Geraldin Guerrero| geraldin@email.com | 1234 |

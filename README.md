# ProsperApp
Proyecto Final - Bases de Datos - Universidad del Valle

# 🚀 ProsperApp
Software para gestión de proyectos de software personales.

**Curso:** Bases de Datos — Universidad del Valle  
**Profesor:** Jefferson A. Peña Torres  
**Integrantes:** 
LAURA DAYANA TASCON VELASCO - 2438545
DANIEL ESCOBAR ESCOBAR - 2437924
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

# 3. Levantar Docker
docker run --name postgres -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin -p 5432:5432 -d postgres
docker run --name pgadmin -p 5050:80 -e PGADMIN_DEFAULT_EMAIL=admin@admin.com -e PGADMIN_DEFAULT_PASSWORD=pg123 -d dpage/pgadmin4

# 4. Correr la app
cd app
python app.py


## 🔑 Usuarios de prueba
| Usuario | Email | Contraseña |
|---|---|---|
| Laura Dayana | laura@email.com | 1234 |
| Ceir Enrique | enrique@email.com | 1234 |
| Daniel | daniel@email.com | 1234 |
| Geraldin | geraldin@email.com | 1234 |

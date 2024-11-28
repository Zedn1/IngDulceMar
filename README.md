# IngDulceMar

## Requisitos Previos
- Python 3.x
- Git

## Guía de Instalación

### 1. Instalación de AppServ
1. Descarga AppServ desde [http://www.appserv.org/](https://www.appserv.org/en/download/)
2. Ejecuta el instalador
3. Durante la instalación:
   - Selecciona los componentes: Apache, MySQL, PHP
   - Define una contraseña para el usuario root de MySQL
   - Completa la instalación

### 2. Configuración de la Base de Datos
1. Accede a phpMyAdmin: 
   - Abre tu navegador
   - Ingresa a `http://localhost/phpmyadmin`
   - Usuario: root
   - Contraseña: [la que configuraste en la instalación]

2. Crear base de datos:
   - Clic en "Nueva" en el panel izquierdo
   - Nombre de la base de datos: [nombre_db]
   - Clic en "Crear"

3. Crear nuevo usuario:
   - Ve a "Bases de Datos"
   - Haz click en "Seleccionar Privilegios" a la derecha de tu base de datos
   - Pulsa en "Agregar cuenta de usuario"
   - Completa:
     - Nombre de usuario: [tu_usuario]
     - Contraseña: [tu_contraseña]
   - Selecciona "Otorgar todos los privilegios"
   - En "Privilegios Globales" haz click en "Seleccionar Todo"
   - Clic en "Continuar"


### 3. Configuración del Entorno Virtual
```bash
# Clonar el repositorio
git clone [URL_DEL_REPOSITORIO]
cd [NOMBRE_DEL_PROYECTO]

# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# En Windows:
.venv\Scripts\activate
# En Linux/Mac:
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 4. Configuración del Archivo .env
Crea un archivo `.env` en la raíz del proyecto con la siguiente información:
```plaintext
DB_NAME=[nombre_db]
DB_USER=[tu_usuario]
DB_PASSWORD=[tu_contraseña]
```

### 5. Configuración de Django
Abre VS Code, accede a Command Prompt y ejecuta:
```bash
# Activar entorno virtual si no está activado
.venv\Scripts\activate

# Realizar migraciones
python manage.py migrate

# Iniciar servidor de desarrollo
python manage.py runserver
```

---

Y listo!!! Todo deberia funcionar perfectamente!!!

## Notas Adicionales
- Asegúrate de que AppServ esté ejecutándose antes de iniciar el proyecto
- Verifica que los servicios de Apache y MySQL estén activos
- Para detener el servidor de desarrollo, presiona Ctrl+C en la terminal

## Solución de Problemas Comunes
1. Error de conexión a la base de datos:
   - Verifica que las credenciales en .env sean correctas
   - Confirma que el servidor MySQL esté activo

2. Error al activar el entorno virtual:
   - Asegúrate de estar en el directorio correcto
   - Verifica que Python esté instalado correctamente
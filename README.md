# 🌱 Semiverd - Las Cuatro Semillas Verdes de Barrancabermeja

Semiverd es una aplicación web gamificada diseñada para educar y concientizar sobre el cuidado del medio ambiente en Barrancabermeja. Los usuarios asumen el rol de **Guardianes Ecológicos**, completando misiones reales, ganando puntos, desbloqueando medallas y haciendo crecer un árbol virtual mediante algoritmos fractales interactivos.

---

## 🛠️ Stack Tecnológico

### Backend (FastAPI + PostgreSQL)
- **FastAPI**: Framework moderno, rápido y de alto rendimiento para construir APIs con Python.
- **SQLAlchemy & Alembic**: ORM para mapeo de base de datos y control de migraciones.
- **Uvicorn**: Servidor ASGI para correr la aplicación FastAPI en desarrollo.
- **PostgreSQL**: Base de datos relacional para el almacenamiento persistente de usuarios, misiones completadas y tips.
- **Reconocimiento Facial**: Login alternativo mediante capturas de cámara web y comparación de vectores faciales.

### Frontend (HTML5 + CSS3 + Vanilla JavaScript MVC)
- **HTML5 & CSS3**: Diseño responsivo (*mobile-first*), transiciones animadas y un sistema de variables de color.
- **Canvas API**: Renderizado dinámico e interactivo del árbol virtual (fractales dibujados recursivamente).
- **ES6 Modules (ESM)**: Uso nativo de módulos en el navegador (`import`/`export`) sin necesidad de empaquetadores complejos.
- **MediaDevices API**: Acceso seguro a la cámara web para la autenticación facial.

---

## 📐 Arquitectura del Frontend (MVC)

El frontend de la aplicación ha sido refactorizado desde una estructura monolítica a un patrón **Modelo-Vista-Controlador (MVC)** modular. Esto separa claramente la lógica de negocio de la presentación, facilitando la escalabilidad del proyecto:

```
frontend/
  ├── index.html               # Estructura principal y plantillas de vistas
  ├── styles.css               # Diseño, variables CSS y estilos generales
  └── js/
      ├── app.js               # Bootstrap de la aplicación: inicializa e integra MVC
      ├── config.js            # Configuraciones globales (API URL, niveles, datos demo)
      ├── models/
      │   └── state.js         # MODEL: Estado global, persistencia local y cliente API
      ├── views/
      │   ├── mainView.js      # VIEW: Navegación, barra superior, tema y notificaciones
      │   ├── loginView.js     # VIEW: Formularios de autenticación y captura de cámara
      │   ├── homeView.js      # VIEW: Panel principal y árbol miniatura
      │   ├── treeView.js      # VIEW: Canvas del árbol fractal animado, estadísticas y medallas
      │   ├── mapView.js       # VIEW: Camino ecológico y paradas de nivel
      │   ├── missionView.js   # VIEW: Lista de misiones y modal de detalles
      │   ├── academiaView.js  # VIEW: Tarjetas de consejos y filtros de categoría
      │   ├── rankingView.js   # VIEW: Tabla de posiciones de guardianes
      │   └── perfilView.js    # VIEW: Ficha de estadísticas del perfil
      └── controllers/
          └── appController.js # CONTROLLER: Manejador de eventos y puente de comunicación
```

### Funcionamiento de Capas:
1. **Model (`state.js`)**: Almacena las variables temporales (token, misiones activas) y realiza las solicitudes HTTP Fetch al backend de FastAPI. Cuenta con soporte para un "Modo Demo" local si el servidor backend no se encuentra en línea.
2. **View (`views/`)**: Cada vista gestiona exclusivamente los elementos del DOM asociados a su pestaña. Por ejemplo, `treeView.js` redibuja el árbol fractal en el Canvas, y `loginView.js` manipula el stream de la cámara web.
3. **Controller (`appController.js`)**: Escucha los clicks y envíos de formularios. Cuando el usuario interactúa, llama a los métodos del modelo (`StateModel`) para actualizar los datos y le ordena a las vistas correspondientes redibujarse.

---

## 🎨 Mejoras de Accesibilidad y Contraste (WCAG AA)

Se realizaron pruebas exhaustivas de legibilidad en los modos **Claro** y **Oscuro**, solucionando los siguientes problemas de diseño:
- **Modo Claro (Botón Demo)**: El botón *Ver Demo* tenía texto blanco sobre fondo verde claro, haciéndose invisible. Se corrigió mediante un override de CSS con bordes y tipografía en verde oscuro contrastante (`#2d5a3e`).
- **Textos Secundarios (`--color-text-dim`)**: Se reemplazó el color de texto de baja opacidad por tonos sólidos y legibles que superan la relación de contraste estándar de **4.5:1** en ambos temas (utilizado en descripciones de misiones y correos de perfil).
- **Placeholders de Formularios**: Se aumentó la opacidad de los marcadores de posición para asegurar que las etiquetas de ayuda sean legibles antes de escribir.
- **Legibilidad de Modales**: Se incrementó la opacidad del texto descriptivo a `0.75` en modo oscuro para evitar la fatiga visual.

---

## 🚀 Instalación y Uso

### Requisitos Previos
- **Python 3.9+**
- **PostgreSQL** instalado y corriendo localmente.
- Un servidor web local para el frontend (como la extensión Live Server de VS Code o `npx http-server`).

### 1. Configuración del Backend

1. Entra al directorio `backend`:
   ```bash
   cd backend
   ```
2. Crea un entorno virtual y actívalo:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows usa: venv\Scripts\activate
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Configura el archivo de variables de entorno `.env` (basándote en `.env.example`):
   ```bash
   DATABASE_URL=postgresql://postgres:TU_CONTRASEÑA@localhost:5432/semiverd_db
   SECRET_KEY=cambiar_en_produccion
   ```
5. Inicia el servidor de desarrollo:
   ```bash
   python app/main.py
   ```
   *La API estará disponible en `http://localhost:8000` y su documentación interactiva Swagger en `http://localhost:8000/docs`.*

### 2. Configuración del Frontend

1. Puesto que el frontend utiliza módulos ES6 nativos, **no debe abrirse el archivo `index.html` directamente como archivo local (`file:///...`)** ya que el navegador bloqueará las importaciones por políticas de seguridad (CORS).
2. Levanta un servidor estático local en la carpeta `frontend/`:
   ```bash
   cd frontend
   npx http-server -p 5500
   ```
3. Abre tu navegador e ingresa a `http://localhost:5500`.
4. Si no tienes el backend configurado o activo, haz click en **"Ver Demo (sin cuenta)"** para explorar la experiencia completa del cliente usando datos mock localizados.

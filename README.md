# 🌱 Semiverd - Las Cuatro Semillas Verdes de Barrancabermeja

Semiverd es una aplicación web gamificada diseñada para educar y concientizar sobre el cuidado del medio ambiente en Barrancabermeja. Los usuarios asumen el rol de **Guardianes Ecológicos**, completando misiones reales, ganando puntos, desbloqueando medallas y haciendo crecer un árbol virtual mediante algoritmos fractales interactivos.

---

## 🛠️ Stack Tecnológico y Arquitectura Unificada (MVC)

El proyecto está organizado en un patrón de diseño **Modelo-Vista-Controlador (MVC)** a nivel de raíz, eliminando la separación física de carpetas de backend y frontend:

```
semiverd/
  ├── main.py                  # Punto de entrada principal (FastAPI). Sirve la API y el portal web.
  ├── seed.py                  # Script para poblar la base de datos localmente.
  ├── requirements.txt         # Dependencias de Python.
  ├── .env                     # Variables de configuración local y de base de datos.
  │
  ├── models/                  # MODELO (Capa de datos y esquemas)
  │   ├── database.py          # Conexión a la base de datos PostgreSQL con SQLAlchemy.
  │   ├── models.py            # Modelos ORM (Usuario, Mision, Progreso, Tip, Recompensa).
  │   └── schemas.py           # Esquemas Pydantic para validación y serialización.
  │
  ├── controllers/             # CONTROLADOR (Capa lógica y endpoints API)
  │   ├── auth_controller.py   # Control de registro, acceso e inicio facial.
  │   ├── missions_controller.py # Control de inicio, progreso y finalización de misiones.
  │   ├── tips_controller.py   # Consultas y filtros de consejos ecológicos.
  │   └── users_controller.py  # Control del perfil de guardián y ranking.
  │
  └── views/                   # VISTA (Capa de presentación / Frontend)
      └── web/                 # Portal web estático montado directamente en el servidor.
          ├── index.html       # Estructura HTML5 de la aplicación.
          ├── styles.css       # Estilos CSS3, animaciones y tokens de tema.
          └── js/              # Lógica modular del frontend (Estructura MVC de cliente).
              ├── app.js       # Bootstrap: inicializa e integra el MVC del cliente.
              ├── config.js    # Constantes y simulación de datos demo en local.
              ├── models/      # Estado local del cliente.
              ├── views/       # Gestión de renderizados del DOM de cada pestaña.
              └── controllers/ # Manejadores de eventos de la interfaz de usuario.
```

---

## 🎨 Mejoras de Accesibilidad y Contraste (WCAG AA)

Se realizaron pruebas de legibilidad en los modos **Claro** y **Oscuro**, solucionando los siguientes problemas de diseño:
- **Modo Claro (Botón Demo)**: El botón *Ver Demo* tenía texto blanco sobre fondo verde claro, haciéndose invisible. Se corrigió mediante un override de CSS con bordes y tipografía en verde oscuro contrastante (`#2d5a3e`).
- **Textos Secundarios (`--color-text-dim`)**: Se reemplazó el color de texto de baja opacidad por tonos sólidos y legibles que superan la relación de contraste estándar de **4.5:1** en ambos temas (utilizado en descripciones de misiones y correos de perfil).
- **Placeholders de Formularios**: Se aumentó la opacidad de los marcadores de posición para asegurar que las etiquetas de ayuda sean legibles antes de escribir.
- **Legibilidad de Modales**: Se incrementó la opacidad del texto descriptivo a `0.75` en modo oscuro para evitar la fatiga visual.
- **Menú de Navegación**: Se mejoró el contraste de los iconos y etiquetas inactivas en la barra de navegación inferior móvil para facilitar su uso a la luz del día.

---

## 🚀 Instalación y Uso

### Requisitos Previos
- **Python 3.9+**
- **PostgreSQL** instalado y corriendo localmente.

### 1. Preparación del Entorno

1. Abre tu terminal en la carpeta del proyecto:
   ```bash
   cd semiverd
   ```
2. Crea un entorno virtual de Python y actívalo:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows usa: venv\Scripts\activate
   ```
3. Instala las dependencias requeridas:
   ```bash
   pip install -r requirements.txt
   ```
4. Configura el archivo de configuración `.env` (creando una copia a partir de `.env.example` si no existe):
   ```bash
   DATABASE_URL=postgresql://postgres:TU_CONTRASEÑA@localhost:5432/semiverd_db
   SECRET_KEY=cambiar_en_produccion
   ```

### 2. Sembrar la Base de Datos

Ejecuta el cargador de datos semilla una sola vez para estructurar las misiones y tips iniciales en tu PostgreSQL:
```bash
python seed.py
```

### 3. Iniciar el Servidor Unificado

Inicia la aplicación completa con el siguiente comando:
```bash
python main.py
```

*La aplicación web completa y la API estarán corriendo en la misma dirección:*
- **Aplicación Web**: [http://localhost:8000](http://localhost:8000)
- **Documentación Interactiva (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)

*Si deseas ver o probar la interfaz del juego sin configurar PostgreSQL ni levantar la base de datos, entra a [http://localhost:8000](http://localhost:8000) y presiona el botón **"Ver Demo (sin cuenta)"** para jugar con datos simulados locales.*

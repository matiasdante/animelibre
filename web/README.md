# Anime Libre - Interfaz Web

Interfaz web moderna para Anime Libre, migrada desde tkinter a Flask con diseño responsivo y funcionalidades mejoradas.

## 🚀 Características

- **Interfaz web moderna y responsiva** - Compatible con desktop, tablet y móvil
- **Búsqueda en tiempo real** - Encuentra animes instantáneamente
- **Múltiples reproductores** - Soporte para VLC, MPV y reproductor predeterminado
- **Historial de animes** - Base de datos SQLite para persistencia
- **API REST** - Endpoints organizados para mejor mantenimiento
- **Diseño dark mode** - Interfaz moderna con gradientes y animaciones

## 📦 Instalación

### Requisitos
- Python 3.8+
- Flask 3.0+
- Dependencias del proyecto base (ver requirements.txt)

### Instalación rápida
```bash
# Clonar el repositorio
git clone https://github.com/Dou-Community-S-A/animelibre.git
cd animelibre

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación web
cd web
python app.py
```

La aplicación estará disponible en: http://localhost:5000

## 🖥️ Uso

### Navegación
- **Inicio**: Página principal con changelog y accesos rápidos
- **Buscar**: Búsqueda de animes con sugerencias populares
- **Historial**: Animes vistos recientemente
- **Configuración**: Selección de reproductor de video

### Búsqueda de Animes
1. Ir a la página "Buscar"
2. Escribir el nombre del anime
3. Seleccionar de los resultados
4. Elegir episodio y proveedor de video
5. El reproductor se abrirá automáticamente

### Configuración de Reproductor
1. Ir a "Configuración"
2. Seleccionar reproductor preferido:
   - **VLC Media Player** (recomendado)
   - **MPV Player** (ligero)
   - **Predeterminado** (del sistema)
3. Guardar configuración

## 🏗️ Arquitectura

```
web/
├── app.py                 # Servidor Flask principal
├── templates/             # Templates HTML
│   ├── base.html         # Template base
│   ├── index.html        # Página principal
│   ├── search.html       # Búsqueda
│   ├── anime_detail.html # Detalles del anime
│   ├── history.html      # Historial
│   └── settings.html     # Configuración
├── static/               # Archivos estáticos
│   ├── css/
│   │   └── style.css     # Estilos CSS
│   └── js/
│       └── app.js        # JavaScript
└── api/                  # Módulos de API
    ├── anime_api.py      # API de animes
    └── vlc_handler.py    # Manejo de reproductores
```

## 🔧 API Endpoints

### Búsqueda
- `GET /api/search?q={query}` - Buscar animes
- `GET /api/anime/{anime_id}` - Información del anime
- `GET /api/anime/{anime_id}/episodes` - Lista de episodios

### Reproducción
- `GET /api/episode/links?anime_id={id}&episode={num}` - Enlaces de episodio
- `POST /api/play` - Reproducir video

### Historial
- `POST /api/history` - Agregar al historial
- `POST /api/history/remove` - Eliminar del historial

### Configuración
- `POST /api/settings` - Guardar configuración
- `GET /api/player/check?player={name}` - Verificar reproductor

## 🎨 Características de Diseño

- **Responsive Design**: Compatible con todos los dispositivos
- **Dark Theme**: Diseño moderno con gradientes azules
- **Animaciones**: Transiciones suaves y efectos visuales
- **Bootstrap 5**: Framework CSS moderno
- **Font Awesome**: Iconos vectoriales
- **Cards**: Diseño por tarjetas para mejor organización

## 🔄 Migración desde tkinter

### Funcionalidades migradas:
- ✅ Búsqueda de animes (AnimeFLV API)
- ✅ Visualización de información del anime
- ✅ Listado de episodios
- ✅ Extracción de links de video
- ✅ Integración con reproductores (VLC/MPV)
- ✅ Historial de animes vistos
- ✅ Configuración de reproductor

### Mejoras añadidas:
- ✅ Interfaz web responsiva
- ✅ API REST organizada
- ✅ Base de datos SQLite
- ✅ Carga asíncrona
- ✅ Mejor manejo de errores
- ✅ Acceso remoto

## 🛠️ Desarrollo

### Estructura del código
- `app.py`: Servidor Flask principal con todas las rutas
- `api/anime_api.py`: Wrapper de la API original de AnimeFLV
- `api/vlc_handler.py`: Manejo de reproductores de video
- Templates: Páginas HTML con Jinja2
- Static: CSS y JavaScript para la interfaz

### Base de datos
SQLite con las siguientes tablas:
- `config`: Configuración de la aplicación
- `history`: Historial de animes vistos

### Compatibilidad
- Mantiene compatibilidad con `scripts/anime_scrapper.py`
- Reutiliza la lógica existente de AnimeFLV
- Preserva la funcionalidad del reproductor

## 🌐 Acceso Remoto

La aplicación puede ejecutarse en red para acceso desde otros dispositivos:

```bash
# Ejecutar en todas las interfaces
python app.py  # Por defecto escucha en 0.0.0.0:5000

# Acceder desde otros dispositivos
http://[IP_DEL_SERVIDOR]:5000
```

## 📱 Soporte Móvil

- Interfaz completamente responsiva
- Navegación optimizada para touch
- Cards redimensionables
- Texto legible en pantallas pequeñas

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama de feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit los cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto mantiene la misma licencia que el proyecto original.

## 👨‍💻 Desarrolladores

- **matutEv**: Desarrollo original y API
- **LostDou**: GUI original y Discord bot
- **Sharckmerferu**: QA testing
- **Migración Web**: Implementación de la interfaz Flask moderna
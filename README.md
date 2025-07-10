
<h1 align="center">
  <br>
  <a href="https://github.com/Dou-Community-S-A"><img src="https://i.imgur.com/eLhJL09.png" alt="Dou-Community" width="200"></a>
  <br>
  AnimeLibre
  <br>
</h1>

<h4 align="center">App para buscar animes de AnimeFLV desde la terminal o desde la GUI</h4>

<p align="center">
  <a href="#Funciones">Funciones</a> •
  <a href="#Como se usa">Como se usa</a> •
  <a href="#Descargar">Descargar</a> •
  <a href="#Creditos">Creditos</a> 
</p>


## Funciones

* Api Animeflv
  - Buscamos anime
  - Seleccionamos opcion
  - Seleccionamos capitulo
  - Entrega link de descarga
* Scrapping Stape
  - Agarra el link de stape
  - Scrappea la url para seleccionar el archivo .mp4
  - Abre la url en VLC
* Gui (WIP)

## Como se usa

Para clonar esta repositorio, vas a necesitar [Git](https://git-scm.com) y [Python](https://www.python.org/downloads/) (que viene con [pip](https://pypi.org/project/pip/)) instalados en tu PC

```bash
# Clone el repositorio.
$ git clone https://github.com/Dou-Community-S-A/animelibre.git

# Ir al repo
$ cd animelibre

# Instalar dependencias
$ pip install -r requirements.txt

# Iniciar la app
$ python3 main.py
$ python3 app.py (GUI)
```

## Grafana Beyla Demo

Además de la funcionalidad principal para buscar animes, este repositorio incluye un script de demostración para [Grafana Beyla](https://grafana.com/oss/beyla/), una herramienta de observabilidad eBPF.

### ¿Qué es Grafana Beyla?
Beyla es una herramienta de observabilidad que usa eBPF para recopilar métricas automáticamente de aplicaciones sin necesidad de modificar el código.

### Como usar el demo

```bash
# Ejecutar el script de configuración
$ ./grafana_beyla_demo.sh

# Iniciar los servicios
$ sudo docker-compose up -d

# Verificar que todos los contenedores estén funcionando
$ docker-compose ps
```

### Servicios incluidos en el demo:
- **Sample App** (puerto 8080): Aplicación de ejemplo basada en Nginx
- **Prometheus** (puerto 9090): Recolección de métricas
- **Grafana** (puerto 3000): Visualización de métricas (usuario: admin, contraseña: admin)
- **Beyla**: Observabilidad eBPF con compatibilidad AppArmor

### Compatibilidad con AppArmor
El demo incluye configuraciones especiales para sistemas con AppArmor habilitado (como Ubuntu/Debian):
- `security_opt: apparmor:unconfined` para el contenedor Beyla
- Capacidades necesarias: `SYS_ADMIN`, `SYS_PTRACE`, `SYS_RESOURCE`
- Montajes de volúmenes requeridos para funcionalidad eBPF

### Solución de problemas
- Asegúrate de ejecutar `docker-compose up -d` con `sudo`
- Para ver logs de Beyla: `docker-compose logs beyla`
- El contenedor Beyla requiere acceso privilegiado para funcionalidad eBPF

## Proximas Actualizaciones
  - Update Total a Node.js/TS
## Descargar

Podes descargar [aca](https://github.com/Dou-Community-S-A/animelibre/releases) el ultimo release del archivo.


## Creditos

* [matutEv](https://github.com/matiasdante)
  -  Development and api usage
  -  WebScrapping
    
* [LostDou](https://github.com/lostdou)
  -  Gui development.
  -  Discord bot implementation
    
* [Sharckmerferu](https://github.com/Shackmerferu)
  -  QA testing
  -  Contributor

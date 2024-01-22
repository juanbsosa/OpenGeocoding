# OpenGeocoding

**Authors:** *Lucas Abbate & Juan Bautista Sosa*

**Acknowledgements:** mostly based on the work done in this repository: [nominatim-docker](https://github.com/mediagis/nominatim-docker). Our main contribution are the scripts in Python and R to query the geocoding server, and the instructions in Spanish.


## Table of Contents

1. [OpenGeocoding (Spanish version)](#opengeocoding-spanish-version)
   - [a) Instalación de Linux](#a-instalación-de-linux)
   - [b) Instalar Docker Desktop](#b-instalar-docker-desktop)
   - [c) Instalar el servidor de Nominatim y correrlo en un contenedor de Docker](#c-instalar-el-servidor-de-nominatim-y-correrlo-en-un-contenedor-de-docker)
   
2. [OpenGeocoding (English version)](#opengeocoding-english-version)
   - [a) Linux Installation](#a-linux-installation)
   - [b) Install Docker Desktop](#b-install-docker-desktop)
   - [c) Install the Nominatim server and run it in a Docker container](#c-install-the-nominatim-server-and-run-it-in-a-docker-container)


## OpenGeocoding (Spanish version)

### Instructivo para instalar y utilizar servidores de geolocalización de código abierto en Windows

El objetivo de este repositorio es explicar todos los pasos necesarios para instalar un servicio de georreferenciación de código abierto en un servidor local y hacerle consultas.


#### a) Instalación de Linux

Utilizaremos Docker para alojar el servidor.

En primer lugar, tenemos que poder correr el sistema operativo Linux en nuestra computadora, ya que lo usaremos como motor backend para procesar y administrar el contenedor de Docker en el cual se alojará nuestro servidor de consulta para georreferenciar direcciones.

En Windows, esto puede conseguirse instalando WSL ("Windows Subsystem for Linux"). Éste es un aplicativo de Windows que nos permite usar herramientas de Linux en una computadora con Windows, con una arquitectura liviana y eficiente.

Para instalar la última versión de WSL en windows, seguir los siguientes pasos:
1) Presionar las teclas Windows+R para abrir el cuadro de diálogo Ejecutar.
2) Escribir 'powershell' y presionar _CTRL+SHIFT+ENTER_ para abrir la consola de Windows PowerShell como administrador.
3) Escribir 'wsl --install' y presionar _ENTER_.


#### b) Instalar Docker Desktop

1) Instalar desde https://docs.docker.com/desktop/install/windows-install/. 
2) Seleccionar la opción para utilizar WSL 2.
3) Reiniciar la PC.

#### c) Instalar el servidor de Nominatim y correrlo en un contenedor de Docker

1) Abrir Docker
2) Abrir la consola (buscar la aplicación "Command Prompt" en el inicio)
3) Correr el comando:

```sh
docker run -it --rm -e PBF_URL=https://download.geofabrik.de/south-america/argentina-latest.osm.pbf -e REPLICATION_URL=https://download.geofabrik.de/south-america/argentina-updates/ -e IMPORT_STYLE=extratags -e IMPORT_WIKIPEDIA=true -p 8080:8080  -v /osm-maps/extras:/nominatim/extras --name nominatim mediagis/nominatim:4.3
```

Explicación:

- _docker run_: comando básico para crear y ejecutar un nuevo contenedor

- _-it_: especificar que el contenedor debe ejecutarse de forma interactiva en la consola

- _--rm_: especificar que el contenedor debe ser eliminado automáticamente al terminar

- _-e_: crear un objeto en el ambiente

  - _PBF_URL_: URL al archivo PBF de OpenStreetMap para Argentina
  
  - _REPLICATION_URL_: URL al archivo PBF de OpenStreetMap con actualizaciones para Argentina. Esto permite que el contenedor se actualice cuando es ejecutado.
  
  - _IMPORT_WIKIPEDIA_: habilita la importación de datos de Wikipedia
  
  - _NOMINATIM_PASSWORD_: contraseña para acceder al servidor de Nominatim
  
- _-v_: monta un volumen llamado "nomitaim-data" al directorio "/var/lib/postgresql/14/main" dentro del contenedor. Esto permite que el contenedor almacene datos, como la base de geocodificación y las actualizaciones, de forma persistente y por fuera del contenedor.


La descarga puede tardar varios minutos. Una vez que termina, el contenedor ya se debería haber creado en Docker y debería estar corriendo. Podemos verificar esto escribiendo un código en la consola que nos muestre todos los contenedores que actualmente están activos:

```sh
docker ps --filter "status=running"
```

¡Listo! Ya podemos empezar a hacer consultas a nuestro servidor, siempre que esté activo. En la carpeta [scripts](./scripts/) de este repositorio les compartimos código para hacerle consultas desde Python o R. ¡A georreferenciar!



## OpenGeocoding (English version)

### Guide to install and use open source geolocation servers in Windows

The purpose of this repository is to explain all the necessary steps to install an open source geocoding service on a local server and make queries to it.

#### a) Linux Installation

We will use Docker to host the server.

First, we need to be able to run Linux on our computer, as we will use it as a backend engine to process and manage the Docker container in which our geocoding query server will be hosted.

On Windows, this is achieved by installing WSL ("Windows Subsystem for Linux"). This is a Windows application that allows us to use Linux tools on a Windows computer, with a lightweight and efficient architecture.

To install the latest version of WSL on Windows, follow these steps:
1) Press the Windows+R keys to open the Run dialog box.
2) Type 'powershell' and press _CTRL+SHIFT+ENTER_ to open the Windows PowerShell console as an administrator.
3) Type 'wsl --install' and press _ENTER_.

#### b) Install Docker Desktop

1) Install from https://docs.docker.com/desktop/install/windows-install/.
2) Select the option to use WSL 2.
3) Restart the PC.

#### c) Install the Nominatim server and run it in a Docker container

1) Open Docker
2) Open the console (search for the "Command Prompt" application in the start menu)
3) Run the command:

```sh
docker run -it --rm -e PBF_URL=https://download.geofabrik.de/south-america/argentina-latest.osm.pbf -e REPLICATION_URL=https://download.geofabrik.de/south-america/argentina-updates/ -e IMPORT_STYLE=extratags -e IMPORT_WIKIPEDIA=true -p 8080:8080  -v /osm-maps/extras:/nominatim/extras --name nominatim mediagis/nominatim:4.3
```

Explanation:

- _docker run_: basic command to create and run a new container

- _-it_: specify that the container should run interactively in the console

- _--rm_: specify that the container should be automatically removed when finished

- _-e_: create an object in the environment

  - _PBF_URL_: URL to the OpenStreetMap PBF file for Argentina
  
  - _REPLICATION_URL_: URL to the OpenStreetMap PBF file with updates for Argentina. This allows the container to update when it is run.
  
  - _IMPORT_WIKIPEDIA_: enables importing data from Wikipedia
  
  - _NOMINATIM_PASSWORD_: password to access the Nominatim server
  
- _-v_: mounts a volume called "nominatim-data" to the "/var/lib/postgresql/14/main" directory inside the container. This allows the container to store data, such as the geocoding database and updates, persistently and outside the container.

The download may take several minutes. Once it is finished, the container should have been created in Docker and should be running. We can verify this by typing a code in the console that shows us all the containers that are currently active:

```sh
docker ps --filter "status=running"
```

All done! We can now start making queries to our server, as long as it is active. In the [scripts](./scripts/) folder of this repository we provide youw with code to make queries from Python or R. Let's start geocoding!

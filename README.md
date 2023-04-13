# OpenSourceGeocoding

For the English version, clich here (forthcoming).

## Instructivo para instalar y utilizar servidores de geolocalización de código abierto

El objetivo de este repositorio es explicar todos los pasos necesarios para instalar un servicio de georreferenciación de código abierto en un servidor local y hacerle consultas.

### Requisitos:

- X GB de espacio libre.


### 1) Instalación de Linux

Utilizaremos Docker para alojar el servidor.

En primer lugar, tenemos que poder correr Linux en nuestra computadora, ya que lo usaremos como motor backend para procesar y administrar el contenedor en Docker en el cual se alojará nuestro servidor de consulta para georreferenciar direcciones.

En Windows, esto se consigue instalando WSL ("Windows Subsystem for Linux"). Éste es un aplicativo de Windows que nos permite usar herramientas de Linux en una computadora con Windows, con una arquitectura liviana y eficiente.

Para instalar la última versión de WSL en windows, seguir los siguientes pasos:
1) Presionar las teclas Windows+R para abrir el cuadro de diálogo Ejecutar.
2) Escribir 'powershell' y presionar CTRL+SHIFT+ENTER para abrir la consola de Windows PowerShell como administrador.
3) Escribir 'wsl --install' y presionar ENTER.

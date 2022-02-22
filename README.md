# Maurogram Resubido
_Proyecto clon de Instagram basado en Python (Sin documentar)_

## Pre-requisitos

* [Python](https://www.python.org/downloads/)
* [Cmder](https://cmder.net/)

## Instalación

Clonar repositorio
```
git clone https://github.com/MauricioVrx/Maurogram.git
```

Acceder a la carpeta
```
cd Maurogram/
```

Crear entorno virtual de python
```
py -m venv venv
```

Acceder al entorno virtual que hemos creado
```
venv\Scripts\activate.bat
```

Instalar los requerimientos necesarios dentro del entorno virtual
```
pip install -r requeriments.txt
```

Verifiquemos que los paquetes se han instalado  correctamente
```
pip freeze
```
Nos debe mostrar:
* asgiref==3.3.1
* Django==3.1.6
* Pillow==9.0.1
* pytz==2021.1
* sqlparse==0.4.1

## Correos electrónicos
Para poder usar el módulo hay que ingresar un correo y la contraseña en "maurogram/settings.py"
* 167 EMAIL_HOST_USER = 'TuCorreo'
* 168 EMAIL_HOST_PASSWORD = 'TuContraseña'

Te puedes guiar [Aqui](https://dev.to/abderrahmanemustapha/how-to-send-email-with-django-and-gmail-in-production-the-right-way-24ab) 
a partir del "The Gmail part" 

### Iniciar Maurogram
```
py manage.py runserver
```

# Portal-SD
Portal para diferentes funciones orientadas a Service Desk como: 
Aplicación web que centraliza múltiples funcionalidades, incluyendo:

-Gestión y control de stock
-Búsqueda de equipamiento mediante integración con GLPI
-Formularios digitales para entrega y devolución de dispositivos
-Acceso a recursos compartidos estilo SharePoint

Diseñado para optimizar los procesos operativos y centralizar la información en un único entorno accesible.

Para utilizar la aplicación, es necesario crear un archivo .env en la raíz del proyecto con las siguientes variables de entorno:

RUTA_FIRMAS=
DB_HOST=
DB_PORT=
DB_USER=
DB_PASSWORD=
DB_NAME=
LOGO_PATH=
SECRET_KEY=
SMTP_SERVER=
SMTP_PORT=
HOST=
GLPI_API_URL=
GLPI_APP_TOKEN=
GLPI_USER_TOKEN=

Estas variables configuran el acceso a la base de datos, servicios de firma, autenticación, servidor de correo y la integración con la API de GLPI.

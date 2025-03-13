
# Plataforma de gestión de turnos

En proceso

## Deployment

### Info DB
- NAME: postgres
- USER: postgres
- PASSWORD: Hh,NBAKe#{a!Syd
- HOST: db.gvvsnkjmjmtmdlbilxip.supabase.co
- PORT: 5432

### Lista de comandos
1- Posicionarse en el proyecto, si no lo estás
```bash
cd apirest-RST
```

> [!CAUTION]
> Por temas de seguridad, las variables de entorno (los valores declarados para la bd) no se suben al repo de github pero se puede decargar el archivo '.env' del drive de sistemas o en https://drive.google.com/file/d/1ycDv90bRqc5vlaVg2Ez6vkYW9QbdhF0q/view?usp=sharing y ponerlos dentro de la carpeta 'apirest-rst'

2- Activar el entorno virtual
```bash
venv\Scripts\activate
```

> [!NOTE]
>  En el caso de no poder activar el entorno virtual, borrá la carpeta 'venv' del directorio del proyecto y ejecutá:
> 
> 1- Crear el entorno virtual
> ```bash
> py -m virtualenv venv
> ```
>
> 2- Ejecutar archivo activate
> ```bash
> venv\Scripts\activate
> ```

4- Migraciones DB:
```bash
py manage.py makemigrations
```
```bash
py manage.py migrate
```

5- Correr el servidor: 
```bash
py manage.py runserver
```


### URL para documentación 

Swagger
http://127.0.0.1:8000/docs/

Redoc
http://127.0.0.1:8000/redocs/

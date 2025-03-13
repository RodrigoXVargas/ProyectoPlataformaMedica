# Plataforma-node

En proceso

## Deployment

### Estructura del proyecto
plataforma-node/  
|-- documentation/  
|-- src/  
|   |-- controllers/  
|   |-- enum/  
|   |-- models/  
|   |   |-- relations/  
|   |-- routes/  
|   |-- schemas/  
|   |-- servicios/  
|   |-- config.ts  
|   |-- index.ts  
|   |-- sequlize.ts  
|   |-- types.ts  
|-- .env  
|-- .gitignore  
|-- package.json  
|-- tsconfig.json  


La carpeta "src" contiene el código fuente del proyecto. Se divide en cuatro subcarpetas:

- "controllers": Esta carpeta contiene los controladores de la aplicación. Los controladores son responsables de manejar las solicitudes HTTP de los usuarios.
- "models": Esta carpeta contiene los modelos de datos de la aplicación. Los modelos representan las entidades de datos de la aplicación.
      - "relations": Contiene las tablas intermedias de las relaciones many-to-many
- "routes": Esta carpeta contiene las rutas de la aplicación. Las rutas definen cómo la aplicación responde a las solicitudes HTTP de los usuarios.
- "schemas": Esta carpeta contiene los esquemas de datos de la aplicación. Los esquemas definen la estructura de los datos de la aplicación.

### Lista de comandos
1- Posicionarse en el proyecto, si no lo estás
```bash
cd plataforma-node
```

> [!CAUTION]
> Por temas de seguridad, las variables de entorno (los valores declarados para la bd) no se suben al repo de github pero se puede decargar el archivo '.env' del drive de sistemas (Mi unidad > Proyecto plataforma > node) y ponerlo dentro del directorio 'plataforma-node'. ¡Asegurarse de que '.env' tenga el '.'!
>
>![image](https://github.com/RSTArgentina/plataformaRST/assets/128536319/6b056fbb-94c1-4488-b5a1-da838a59f06a)

2- Instalar/actualizar dependencias: 
```bash
npm i
```

3- Correr el servidor: 
```bash
npm run dev
```

### Acceder a la documentación  
Abrir el archivo `index.html` ubicado en `plataformaRST > plataforma-node > documentation`

![image](https://github.com/RSTArgentina/plataformaRST/assets/128536319/157b2a5a-005d-4301-bcf2-788c136c03df)





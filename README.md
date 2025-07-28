# 🖼️ Image Processing Service(Cloudinary-like)

Este proyecto consiste en crear un sistema backend para un servicio de procesamiento de imágenes similar a **Cloudinary**, permitiendo a los usuarios subir imágenes, transformarlas (redimensionar, recortar, rotar, aplicar filtros, etc.) y recuperarlas en distintos formatos.

---

## 🚀 Tecnologías y Herramientas

- **Lenguaje**: Python (Fast Api)
- **Almacenamiento de Imágenes**: AWS S3 (Para dev MiniO)
- **Autenticación**: JWT (JSON Web Tokens)
- **Procesamiento de Imágenes**: Pillow
- **Base de Datos**: PostgreSQL
- **Infraestructura**: AWS
- **Procesamiento asíncrono**:  Kafka 

---

## 📦 Características

### 👤 Autenticación de Usuarios
- **Registro**: los usuarios pueden crear una cuenta.
- **Inicio de Sesión**: acceso mediante nombre de usuario y contraseña.
- **Protección JWT**: acceso seguro a endpoints.

### 🖼️ Gestión de Imágenes
- **Subida de Imágenes**: mediante multipart/form-data.
- **Transformaciones**:
  - Redimensionar
  - Recortar
  - Rotar
  - Aplicar marca de agua
  - Voltear horizontal/vertical
  - Comprimir
  - Cambiar formato (JPEG, PNG, etc.)
  - Filtros (blanco y negro, sepia, etc.)
- **Recuperar Imágenes**: obtener imágenes originales o transformadas.
- **Listar Imágenes**: con metadatos por usuario.

 
## 📄Licencia
Este proyecto está licenciado bajo la licencia MIT: consulte el archivo [LICENSE](LICENSE) para obtener más detalles.


## 👀Contacto
Si tiene alguna pregunta o necesita más ayuda, no dude en ponerse en contacto conmigo en [codeartprogrammer@gmail.com].

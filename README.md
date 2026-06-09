# Mayorista — Sistema de Gestión para Comercio Mayorista (Proyecto en desarrollo activo)

Sistema web de gestión para un negocio mayorista. El proyecto incluye un backend completo con API REST y tiene planificado un frontend y un portal exclusivo para clientes mayoristas.

## Estado del proyecto

- Backend (API REST) — en etapa final
- Frontend (panel interno para admin y empleados) — pronto
- Portal de clientes mayoristas — pronto

## Descripción

El sistema permite gestionar productos, stock, ventas y usuarios de un negocio mayorista. Cuenta con dos tipos de usuarios internos (administrador y empleado) y tiene planificado un portal externo para clientes mayoristas donde podrán hacer pedidos online sin necesidad de llamar o ir al local.

La idea central es que el admin tenga el menor trabajo operativo posible: aprueba a un cliente mayorista una sola vez, y a partir de ahí ese cliente gestiona sus propios pedidos de forma autónoma.

## Stack tecnológico

**Backend**
- Python
- FastAPI
- SQLAlchemy (ORM)
- PostgreSQL

**Seguridad**
- JWT (autenticación con tokens)
- bcrypt (hasheo de contraseñas)

## Funcionalidades del backend

### Productos
- Listar productos con stock
- Buscar por nombre (búsqueda parcial)
- Buscar por código de barras
- Crear, actualizar y eliminar productos (solo admin)
- Cada producto tiene precio minorista y mayorista, stock actual y stock mínimo configurado por producto

### Ventas
- Registrar ventas con descuento automático de stock al confirmar
- Soporte para lector de código de barras (foco automático en el campo de búsqueda)
- Alerta automática cuando el stock llega al mínimo configurado
- Editar y eliminar líneas de una venta con recálculo de totales y devolución de stock
- Soporte para envío a domicilio o retiro en el local

### Reportes (solo admin)
- Total acumulado de ventas por período personalizado
- Productos más vendidos por período, ordenados por cantidad

### Usuarios
- Registro y login con autenticación JWT
- Roles: administrador y empleado
- Desactivar usuarios sin eliminarlos
- Cambio de contraseña con verificación de la contraseña actual
- Ver historial de ventas por usuario

## Estructura del proyecto

```
mayorista/
├── main.py
└── app/
    ├── database.py
    ├── seguridad.py
    ├── models/
    │   ├── usuarios.py
    │   ├── productos.py
    │   └── ventas.py
    ├── routes/
    │   ├── usuarios.py
    │   ├── productos.py
    │   └── ventas.py
    └── schemas/
        ├── usuarios.py
        ├── productos.py
        └── ventas.py
```

## Cómo correr el proyecto

**1. Clonar el repositorio**
```
git clone https://github.com/tu-usuario/mayorista
cd mayorista
```

**2. Instalar dependencias**
```
pip install fastapi uvicorn sqlalchemy psycopg2-binary passlib bcrypt python-jose python-multipart
```

**3. Configurar la base de datos**

Crear una base de datos PostgreSQL llamada `mayorista_db` y actualizar la URL de conexión en `app/database.py` con tu propio usuario y contraseña de PostgreSQL.

**4. Levantar el servidor**
```
python -m uvicorn main:app --reload
```

**5. Ver la documentación interactiva**
```
http://127.0.0.1:8000/docs
```

## Próximos pasos

- Frontend con HTML, Tailwind CSS y JavaScript
- Portal de clientes mayoristas con registro, catálogo y pedidos online
- Generación de comprobantes en PDF por venta
- Recuperación de contraseña por email

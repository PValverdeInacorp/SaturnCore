# Nuevo Endpoint de Consulta - SaturnCore

## ✅ Cambios Realizados

Se ha agregado un nuevo endpoint para enviar correos de consulta obteniendo datos de **otra base de datos** (`u179238392_inacorp`).

### Archivos Creados/Modificados:

#### 1. **Servicios** (`apps/correos/application/services/`)
- ✅ `consulta_correo_service.py` - Nuevo servicio que llama:
  - `SP_OBTENER_CONSULTA_ULTIMO_PEDIDO_CORREO()` - Obtiene productos
  - `SP_OBTENER_DATOS_ORDEN_COMPRA()` - Obtiene email

#### 2. **Use Cases** (`apps/correos/application/use_cases/`)
- ✅ `enviar_correo_consulta.py` - Nuevo use case que orquesta:
  - Llamada a servicios de consulta
  - Renderización de HTML
  - Envío via Microsoft Graph

#### 3. **API** (`apps/correos/api/`)
- ✅ `views.py` - Agregada clase `EnviarCorreoConsultaView`
- ✅ `serializers.py` - Agregado `EnviarCorreoConsultaSerializer`
- ✅ `urls.py` - Agregada ruta `POST /api/correos/consulta/`

#### 4. **Templates** (`apps/correos/templates/correos/`)
- ✅ `consulta_email.html` - Template HTML para tabla de productos

#### 5. **Configuración** (`config/`)
- ✅ `settings.py` - Agregada conexión `"pagina_web"` a BD `u179238392_inacorp`

---

## 🔧 Configuración Requerida en `.env`

```
# DB PAGINA WEB INACORP
DB_NAME_PAGINA_WEB=u179238392_inacorp
DB_USER_PAGINA_WEB=u179238392_inacorp
DB_PASSWORD_PAGINA_WEB=?iUM2dKZ240c
DB_HOST_PAGINA_WEB=localhost
DB_PORT_PAGINA_WEB=3306
```

✅ Ya están configurados en tu `.env`

---

## 📋 Flujo del Nuevo Endpoint

```
POST /api/correos/consulta/
│
├─ ConsultaCorreoService.construir_html_consulta()
│  ├─ Ejecuta: SP_OBTENER_CONSULTA_ULTIMO_PEDIDO_CORREO()
│  │  └─ Retorna: ReferenciaProducto, NombreProducto, Cantidad, Precio
│  ├─ Ejecuta: SP_OBTENER_DATOS_ORDEN_COMPRA()
│  │  └─ Retorna: EMAIL (y otros datos)
│  └─ Renderiza: consulta_email.html con tabla
│
├─ GraphProvider.enviar()
│  ├─ Obtiene token de Microsoft
│  └─ Envía correo con tabla de productos
│
└─ Response: { "ok": true, "email_destino": "...", ... }
```

---

## 🚀 Cómo Usar

### 1. Reinicia Django
```bash
Ctrl+C (si está corriendo)
python manage.py runserver
```

### 2. Abre Swagger
```
http://localhost:8000/swagger/
```

### 3. Prueba el endpoint
**POST** `/api/correos/consulta/`

**Body:**
```json
{}
```

(No requiere parámetros, obtiene datos directamente de los SP)

**Response (200):**
```json
{
  "ok": true,
  "mensaje": "Correo enviado correctamente",
  "email_destino": "cliente@ejemplo.com",
  "cantidad_productos": 5,
  "status_code_graph": 202
}
```

---

## 📊 Estructura de Datos

### SP_OBTENER_CONSULTA_ULTIMO_PEDIDO_CORREO()
Retorna:
```
ReferenciaProducto (VARCHAR)
NombreProducto (VARCHAR)
Cantidad (INT)
Precio (DECIMAL)
```

### SP_OBTENER_DATOS_ORDEN_COMPRA()
Retorna:
```
EMAIL (VARCHAR)
... (otros campos)
```

---

## ✅ Endpoints Disponibles Ahora

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/correos/send/` | Enviar correo por orden |
| GET | `/api/correos/pdf/{order_id}/` | Generar PDF de orden |
| **POST** | **`/api/correos/consulta/`** | **Enviar correo de consulta (NUEVO)** |

---

## 🔍 Troubleshooting

Si obtienes error `Can't connect to server`:
- Verifica que DB_HOST_PAGINA_WEB=localhost (no host.docker.internal)
- Verifica credenciales en .env
- Prueba conectar a la BD directamente desde MySQL client

Si obtiene error `SP not found`:
- Verifica que los SP existan en la BD: `u179238392_inacorp`
- Ejecuta: `SHOW PROCEDURE STATUS WHERE Name LIKE 'SP_OBTENER%';`

---

**Última actualización:** 15 de Abril de 2026
**Estado:** Listo para testing

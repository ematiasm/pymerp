# 📊 Modelos de Datos - Sistema POS

## ✅ Fase 1 Completada: Modelos de Datos

Se han creado todos los modelos de datos necesarios para el sistema de Punto de Venta (POS) en el archivo `/workspace/backend/app/models.py`.

---

## 📋 Entidades Implementadas

### 1. **Category** (Categoría)
- **Propósito**: Organizar productos por categorías
- **Campos principales**:
  - `name`: Nombre de la categoría (1-100 caracteres)
  - `description`: Descripción opcional
  - `is_active`: Estado activo/inactivo
- **Relaciones**: Uno a muchos con Product

### 2. **Product** (Producto)
- **Propósito**: Representar los artículos vendibles
- **Campos principales**:
  - `name`: Nombre del producto
  - `description`: Descripción detallada
  - `barcode`: Código de barras (único, indexado)
  - `sku`: SKU interno (único, indexado)
  - `price`: Precio de venta
  - `cost`: Costo de compra
  - `stock`: Cantidad en inventario
  - `min_stock`: Stock mínimo para alertas
  - `max_stock`: Stock máximo opcional
  - `is_taxable`: Si aplica impuestos
  - `tax_rate`: Porcentaje de impuesto (0-100%)
  - `allow_sale_without_stock`: Permitir vender sin stock
- **Relaciones**: 
  - Muchos a uno con Category
  - Uno a muchos con SaleItem

### 3. **Customer** (Cliente)
- **Propósito**: Gestionar información de clientes
- **Campos principales**:
  - `name`: Nombre completo o razón social
  - `email`: Correo electrónico
  - `phone`: Teléfono
  - `document_type`: Tipo de documento (DNI, RUC, etc.)
  - `document_number`: Número de documento
  - `address`: Dirección
  - `notes`: Notas adicionales
- **Relaciones**: Uno a muchos con Sale

### 4. **Sale** (Venta)
- **Propósito**: Registrar transacciones de venta
- **Campos principales**:
  - `invoice_number`: Número de factura/ticket (único)
  - `subtotal`: Subtotal antes de impuestos
  - `discount`: Descuento aplicado
  - `tax_amount`: Monto de impuestos
  - `total`: Total final
  - `payment_method`: Método de pago (cash, card, transfer, other)
  - `amount_paid`: Monto pagado por el cliente
  - `change_amount`: Cambio/devolución
  - `notes`: Notas de la venta
  - `status`: Estado (completed, cancelled, refunded)
- **Relaciones**:
  - Muchos a uno con Customer
  - Muchos a uno con User (cashier)
  - Uno a muchos con SaleItem

### 5. **SaleItem** (Ítem de Venta)
- **Propósito**: Detallar productos dentro de una venta
- **Campos principales**:
  - `quantity`: Cantidad vendida
  - `unit_price`: Precio unitario al momento de la venta
  - `discount`: Descuento aplicado al ítem
  - `tax_rate`: Impuesto aplicado
  - `tax_amount`: Monto de impuesto del ítem
  - `subtotal`: Subtotal del ítem
  - `total`: Total del ítem
- **Relaciones**:
  - Muchos a uno con Product
  - Muchos a uno con Sale

### 6. **Supplier** (Proveedor) - *Preparación Fase 2*
- **Propósito**: Gestionar proveedores para compras
- **Campos principales**:
  - `name`: Nombre del proveedor
  - `contact_name`: Nombre de contacto
  - `email`: Correo electrónico
  - `phone`: Teléfono
  - `address`: Dirección
  - `document_type`: Tipo de documento
  - `document_number`: Número de documento

### 7. **CashRegister** (Caja/Turno) - *Preparación Fase 2*
- **Propósito**: Gestionar apertura y cierre de cajas
- **Campos principales**:
  - `opening_balance`: Saldo inicial
  - `closing_balance`: Saldo final
  - `opening_notes`: Notas de apertura
  - `closing_notes`: Notas de cierre
  - `status`: Estado (open, closed, suspended)
  - `opened_at`: Fecha/hora de apertura
  - `closed_at`: Fecha/hora de cierre
- **Relaciones**: Muchos a uno con User (cashier)

---

## 🔗 Relaciones entre Modelos

```
User ──────────────┬────────────── Sale
                   │                │
                   │                └── SaleItem ─── Product
                   │                                 │
                   └── CashRegister                 Category
                   
Customer ──────────┘
```

### Diagrama ER Simplificado

```
┌─────────────┐       ┌──────────────┐       ┌─────────────┐
│  Category   │◄──────│   Product    │──────►│  SaleItem   │
└─────────────┘       └──────────────┘       └─────────────┘
                                                  ▲
┌─────────────┐       ┌──────────────┐           │
│  Customer   │◄──────│     Sale     │◄──────────┘
└─────────────┘       └──────────────┘
                           ▲
┌─────────────┐            │
│    User     │────────────┘ (cashier)
└─────────────┘

┌─────────────┐
│    User     │◄──────┐
└─────────────┘       │
                      │
┌─────────────────┐   │
│ CashRegister    │───┘
└─────────────────┘
```

---

## 🎯 Enums Definidos

### SaleStatus
- `COMPLETED` = "completed"
- `CANCELLED` = "cancelled"
- `REFUNDED` = "refunded"

### PaymentMethod
- `CASH` = "cash"
- `CARD` = "card"
- `TRANSFER` = "transfer"
- `OTHER` = "other"

### CashRegisterStatus
- `OPEN` = "open"
- `CLOSED` = "closed"
- `SUSPENDED` = "suspended"

---

## 📦 Estructura de Clases por Modelo

Cada entidad sigue el patrón SQLModel/Pydantic:

```python
# Ejemplo con Product
class ProductBase(SQLModel):
    # Campos compartidos
    
class ProductCreate(ProductBase):
    # Campos para creación (incluye foreign keys)
    
class ProductUpdate(SQLModel):
    # Campos opcionales para actualización
    
class Product(ProductBase, table=True):
    # Modelo de base de datos (incluye id, timestamps, relaciones)
    
class ProductPublic(ProductBase):
    # Campos para respuesta API (incluye id, timestamps)
    
class ProductsPublic(SQLModel):
    # Respuesta paginada
    data: list[ProductPublic]
    count: int
```

---

## 🔍 Características Especiales

### Validaciones Implementadas
- ✅ Longitudes mínimas y máximas en campos string
- ✅ Validación de rangos numéricos (ge, le, gt)
- ✅ Precisión decimal (2 decimales para moneda)
- ✅ Emails válidos con EmailStr
- ✅ UUIDs generados automáticamente
- ✅ Timestamps UTC automáticos (created_at, updated_at)

### Índices y Restricciones
- ✅ `barcode` y `sku` únicos e indexados en Product
- ✅ `invoice_number` único en Sale
- ✅ Foreign keys con ondelete apropiados:
  - `CASCADE`: Elimina dependientes (ej. SaleItem al eliminar Sale)
  - `SET NULL`: Mantiene registro pero nullifica referencia (ej. Customer en Sale)
  - `RESTRICT`: Previene eliminación si hay dependencias (ej. User en Sale)

### Relaciones Bidireccionales
- ✅ Todas las relaciones están definidas con `back_populates`
- ✅ Cascade delete configurado donde corresponde

---

## 🧪 Verificación

Los modelos han sido verificados exitosamente:

```bash
✅ Todos los modelos POS importados correctamente
✅ Todos los modelos (incluyendo User, Item) importados correctamente
```

---

## 📝 Próximos Pasos (Fase 1 - Semana 2)

1. **Crear endpoints API para Products**:
   - `POST /api/v1/products/` - Crear producto
   - `GET /api/v1/products/` - Listar productos (con filtros, búsqueda, paginación)
   - `GET /api/v1/products/{id}` - Obtener producto
   - `PUT /api/v1/products/{id}` - Actualizar producto
   - `DELETE /api/v1/products/{id}` - Eliminar producto
   - `PATCH /api/v1/products/{id}/stock` - Ajustar stock

2. **Crear endpoints API para Categories**:
   - CRUD completo similar a products

3. **Crear endpoints API para Customers**:
   - CRUD completo
   - Búsqueda por documento/email

4. **Migraciones de Base de Datos**:
   - Generar migración Alembic para nuevos modelos
   - Ejecutar migración en PostgreSQL

---

## 📚 Referencias

- **Archivo de modelos**: `/workspace/backend/app/models.py`
- **Plan del proyecto**: `/workspace/PLAN_PROYECTO_POS.md`
- **Documentación FastAPI**: https://fastapi.tiangolo.com/
- **Documentación SQLModel**: https://sqlmodel.tiangolo.com/

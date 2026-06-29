# Plan de Proyecto: Sistema de Punto de Venta (POS)

## 📋 Resumen Ejecutivo

Desarrollo de un sistema de Punto de Venta (POS) moderno basado en el template **Full Stack FastAPI**, diseñado para pequeñas y medianas empresas que requieren gestión de ventas, inventario, clientes y reportes en tiempo real.

### Stack Tecnológico
- **Backend**: FastAPI + SQLModel + PostgreSQL
- **Frontend**: React 19 + TypeScript + Vite + Tailwind CSS + shadcn/ui
- **Base de Datos**: PostgreSQL
- **Autenticación**: JWT (JSON Web Token)
- **Contenerización**: Docker Compose
- **Testing**: Pytest (backend) + Playwright (frontend E2E)

---

## 🎯 Objetivos del Proyecto

### Objetivo Principal
Crear un sistema POS completo que permita:
- Registrar y procesar ventas rápidamente
- Gestionar inventario de productos
- Administrar clientes y proveedores
- Generar reportes y análisis de ventas
- Soportar múltiples usuarios con roles diferenciados
- Operar offline con sincronización posterior (fase 2)

### Objetivos Específicos
1. **Interfaz intuitiva** para cajeros con mínimo entrenamiento requerido
2. **Búsqueda rápida** de productos por código de barras, nombre o SKU
3. **Gestión de inventario** en tiempo real con alertas de stock bajo
4. **Múltiples métodos de pago**: efectivo, tarjeta, transferencia
5. **Tickets/facturas** imprimibles o digitales
6. **Dashboard administrativo** con KPIs de ventas
7. **Control de caja** con apertura/cierre de turno
8. **Descuentos y promociones** configurables

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND (React)                      │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐   │
│  │    POS      │ │  Inventario │ │    Administración   │   │
│  │   (Caja)    │ │             │ │   (Dashboard/Reportes)│  │
│  └─────────────┘ └─────────────┘ └─────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼ HTTP/REST API
┌─────────────────────────────────────────────────────────────┐
│                      BACKEND (FastAPI)                       │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐   │
│  │  Auth    │ │  Ventas  │ │Productos │ │   Reportes   │   │
│  │  (JWT)   │ │          │ │Inventario│ │   Analytics  │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘   │
│                                                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐   │
│  │Clientes  │ │Proveedores│ │  Caja    │ │Configuración │   │
│  │          │ │          │ │(Turnos)  │ │   Sistema    │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼ SQLModel ORM
┌─────────────────────────────────────────────────────────────┐
│                   DATABASE (PostgreSQL)                      │
│  Tablas: users, products, categories, sales, sale_items,    │
│          customers, suppliers, inventory_movements,         │
│          cash_registers, payments, discounts, settings      │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Fases de Desarrollo

### **Fase 1: Núcleo del Sistema (Semanas 1-4)**

#### Semana 1: Configuración y Modelos Base
- [ ] Configurar entorno de desarrollo
- [ ] Definir modelos de datos principales
- [ ] Implementar migraciones iniciales
- [ ] Configurar autenticación y roles

**Modelos a crear:**
```python
# models.py - Nuevos modelos
- Product (productos)
- Category (categorías de productos)
- Customer (clientes)
- Supplier (proveedores)
- Sale (ventas cabecera)
- SaleItem (detalle de venta)
- PaymentMethod (métodos de pago)
- Payment (pagos)
- InventoryMovement (movimientos de inventario)
- CashRegister (caja/turno)
```

#### Semana 2: Gestión de Productos e Inventario
- [ ] CRUD de productos
- [ ] CRUD de categorías
- [ ] Gestión de stock (entradas/salidas)
- [ ] Búsqueda y filtrado de productos
- [ ] Códigos de barra/SKU
- [ ] Precios (costo, venta, oferta)

**Endpoints backend:**
```python
# api/routes/products.py
GET    /products/           # Listar productos con filtros
POST   /products/           # Crear producto
GET    /products/{id}       # Obtener producto
PUT    /products/{id}       # Actualizar producto
DELETE /products/{id}       # Eliminar producto
POST   /products/bulk/      # Carga masiva
GET    /products/search/    # Búsqueda avanzada
POST   /products/{id}/stock # Ajuste de stock
```

#### Semana 3: Módulo de Ventas (POS)
- [ ] Interfaz de punto de venta
- [ ] Carrito de compras
- [ ] Proceso de checkout
- [ ] Múltiples métodos de pago
- [ ] Impresión de tickets
- [ ] Registro de ventas

**Endpoints backend:**
```python
# api/routes/sales.py
POST   /sales/              # Registrar venta
GET    /sales/              # Listar ventas
GET    /sales/{id}          # Detalle de venta
GET    /sales/ticket/{id}   # Generar ticket
POST   /sales/{id}/cancel   # Cancelar venta
GET    /sales/today/        # Ventas del día
```

#### Semana 4: Clientes y Dashboard Básico
- [ ] CRUD de clientes
- [ ] Historial de compras por cliente
- [ ] Dashboard con métricas básicas
- [ ] Reporte de ventas diarias
- [ ] Pruebas integrales

---

### **Fase 2: Funcionalidades Avanzadas (Semanas 5-8)**

#### Semana 5: Gestión de Caja y Turnos
- [ ] Apertura de caja
- [ ] Arqueo de caja
- [ ] Cierre de turno
- [ ] Control de efectivo
- [ ] Reporte de cierres

**Modelos adicionales:**
```python
class CashRegisterOpen(SQLModel, table=True):
    id: UUID
    user_id: UUID
    opening_amount: Decimal
    opened_at: datetime
    
class CashRegisterClose(SQLModel, table=True):
    id: UUID
    register_open_id: UUID
    closing_amount: Decimal
    expected_amount: Decimal
    difference: Decimal
    closed_at: datetime
    observations: str | None
```

#### Semana 6: Descuentos y Promociones
- [ ] Descuentos por porcentaje/fijo
- [ ] Promociones por volumen
- [ ] Cupones de descuento
- [ ] Lista de precios múltiple
- [ ] Precios especiales por cliente

#### Semana 7: Proveedores y Compras
- [ ] CRUD de proveedores
- [ ] Órdenes de compra
- [ ] Recepción de mercancía
- [ ] Costeo de productos
- [ ] Reporte de compras

#### Semana 8: Reportes Avanzados
- [ ] Reporte de ventas por período
- [ ] Productos más vendidos
- [ ] Ventas por vendedor
- [ ] Ventas por categoría
- [ ] Análisis de rentabilidad
- [ ] Exportación a Excel/PDF

---

### **Fase 3: Optimización y Producción (Semanas 9-12)**

#### Semana 9: UX/UI y Optimización
- [ ] Mejoras de interfaz
- [ ] Atajos de teclado
- [ ] Modo offline (básico)
- [ ] Optimización de consultas
- [ ] Caché de productos frecuentes

#### Semana 10: Seguridad y Auditoría
- [ ] Logs de auditoría
- [ ] Permisos granulares
- [ ] Backup automático
- [ ] Encriptación de datos sensibles
- [ ] Validaciones adicionales

#### Semana 11: Testing y QA
- [ ] Tests unitarios completos
- [ ] Tests de integración
- [ ] Tests E2E con Playwright
- [ ] Pruebas de carga
- [ ] Corrección de bugs

#### Semana 12: Despliegue y Documentación
- [ ] Configuración de producción
- [ ] Documentación de usuario
- [ ] Manual técnico
- [ ] Capacitación
- [ ] Go-live

---

## 🗂️ Estructura de Archivos Propuesta

```
backend/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py          # (existente)
│   │   │   ├── users.py         # (existente)
│   │   │   ├── products.py      # [NUEVO]
│   │   │   ├── categories.py    # [NUEVO]
│   │   │   ├── customers.py     # [NUEVO]
│   │   │   ├── suppliers.py     # [NUEVO]
│   │   │   ├── sales.py         # [NUEVO]
│   │   │   ├── payments.py      # [NUEVO]
│   │   │   ├── inventory.py     # [NUEVO]
│   │   │   ├── cash_register.py # [NUEVO]
│   │   │   └── reports.py       # [NUEVO]
│   │   └── deps.py              # (existente - actualizar)
│   ├── core/
│   │   ├── config.py            # (actualizar con settings POS)
│   │   ├── db.py                # (existente)
│   │   └── security.py          # (existente)
│   ├── models.py                # [AMPLIAR significativamente]
│   ├── crud.py                  # [AMPLIAR]
│   ├── alembic/
│   │   └── versions/            # [NUEVAS MIGRACIONES]
│   └── utils/
│       ├── barcode.py           # [NUEVO] Generación/lectura códigos
│       ├── reports.py           # [NUEVO] Generación PDF/Excel
│       └── calculations.py      # [NUEVO] Cálculos financieros
└── tests/
    ├── test_products.py         # [NUEVO]
    ├── test_sales.py            # [NUEVO]
    ├── test_inventory.py        # [NUEVO]
    └── ...

frontend/
├── src/
│   ├── components/
│   │   ├── POS/
│   │   │   ├── ProductSearch.tsx     # [NUEVO]
│   │   │   ├── ShoppingCart.tsx      # [NUEVO]
│   │   │   ├── CheckoutModal.tsx     # [NUEVO]
│   │   │   ├── PaymentSelector.tsx   # [NUEVO]
│   │   │   └── TicketPreview.tsx     # [NUEVO]
│   │   ├── Products/
│   │   │   ├── ProductList.tsx       # [NUEVO]
│   │   │   ├── ProductForm.tsx       # [NUEVO]
│   │   │   └── StockAdjustment.tsx   # [NUEVO]
│   │   ├── Customers/
│   │   │   ├── CustomerList.tsx      # [NUEVO]
│   │   │   └── CustomerForm.tsx      # [NUEVO]
│   │   ├── Reports/
│   │   │   ├── SalesReport.tsx       # [NUEVO]
│   │   │   ├── Dashboard.tsx         # [NUEVO]
│   │   │   └── Charts/               # [NUEVO]
│   │   └── CashRegister/
│   │       ├── OpenRegister.tsx      # [NUEVO]
│   │       ├── CloseRegister.tsx     # [NUEVO]
│   │       └── CashMovement.tsx      # [NUEVO]
│   ├── routes/
│   │   ├── _layout/
│   │   │   ├── pos.tsx               # [NUEVO]
│   │   │   ├── products.tsx          # [NUEVO]
│   │   │   ├── customers.tsx         # [NUEVO]
│   │   │   ├── reports.tsx           # [NUEVO]
│   │   │   └── settings.tsx          # [NUEVO]
│   ├── hooks/
│   │   ├── useCart.ts                # [NUEVO]
│   │   ├── useProducts.ts            # [NUEVO]
│   │   └── useSales.ts               # [NUEVO]
│   └── lib/
│       ├── utils.ts                  # (existente - ampliar)
│       └── calculations.ts           # [NUEVO]
```

---

## 📊 Modelos de Datos Detallados

### Modelo Product
```python
class ProductBase(SQLModel):
    name: str = Field(max_length=255, index=True)
    description: str | None = Field(default=None, max_length=500)
    sku: str = Field(max_length=50, unique=True, index=True)
    barcode: str | None = Field(default=None, max_length=50, index=True)
    cost_price: Decimal = Field(decimal_places=2, ge=0)
    sale_price: Decimal = Field(decimal_places=2, ge=0)
    offer_price: Decimal | None = Field(default=None, decimal_places=2, ge=0)
    stock_quantity: int = Field(default=0, ge=0)
    min_stock: int = Field(default=5, ge=0)  # Alerta cuando stock < min_stock
    is_active: bool = True
    category_id: UUID | None = Field(default=None, foreign_key="category.id")
    supplier_id: UUID | None = Field(default=None, foreign_key="supplier.id")
    image_url: str | None = Field(default=None, max_length=500)
    tax_rate: Decimal = Field(default=0.16, decimal_places=4)  # IVA u otros impuestos
```

### Modelo Sale
```python
class SaleBase(SQLModel):
    invoice_number: str | None = Field(default=None, max_length=50)
    customer_id: UUID | None = Field(default=None, foreign_key="customer.id")
    user_id: UUID = Field(foreign_key="user.id")  # Vendedor
    cash_register_open_id: UUID = Field(foreign_key="cash_register_open.id")
    subtotal: Decimal = Field(decimal_places=2)
    discount: Decimal = Field(default=0, decimal_places=2)
    tax: Decimal = Field(decimal_places=2)
    total: Decimal = Field(decimal_places=2)
    status: SaleStatus = Field(default=SaleStatus.COMPLETED)  # COMPLETED, CANCELLED, REFUNDED
    payment_method: str  # CASH, CARD, TRANSFER, MIXED
    notes: str | None = Field(default=None, max_length=500)
```

### Modelo SaleItem
```python
class SaleItemBase(SQLModel):
    sale_id: UUID = Field(foreign_key="sale.id", primary_key=True)
    product_id: UUID = Field(foreign_key="product.id", primary_key=True)
    quantity: int = Field(gt=0)
    unit_price: Decimal = Field(decimal_places=2)
    discount: Decimal = Field(default=0, decimal_places=2)
    tax: Decimal = Field(decimal_places=2)
    subtotal: Decimal = Field(decimal_places=2)
    total: Decimal = Field(decimal_places=2)
```

---

## 🔐 Roles y Permisos

| Rol | Ventas | Productos | Inventario | Clientes | Reportes | Caja | Admin |
|-----|--------|-----------|------------|----------|----------|------|-------|
| **Admin** | ✅ CRUD | ✅ CRUD | ✅ CRUD | ✅ CRUD | ✅ Todos | ✅ CRUD | ✅ |
| **Manager** | ✅ CRUD | ✅ CRUD | ✅ CRUD | ✅ CRUD | ✅ Limitados | ✅ CRUD | ❌ |
| **Vendedor** | ✅ CRUD | ❌ | ⚠️ Ver | ✅ CRUD | ⚠️ Propias | ⚠️ Apertura/Cierre | ❌ |
| **Cajero** | ✅ CRUD | ❌ | ❌ | ⚠️ Ver | ❌ | ✅ Operar | ❌ |

✅ = Acceso completo | ⚠️ = Acceso limitado | ❌ = Sin acceso

---

## 📈 KPIs y Métricas Clave

### Dashboard Principal
1. **Ventas del Día**: Total, número de transacciones, ticket promedio
2. **Ventas vs Meta**: Comparativa con objetivo diario/mensual
3. **Productos Top 10**: Más vendidos por cantidad y valor
4. **Métodos de Pago**: Distribución porcentual
5. **Alertas de Stock**: Productos por debajo del mínimo
6. **Flujo de Caja**: Entradas vs salidas del día

### Reportes Analíticos
- Ventas por período (diario, semanal, mensual, anual)
- Ventas por vendedor
- Ventas por categoría/producto
- Ventas por hora/día de la semana
- Rentabilidad por producto
- Rotación de inventario
- Clientes más frecuentes

---

## 🧪 Estrategia de Testing

### Backend (Pytest)
```python
# tests/test_sales.py
def test_create_sale_success()
def test_create_sale_insufficient_stock()
def test_cancel_sale()
def test_get_sales_by_date()
def test_sale_calculations()

# tests/test_inventory.py
def test_stock_update_on_sale()
def test_stock_alert_threshold()
def test_inventory_movement_log()
```

### Frontend (Playwright)
```typescript
// tests/e2e/pos.spec.ts
test('complete sale flow', async ({ page }) => {
  // Login
  // Search product
  // Add to cart
  // Checkout
  // Select payment
  // Print ticket
})

test('inventory update after sale', async ({ page }) => {
  // Verify stock decreases after sale
})
```

---

## 🚀 Plan de Despliegue

### Entornos
1. **Desarrollo**: Docker Compose local
2. **Staging**: Réplica de producción para testing
3. **Producción**: Docker Compose + Traefik + HTTPS

### Requisitos de Servidor (Producción)
- **CPU**: 2+ cores
- **RAM**: 4GB mínimo, 8GB recomendado
- **Almacenamiento**: 20GB SSD + espacio para backups
- **SO**: Ubuntu 22.04 LTS o similar

### Backup Strategy
- **Database**: Backup diario automático (pg_dump)
- **Retención**: 30 días
- **Offsite**: Copia semanal a cloud storage

---

## 📝 Consideraciones de Seguridad

1. **Autenticación**: JWT con refresh tokens
2. **Autorización**: RBAC (Role-Based Access Control)
3. **Datos Sensibles**: Encriptación en reposo
4. **Logs**: Auditoría de todas las transacciones
5. **HTTPS**: Obligatorio en producción
6. **Rate Limiting**: Prevenir abusos en API
7. **Validación**: Input validation en todos los endpoints
8. **SQL Injection**: Prevención mediante SQLModel ORM

---

## 🔄 Integraciones Futuras (Roadmap)

### Fase 4+ (Post-MVP)
- [ ] **Facturación Electrónica**: Integración con SAT/Hacienda
- [ ] **E-commerce**: Sincronización con tienda online
- [ ] **TPV Virtual**: Integración con pasarelas de pago
- [ ] **App Móvil**: Para inventario y ventas externas
- [ ] **Multi-sucursal**: Gestión de varias tiendas
- [ ] **CRM**: Fidelización de clientes
- [ ] **BI**: Business Intelligence avanzado
- [ ] **API Pública**: Para integraciones de terceros

---

## 📅 Cronograma Resumido

| Fase | Duración | Entregables Principales |
|------|----------|------------------------|
| **Fase 1** | 4 semanas | Núcleo POS funcional, productos, ventas básicas |
| **Fase 2** | 4 semanas | Caja, descuentos, proveedores, reportes |
| **Fase 3** | 4 semanas | Optimización, testing, despliegue |
| **Total MVP** | **12 semanas** | **Sistema POS listo para producción** |

---

## 👥 Equipo Recomendado

- **1 Backend Developer**: FastAPI, SQLModel, PostgreSQL
- **1 Frontend Developer**: React, TypeScript, Tailwind CSS
- **1 Full Stack/QA**: Testing, deployment, documentación
- **1 Product Owner**: Definición de requisitos, validación

*Nota: En equipos pequeños, 2 desarrolladores full-stack pueden cubrir el proyecto en el timeline estimado.*

---

## 💰 Estimación de Costos (Infraestructura)

### Mensual (Cloud)
- **Servidor VPS**: $20-50 USD/mes (DigitalOcean, Linode, AWS Lightsail)
- **Backup Storage**: $5-10 USD/mes
- **Dominio**: $15 USD/año
- **SSL Certificate**: Gratis (Let's Encrypt)
- **Total estimado**: **$30-65 USD/mes**

### On-Premise (Inicial)
- **Hardware servidor**: $500-1000 USD (una vez)
- **Mantenimiento**: Electricidad + actualizaciones
- **Total estimado**: **$600-1200 USD inicial**

---

## ✅ Criterios de Aceptación (MVP)

El sistema se considera listo para producción cuando:

1. ✅ Puede registrar una venta completa en menos de 30 segundos
2. ✅ El inventario se actualiza automáticamente tras cada venta
3. ✅ Genera tickets imprimibles correctamente
4. ✅ Soporta al menos 3 métodos de pago
5. ✅ Tiene control de apertura/cierre de caja
6. ✅ Los reportes básicos son precisos
7. ✅ Todos los tests automatizados pasan (cobertura >80%)
8. ✅ Documentación de usuario completada
9. ✅ Backup automático configurado
10. ✅ SSL/HTTPS activo en producción

---

## 📞 Soporte y Mantenimiento

### Post-Implementación
- **Garantía**: 30 días de soporte gratuito post-go-live
- **Mantenimiento**: Contrato mensual opcional ($200-500 USD/mes)
- **Actualizaciones**: Trimestrales (features + security patches)
- **Soporte Prioritario**: SLA de 4 horas para incidencias críticas

---

**Documento creado**: 2026-06-29  
**Versión**: 1.0  
**Estado**: Planificación  

---

*Este plan es flexible y puede ajustarse según los requisitos específicos del cliente y la disponibilidad del equipo.*

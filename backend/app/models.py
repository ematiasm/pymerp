import uuid
from datetime import UTC, datetime

from pydantic import EmailStr
from sqlalchemy import DateTime
from sqlmodel import Field, Relationship, SQLModel


def get_datetime_utc() -> datetime:
    return datetime.now(UTC)


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(SQLModel):
    email: EmailStr | None = Field(default=None, max_length=255)
    is_active: bool | None = None
    is_superuser: bool | None = None
    full_name: str | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)
    # Relaciones POS
    sales: list["Sale"] = Relationship(back_populates="cashier")
    cash_registers: list["CashRegister"] = Relationship(back_populates="cashier")


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID
    created_at: datetime | None = None


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime | None = None


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)


# ==================== MODELOS PARA PUNTO DE VENTA (POS) ====================


# ==================== CATEGORY ====================
class CategoryBase(SQLModel):
    name: str = Field(min_length=1, max_length=100, description="Nombre de la categoría")
    description: str | None = Field(default=None, max_length=255, description="Descripción opcional")
    is_active: bool = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=255)
    is_active: bool | None = None


class Category(CategoryBase, table=True):
    __tablename__ = "category"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    # Relación con productos
    products: list["Product"] = Relationship(back_populates="category", cascade_delete=True)


class CategoryPublic(CategoryBase):
    id: uuid.UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None


class CategoriesPublic(SQLModel):
    data: list[CategoryPublic]
    count: int


# ==================== PRODUCT ====================
class ProductBase(SQLModel):
    name: str = Field(min_length=1, max_length=255, description="Nombre del producto")
    description: str | None = Field(default=None, max_length=500, description="Descripción del producto")
    barcode: str | None = Field(default=None, max_length=100, unique=True, index=True, description="Código de barras")
    sku: str | None = Field(default=None, max_length=100, unique=True, index=True, description="SKU interno")
    price: float = Field(ge=0, decimal_places=2, description="Precio de venta")
    cost: float | None = Field(default=None, ge=0, decimal_places=2, description="Costo de compra")
    stock: int = Field(default=0, ge=0, description="Cantidad en inventario")
    min_stock: int = Field(default=0, ge=0, description="Stock mínimo para alerta")
    max_stock: int | None = Field(default=None, ge=0, description="Stock máximo opcional")
    is_active: bool = True
    is_taxable: bool = True  # Si aplica impuestos
    tax_rate: float | None = Field(default=None, ge=0, le=100, decimal_places=2, description="Porcentaje de impuesto")
    allow_sale_without_stock: bool = False  # Permitir vender sin stock


class ProductCreate(ProductBase):
    category_id: uuid.UUID | None = Field(default=None, foreign_key="category.id", description="ID de categoría")


class ProductUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=500)
    barcode: str | None = Field(default=None, max_length=100)
    sku: str | None = Field(default=None, max_length=100)
    price: float | None = Field(default=None, ge=0, decimal_places=2)
    cost: float | None = Field(default=None, ge=0, decimal_places=2)
    stock: int | None = Field(default=None, ge=0)
    min_stock: int | None = Field(default=None, ge=0)
    max_stock: int | None = Field(default=None, ge=0)
    is_active: bool | None = None
    is_taxable: bool | None = None
    tax_rate: float | None = Field(default=None, ge=0, le=100, decimal_places=2)
    allow_sale_without_stock: bool | None = None
    category_id: uuid.UUID | None = Field(default=None, foreign_key="category.id")


class Product(ProductBase, table=True):
    __tablename__ = "product"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    # Relaciones
    category_id: uuid.UUID | None = Field(default=None, foreign_key="category.id", ondelete="SET NULL")
    category: Category | None = Relationship(back_populates="products")
    sale_items: list["SaleItem"] = Relationship(back_populates="product", cascade_delete=True)


class ProductPublic(ProductBase):
    id: uuid.UUID
    category_id: uuid.UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class ProductsPublic(SQLModel):
    data: list[ProductPublic]
    count: int


# ==================== CUSTOMER ====================
class CustomerBase(SQLModel):
    name: str = Field(min_length=1, max_length=255, description="Nombre completo o razón social")
    email: EmailStr | None = Field(default=None, max_length=255, description="Correo electrónico")
    phone: str | None = Field(default=None, max_length=50, description="Teléfono")
    document_type: str | None = Field(default=None, max_length=50, description="Tipo de documento (DNI, RUC, etc.)")
    document_number: str | None = Field(default=None, max_length=50, description="Número de documento")
    address: str | None = Field(default=None, max_length=500, description="Dirección")
    notes: str | None = Field(default=None, max_length=1000, description="Notas adicionales")
    is_active: bool = True


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=50)
    document_type: str | None = Field(default=None, max_length=50)
    document_number: str | None = Field(default=None, max_length=50)
    address: str | None = Field(default=None, max_length=500)
    notes: str | None = Field(default=None, max_length=1000)
    is_active: bool | None = None


class Customer(CustomerBase, table=True):
    __tablename__ = "customer"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    # Relaciones
    sales: list["Sale"] = Relationship(back_populates="customer", cascade_delete=True)


class CustomerPublic(CustomerBase):
    id: uuid.UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None


class CustomersPublic(SQLModel):
    data: list[CustomerPublic]
    count: int


# ==================== SALE (VENTA) ====================
class SaleStatus(str):
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class PaymentMethod(str):
    CASH = "cash"
    CARD = "card"
    TRANSFER = "transfer"
    OTHER = "other"


class SaleBase(SQLModel):
    invoice_number: str | None = Field(default=None, max_length=100, unique=True, index=True, description="Número de factura/ticket")
    subtotal: float = Field(ge=0, decimal_places=2, description="Subtotal antes de impuestos")
    discount: float = Field(default=0, ge=0, decimal_places=2, description="Descuento aplicado")
    tax_amount: float = Field(default=0, ge=0, decimal_places=2, description="Monto de impuestos")
    total: float = Field(ge=0, decimal_places=2, description="Total final")
    payment_method: PaymentMethod = Field(default=PaymentMethod.CASH, description="Método de pago")
    amount_paid: float = Field(ge=0, decimal_places=2, description="Monto pagado por el cliente")
    change_amount: float = Field(default=0, ge=0, decimal_places=2, description="Cambio/devolución")
    notes: str | None = Field(default=None, max_length=1000, description="Notas de la venta")
    status: SaleStatus = Field(default=SaleStatus.COMPLETED, description="Estado de la venta")
    model_config = {"arbitrary_types_allowed": True}


class SaleCreate(SaleBase):
    customer_id: uuid.UUID | None = Field(default=None, foreign_key="customer.id", description="ID del cliente")
    cashier_id: uuid.UUID = Field(foreign_key="user.id", description="ID del cajero/vendedor")


class SaleUpdate(SQLModel):
    invoice_number: str | None = Field(default=None, max_length=100)
    subtotal: float | None = Field(default=None, ge=0, decimal_places=2)
    discount: float | None = Field(default=None, ge=0, decimal_places=2)
    tax_amount: float | None = Field(default=None, ge=0, decimal_places=2)
    total: float | None = Field(default=None, ge=0, decimal_places=2)
    payment_method: PaymentMethod | None = None
    amount_paid: float | None = Field(default=None, ge=0, decimal_places=2)
    change_amount: float | None = Field(default=None, ge=0, decimal_places=2)
    notes: str | None = Field(default=None, max_length=1000)
    status: SaleStatus | None = None
    customer_id: uuid.UUID | None = Field(default=None, foreign_key="customer.id")
    model_config = {"arbitrary_types_allowed": True}


class Sale(SaleBase, table=True):
    __tablename__ = "sale"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    # Relaciones
    customer_id: uuid.UUID | None = Field(default=None, foreign_key="customer.id", ondelete="SET NULL")
    customer: Customer | None = Relationship(back_populates="sales")
    cashier_id: uuid.UUID = Field(foreign_key="user.id", ondelete="RESTRICT")
    cashier: User | None = Relationship(back_populates="sales")
    items: list["SaleItem"] = Relationship(back_populates="sale", cascade_delete=True)


class SalePublic(SaleBase):
    id: uuid.UUID
    customer_id: uuid.UUID | None = None
    cashier_id: uuid.UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None


class SalesPublic(SQLModel):
    data: list[SalePublic]
    count: int


# ==================== SALE ITEM (ÍTEM DE VENTA) ====================
class SaleItemBase(SQLModel):
    quantity: int = Field(gt=0, description="Cantidad vendida")
    unit_price: float = Field(ge=0, decimal_places=2, description="Precio unitario al momento de la venta")
    discount: float = Field(default=0, ge=0, decimal_places=2, description="Descuento aplicado al ítem")
    tax_rate: float | None = Field(default=None, ge=0, le=100, decimal_places=2, description="Impuesto aplicado")
    tax_amount: float = Field(default=0, ge=0, decimal_places=2, description="Monto de impuesto del ítem")
    subtotal: float = Field(ge=0, decimal_places=2, description="Subtotal del ítem (cantidad * precio - descuento)")
    total: float = Field(ge=0, decimal_places=2, description="Total del ítem (subtotal + impuesto)")


class SaleItemCreate(SaleItemBase):
    product_id: uuid.UUID = Field(foreign_key="product.id", description="ID del producto")
    sale_id: uuid.UUID = Field(foreign_key="sale.id", description="ID de la venta")


class SaleItemUpdate(SQLModel):
    quantity: int | None = Field(default=None, gt=0)
    unit_price: float | None = Field(default=None, ge=0, decimal_places=2)
    discount: float | None = Field(default=None, ge=0, decimal_places=2)
    tax_rate: float | None = Field(default=None, ge=0, le=100, decimal_places=2)
    tax_amount: float | None = Field(default=None, ge=0, decimal_places=2)
    subtotal: float | None = Field(default=None, ge=0, decimal_places=2)
    total: float | None = Field(default=None, ge=0, decimal_places=2)


class SaleItem(SaleItemBase, table=True):
    __tablename__ = "sale_item"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    # Relaciones
    product_id: uuid.UUID = Field(foreign_key="product.id", ondelete="RESTRICT")
    product: Product | None = Relationship(back_populates="sale_items")
    sale_id: uuid.UUID = Field(foreign_key="sale.id", ondelete="CASCADE")
    sale: Sale | None = Relationship(back_populates="items")


class SaleItemPublic(SaleItemBase):
    id: uuid.UUID
    product_id: uuid.UUID
    sale_id: uuid.UUID
    product_name: str | None = None  # Nombre del producto al momento de la venta (snapshot)


# ==================== SUPPLIER (PROVEEDOR) - PREPARACIÓN FASE 2 ====================
class SupplierBase(SQLModel):
    name: str = Field(min_length=1, max_length=255, description="Nombre del proveedor")
    contact_name: str | None = Field(default=None, max_length=255, description="Nombre de contacto")
    email: EmailStr | None = Field(default=None, max_length=255, description="Correo electrónico")
    phone: str | None = Field(default=None, max_length=50, description="Teléfono")
    address: str | None = Field(default=None, max_length=500, description="Dirección")
    document_type: str | None = Field(default=None, max_length=50, description="Tipo de documento")
    document_number: str | None = Field(default=None, max_length=50, description="Número de documento")
    notes: str | None = Field(default=None, max_length=1000, description="Notas")
    is_active: bool = True


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    contact_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=50)
    address: str | None = Field(default=None, max_length=500)
    document_type: str | None = Field(default=None, max_length=50)
    document_number: str | None = Field(default=None, max_length=50)
    notes: str | None = Field(default=None, max_length=1000)
    is_active: bool | None = None


class Supplier(SupplierBase, table=True):
    __tablename__ = "supplier"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
    )


class SupplierPublic(SupplierBase):
    id: uuid.UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None


class SuppliersPublic(SQLModel):
    data: list[SupplierPublic]
    count: int


# ==================== CASH REGISTER (CAJA/TURNOS) - PREPARACIÓN FASE 2 ====================
class CashRegisterStatus(str):
    OPEN = "open"
    CLOSED = "closed"
    SUSPENDED = "suspended"


class CashRegisterBase(SQLModel):
    opening_balance: float = Field(default=0, ge=0, decimal_places=2, description="Saldo inicial de caja")
    closing_balance: float | None = Field(default=None, ge=0, decimal_places=2, description="Saldo final de caja")
    opening_notes: str | None = Field(default=None, max_length=500, description="Notas de apertura")
    closing_notes: str | None = Field(default=None, max_length=500, description="Notas de cierre")
    status: CashRegisterStatus = Field(default=CashRegisterStatus.OPEN, description="Estado de la caja")
    model_config = {"arbitrary_types_allowed": True}


class CashRegisterCreate(CashRegisterBase):
    cashier_id: uuid.UUID = Field(foreign_key="user.id", description="ID del cajero responsable")


class CashRegisterUpdate(SQLModel):
    closing_balance: float | None = Field(default=None, ge=0, decimal_places=2)
    closing_notes: str | None = Field(default=None, max_length=500)
    status: CashRegisterStatus | None = None
    model_config = {"arbitrary_types_allowed": True}


class CashRegister(CashRegisterBase, table=True):
    __tablename__ = "cash_register"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    opened_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    closed_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    # Relaciones
    cashier_id: uuid.UUID = Field(foreign_key="user.id", ondelete="RESTRICT")
    cashier: User | None = Relationship(back_populates="cash_registers")


class CashRegisterPublic(CashRegisterBase):
    id: uuid.UUID
    cashier_id: uuid.UUID
    opened_at: datetime | None = None
    closed_at: datetime | None = None


class CashRegistersPublic(SQLModel):
    data: list[CashRegisterPublic]
    count: int


# ==================== ACTUALIZAR MODELO USER CON NUEVAS RELACIONES ====================
# Las relaciones ya están definidas en la clase User (líneas 61-62)
# No es necesario agregarlas aquí nuevamente

from datetime import datetime
from enum import Enum

from sqlalchemy import (
    BigInteger,
    Column,
    Date,
    DateTime,
    DECIMAL,
    Enum as SAEnum,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from backend.app.db.database import Base


class UserSource(str, Enum):
    portal = "portal"
    backend = "backend"


class AdminUser(Base):
    __tablename__ = "admin_user"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    status = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class User(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    mobile = Column(String(20), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    nickname = Column(String(64))
    source = Column(SAEnum(UserSource), nullable=False, default=UserSource.portal)
    register_ip = Column(String(64))
    registered_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_login_at = Column(DateTime)
    balance = Column(DECIMAL(12, 2), default=0, nullable=False)
    real_name = Column(String(64))
    status = Column(Integer, default=1, nullable=False)


class UserAddress(Base):
    __tablename__ = "user_address"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("user.id"), nullable=False)
    receiver_name = Column(String(64), nullable=False)
    mobile = Column(String(20), nullable=False)
    province = Column(String(64))
    city = Column(String(64))
    district = Column(String(64))
    detail_addr = Column(String(255))
    is_default = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    user = relationship("User")


class ProductCategory(Base):
    __tablename__ = "product_category"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Product(Base):
    __tablename__ = "product"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    category_id = Column(BigInteger, ForeignKey("product_category.id"), nullable=False)
    price = Column(DECIMAL(12, 2), nullable=False)
    init_stock = Column(Integer, nullable=False)
    stock = Column(Integer, nullable=False)
    zodiac_flags = Column(String(64))
    is_home_show = Column(Integer, default=0, nullable=False)
    home_section = Column(String(32))
    main_image = Column(String(255))
    description_html = Column(Text)
    status = Column(String(8), default="on", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    category = relationship("ProductCategory")


class ProductOrder(Base):
    __tablename__ = "product_order"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    order_no = Column(String(64), unique=True, nullable=False)
    user_id = Column(BigInteger, ForeignKey("user.id"), nullable=False)
    address_id = Column(BigInteger, ForeignKey("user_address.id"), nullable=False)
    amount_product = Column(DECIMAL(12, 2), nullable=False)
    amount_shipping = Column(DECIMAL(12, 2), default=0, nullable=False)
    amount_total = Column(DECIMAL(12, 2), nullable=False)
    pay_status = Column(String(16), default="unpaid", nullable=False)
    ship_status = Column(String(16), default="unshipped", nullable=False)
    pay_method = Column(String(16), nullable=False)
    pay_time = Column(DateTime)
    ship_time = Column(DateTime)
    receive_time = Column(DateTime)
    express_company = Column(String(64))
    tracking_no = Column(String(64))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    user = relationship("User")
    address = relationship("UserAddress")
    items = relationship("ProductOrderItem", back_populates="order")


class ProductOrderItem(Base):
    __tablename__ = "product_order_item"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    order_id = Column(BigInteger, ForeignKey("product_order.id"), nullable=False)
    product_id = Column(BigInteger, ForeignKey("product.id"), nullable=False)
    product_name = Column(String(128), nullable=False)
    category_name = Column(String(64))
    price = Column(DECIMAL(12, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
    amount = Column(DECIMAL(12, 2), nullable=False)

    order = relationship("ProductOrder", back_populates="items")
    product = relationship("Product")


class BlessItem(Base):
    __tablename__ = "bless_item"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    price_coin = Column(Integer, nullable=False)
    status = Column(String(8), default="on", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class BlessOrder(Base):
    __tablename__ = "bless_order"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    order_no = Column(String(64), unique=True, nullable=False)
    user_id = Column(BigInteger, ForeignKey("user.id"), nullable=False)
    bless_item_id = Column(BigInteger, ForeignKey("bless_item.id"), nullable=False)
    item_name = Column(String(64), nullable=False)
    price_coin = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    total_coin = Column(Integer, nullable=False)
    rmb_amount = Column(DECIMAL(12, 2), nullable=False)
    rate_at_order = Column(DECIMAL(12, 4), nullable=False)
    pay_status = Column(String(16), default="unpaid", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    paid_at = Column(DateTime)



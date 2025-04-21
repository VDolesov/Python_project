from datetime import datetime, date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DECIMAL, String, Integer, Date
from project.infrastructure.postgres.database import Base


class Client(Base):
    __tablename__ = "clients"

    client_id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(nullable=True)

    bookings = relationship("Booking", back_populates="client")


class Hotel(Base):
    __tablename__ = "hotels"

    hotel_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[str] = mapped_column(String(200), nullable=True)

    room_types = relationship("RoomType", back_populates="hotel")
    rooms = relationship("Room", back_populates="hotel")
    bookings = relationship("Booking", back_populates="hotel")
    feedbacks = relationship("Feedback", back_populates="hotel")


class RoomType(Base):
    __tablename__ = "room_types"

    room_type_id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.hotel_id"), nullable=False)
    room_number: Mapped[str] = mapped_column(String(20), nullable=False)
    room_type: Mapped[str] = mapped_column(String(50), nullable=False)
    price_per_night: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    capacity: Mapped[int] = mapped_column(nullable=False)

    hotel = relationship("Hotel", back_populates="room_types")

    rooms = relationship("Room", back_populates="room_type")


class Room(Base):
    __tablename__ = "rooms"

    room_id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.hotel_id"), nullable=False)
    room_type_id: Mapped[int] = mapped_column(ForeignKey("room_types.room_type_id"), nullable=False)
    room_number: Mapped[str] = mapped_column(String(20), nullable=False)
    price_per_night: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    capacity: Mapped[int] = mapped_column(nullable=False)

    hotel = relationship("Hotel", back_populates="rooms")
    room_type = relationship("RoomType", back_populates="rooms")


class Booking(Base):
    __tablename__ = "bookings"

    booking_id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.client_id"), nullable=False)
    room_type_id: Mapped[int] = mapped_column(ForeignKey("room_types.room_type_id"), nullable=False)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.hotel_id"), nullable=False)
    booking_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    check_in_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    check_out_date: Mapped[datetime] = mapped_column(Date, nullable=False)

    client = relationship("Client", back_populates="bookings")
    room_type = relationship("RoomType")
    hotel = relationship("Hotel", back_populates="bookings")


class PaymentType(Base):
    __tablename__ = "payment_types"

    type_payment_id: Mapped[int] = mapped_column(primary_key=True)
    name_payment: Mapped[str] = mapped_column(String(50), nullable=False)


class Stay(Base):
    __tablename__ = "stays"

    stay_id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.room_id"), nullable=False)
    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.booking_id"), nullable=False)
    payment: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    check_in_date: Mapped[Date] = mapped_column(Date, nullable=False)
    check_out_date: Mapped[Date] = mapped_column(Date, nullable=False)
    type_payment_id: Mapped[int] = mapped_column(ForeignKey("payment_types.type_payment_id"), nullable=False)
    total_price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)

    room = relationship("Room")
    booking = relationship("Booking")
    payment_type = relationship("PaymentType")


class Service(Base):
    __tablename__ = "services"

    service_id: Mapped[int] = mapped_column(primary_key=True)
    service_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)


class ServiceUsage(Base):
    __tablename__ = "service_usage"

    service_usage_id: Mapped[int] = mapped_column(primary_key=True)
    stay_id: Mapped[int] = mapped_column(ForeignKey("stays.stay_id"), nullable=False)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.service_id"), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    total_price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)

    stay = relationship("Stay")
    service = relationship("Service")


class Feedback(Base):
    __tablename__ = "feedback"

    feedback_id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.hotel_id"), nullable=False)
    stay_id: Mapped[int] = mapped_column(ForeignKey("stays.stay_id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[str] = mapped_column(String(200), nullable=False)

    hotel = relationship("Hotel", back_populates="feedbacks")
    stay = relationship("Stay")

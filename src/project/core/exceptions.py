class ClientAlreadyExists(Exception):
    def __init__(self, message="Client already exists"):
        self.message = message
        super().__init__(self.message)


class ClientNotFound(Exception):
    def __init__(self, message="Client not found"):
        self.message = message
        super().__init__(self.message)


class HotelAlreadyExists(Exception):
    def __init__(self, message="Hotel already exists"):
        self.message = message
        super().__init__(self.message)


class HotelNotFound(Exception):
    def __init__(self, message="Hotel not found"):
        self.message = message
        super().__init__(self.message)


class RoomAlreadyExists(Exception):
    def __init__(self, message="Room already exists"):
        self.message = message
        super().__init__(self.message)

class RoomCapacity(Exception):
    def __init__(self, message="capacity < 0"):
        self.message = message
        super().__init__(self.message)

class RoomPerPrice(Exception):
    def __init__(self, message="price per night < 0"):
        self.message = message
        super().__init__(self.message)


class RoomNotFound(Exception):
    def __init__(self, message="Room not found"):
        self.message = message
        super().__init__(self.message)

class RoomTypeAlreadyExists(Exception):
    def __init__(self, message="Room type already exists"):
        self.message = message
        super().__init__(self.message)


class RoomTypeNotFound(Exception):
    def __init__(self, message="Room type not found"):
        self.message = message
        super().__init__(self.message)


class ServiceAlreadyExists(Exception):
    def __init__(self, message="Service already exists"):
        self.message = message
        super().__init__(self.message)


class ServiceNotFound(Exception):
    def __init__(self, message="Service not found"):
        self.message = message
        super().__init__(self.message)

class BookingNotFound(Exception):
    def __init__(self, message="Booking not found"):
        self.message = message
        super().__init__(self.message)


class BookingAlreadyExists(Exception):
    def __init__(self, message="Booking already exists"):
        self.message = message
        super().__init__(self.message)


class StayNotFound(Exception):
    def __init__(self, message="Stay not found"):
        self.message = message
        super().__init__(self.message)


class StayAlreadyExists(Exception):
    def __init__(self, message="Stay already exists"):
        self.message = message
        super().__init__(self.message)


class ServiceUsageNotFound(Exception):
    def __init__(self, message="Service usage not found"):
        self.message = message
        super().__init__(self.message)


class ServiceUsageAlreadyExists(Exception):
    def __init__(self, message="Service usage already exists"):
        self.message = message
        super().__init__(self.message)

class FeedbackNotFound(Exception):
    def __init__(self, message="Feedback not found"):
        self.message = message
        super().__init__(self.message)


class FeedbackAlreadyExists(Exception):
    def __init__(self, message="Feedback already exists"):
        self.message = message
        super().__init__(self.message)

class PaymentTypeNotFound(Exception):
    def __init__(self, message="Payment type not found"):
        self.message = message
        super().__init__(self.message)


class PaymentTypeAlreadyExists(Exception):
    def __init__(self, message="Payment type already exists"):
        self.message = message
        super().__init__(self.message)

class InvalidStayDates(Exception):
    def __init__(self, message="Invalid stay dates: check-in date must be earlier than check-out date"):
        self.message = message
        super().__init__(self.message)

class RoomNotFoundInStays(Exception):
    def __init__(self, message="Room ID does not exist in rooms table"):
        self.message = message
        super().__init__(self.message)

class InvalidPaymentAmount(Exception):
    def __init__(self, message="Invalid payment amount: payment must be greater than or equal to 0"):
        self.message = message
        super().__init__(self.message)

class InvalidServicePrice(Exception):
    def __init__(self, message="Invalid service price: price must be greater than 0"):
        self.message = message
        super().__init__(self.message)

class ForeignKeyConstraintViolation(Exception):
    def __init__(self, message="Foreign key constraint violation: referenced record not found"):
        self.message = message
        super().__init__(self.message)


class InvalidQuantity(Exception):
    def __init__(self, message="Quantity must be greater than 0"):
        self.message = message
        super().__init__(self.message)


class InvalidTotalPrice(Exception):
    def __init__(self, message="Total price must be greater than or equal to 0"):
        self.message = message
        super().__init__(self.message)

class StayNotFound(Exception):
    def __init__(self, message="Stay not found"):
        self.message = message
        super().__init__(self.message)
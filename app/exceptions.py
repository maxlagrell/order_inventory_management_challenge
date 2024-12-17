class ProductNotFoundError(Exception):
    message = "Product not found"

class InvalidUUIDFormatError(Exception):
    message = "Invalid UUID format"

class InvalidInputError(Exception):
    message = "Invalid input"

class InsufficientInventoryError(Exception):
    message = "Insufficient inventory"

class OrderNotFoundError(Exception):
    message = "Order not found"

class UserNotFoundError(Exception):
    message = "User not found"

class InvalidContentTypeError(Exception):
    message = "Content type must be application/json"

class InvalidJSONError(Exception):
    message = "Invalid JSON"





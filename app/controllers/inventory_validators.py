from uuid import UUID
from sanic import response
from app.services.inventory_service import InventoryService
from app.exceptions import InvalidInputError, InvalidUUIDFormatError, ProductNotFoundError, InvalidContentTypeError, InvalidJSONError


def validate_product_id(product_id: str):
    try:
        UUID(product_id)
    except ValueError as e:
        raise InvalidUUIDFormatError
  
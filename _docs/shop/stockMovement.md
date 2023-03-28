# Model

The StockMovement model represents a movement of a product's stock in a deposit.

## Fields

`deposit`: a ForeignKey to the Deposit model that represents the deposit where the product is stored.

`product`: a ForeignKey to the Product model that represents the product.

`value`: a DecimalField that stores the value of the stock movement.

`amount`: a DecimalField that stores the quantity of the stock movement.

`movementType`: a CharField that stores the type of movement. The field has two possible values: "IN" for input and "OUT" for output.

`createdAt`: a DateTimeField that stores the date and time when the stock movement was created. The value is automatically set when a new stock movement is created.

`updatedAt`: a DateTimeField that stores the date and time when the stock movement was last updated. The value is automatically updated every time a stock movement is saved.

`deletedAt`: a DateTimeField that stores the date and time when the stock movement was deleted. If the stock movement has not been deleted, this field is null.

## Methods

`delete()`: a method that marks the stock movement as deleted by setting the deletedAt field to the current date and time. The method also logs the deletion of the stock movement.

# Viewset

The StockMovementViewSets viewset implements read-only operations for the StockMovement model.

## Endpoints

The following endpoints are available for the StockMovementViewSets viewset:

| Method | URL | Description |
|--------|-----|-------------|
| GET | /api/stockmovement/ | Lists all active instances of StockMovement. |
| GET | /api/stockmovement/{id}/ | Retrieves a specific instance of StockMovement by ID. |

## Parameters

The following parameters are available for the StockMovementViewSets viewset:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| deposit_id | integer | no | Filters instances by deposit ID. |
| product_id | integer | no | Filters instances by product ID. | 
| movementType | string | no | Filters instances by movement type (IN or OUT). |

## Response

The responses for the StockMovementViewSets viewset are in JSON format.

## Permissions

The StockMovementViewSets viewset uses the DjangoModelPermissions permission, which ensures that only authenticated and authorized users can access the operations.
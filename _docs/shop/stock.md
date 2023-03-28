# Model

The Stock model is a Django class that represents a stock of products in a particular deposit. Each instance of Stock contains the following information:

`deposit`: a foreign key that points to the deposit where the stock is kept.

`product`: a foreign key that points to the product held in the stock.

`value`: a DecimalField that stores the value of the product in the stock.

`amount`: a DecimalField that stores the amount of the product in the stock.

`createdAt`: a DateTimeField that stores the date and time when the stock was created. The value is automatically set when a new stock is created.

`updatedAt`: a DateTimeField that stores the date and time when the stock was last updated. The value is automatically updated every time a stock is saved.

`deletedAt`: a DateTimeField that stores the date and time when the stock was deleted. If the stock has not been deleted, this field is null.

## Methods

`isValid()`: a method that checks whether the stock is valid or not. If the deletedAt field is not null, the stock is considered invalid.

`total()`: a method that returns the total value of the stock.

`delete()`: a method that marks the stock as deleted by setting the deletedAt field to the current date and time. Before a stock can be deleted, the method checks if the stock amount is not zero. If the stock amount is greater than zero, the method raises a ValidationError.

`close()`: a method that marks the stock as deleted by calling the delete() method.

`open()`: a method that restores the stock by setting the deletedAt field to null.

# Viewset

The StockViewset is a Django Rest Framework class that provides CRUD (Create, Read, Update, and Delete) operations for the Stock model. The viewset uses the StockSerializer serializer and the DjangoModelPermissions permission, which ensures that only authenticated and authorized users can access the operations.

## Parameters

The following parameters are available for the StockViewset:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| deposit_id | integer | no | Filters instances by deposit ID. |
| product_id | integer | no | Filters instances by product ID. |

## Endpoints

The following endpoints are available for the StockViewset:

| Method | URL | Description |
|--------|-----|-------------|
| POST | /api/stock/ | Creates a new instance of Stock. |
| GET | /api/stock/ | Lists all active instances of Stock. |
| GET | /api/stock/{id}/ | Retrieves a specific instance of Stock by ID. |
| PUT | /api/stock/{id}/ | Updates a specific instance of Stock. |
| PATCH | /api/stock/{id}/ | Partially updates a specific instance of Stock. |
| DELETE | /api/stock/{id}/ | Marks a specific instance of Stock as deleted. |

## Response

The responses for the StockViewset are in JSON format.

## Permissions

The StockViewset uses the DjangoModelPermissions permission, which ensures that only authenticated and authorized users can access the operations.
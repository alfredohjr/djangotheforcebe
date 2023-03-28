# Model

The Product model represents a product in the system.

## Fields

`name`: a CharField that stores the name of the product. The maximum length of the name is 30 characters.

`margin`: a DecimalField that stores the margin of the product as a decimal number with up to 5 digits before the decimal point and 3 digits after it. The default value is 0.

`createdAt`: a DateTimeField that stores the date and time when the product was created. The value is automatically set when a new product is created.

`updatedAt`: a DateTimeField that stores the date and time when the product was last updated. The value is automatically updated every time a product is saved.

`deletedAt`: a DateTimeField that stores the date and time when the product was deleted. If the product has not been deleted, this field is null.

## Methods

`delete()`: a method that marks the product as deleted by setting the deletedAt field to the current date and time. Before a product can be deleted, the method checks if the product is in stock or if there is an open related document. If any of these conditions are met, the method raises a ValidationError.

`close()`: a method that marks the product as deleted by calling the delete() method.

`open()`: a method that restores the product by setting the deletedAt field to null.

`marginValue()`: a property that returns the margin value formatted as a percentage.

# Viewset

The ProductViewset viewset provides CRUD (Create, Read, Update, and Delete) operations for the Product model.

## Methods

`create`: creates a new instance of Product.

`list`: lists all active instances of Product.

`retrieve`: retrieves a specific instance of Product by ID.

`update`: updates a specific instance of Product.

`partial_update`: partially updates a specific instance of Product.

`destroy`: marks a specific instance of Product as deleted.

The class uses the ProductSerializer serializer and the DjangoModelPermissions permission, which ensures that only authenticated and authorized users can access the operations.

The class also has a get_queryset() method that returns all active instances of Product, filtered by name (if there are any filter parameters in the query string).

## Endpoints

The following endpoints are available for the ProductViewset viewset:

| Method | URL | Description |
|--------|-----|-------------|
| POST   | /api/product/ | Creates a new instance of Product. |
| GET    | /api/product/ | Lists all active instances of Product. |
| GET    | /api/product/{id}/ | Retrieves a specific instance of Product by ID. |
| PUT    | /api/product/{id}/ | Updates a specific instance of Product. |
| PATCH  | /api/product/{id}/ | Partially updates a specific instance of Product. |
| DELETE | /api/product/{id}/ | Marks a specific instance of Product as deleted. |

## Parameters

The following parameters are available for the ProductViewset viewset:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name      | string | no     | Filters instances by name. |

## Response

The responses for the ProductViewset viewset are in JSON format.

## Permissions

The ProductViewset viewset uses the DjangoModelPermissions permission, which ensures that only authenticated and authorized users can access the operations.
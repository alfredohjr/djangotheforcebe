# Model

The Deposit model represents a deposit in the system.

## Fields

`name`: a CharField that stores the name of the deposit. The maximum length of the name is 30 characters.

`company`: a ForeignKey that references the Company model, representing the company that owns the deposit.

`createdAt`: a DateTimeField that stores the date and time when the deposit was created. The value is automatically set when a new deposit is created.

`updatedAt`: a DateTimeField that stores the date and time when the deposit was last updated. The value is automatically updated every time a deposit is saved.

`deletedAt`: a DateTimeField that stores the date and time when the deposit was deleted. If the deposit has not been deleted, this field is null.

## Methods

`delete()`: a method that marks the deposit as deleted by setting the deletedAt field to the current date and time. Before a deposit can be deleted, the method checks if the product stock is not zero. If any of these conditions are met, the method raises a ValidationError.

`close()`: a method that marks the deposit as deleted by calling the delete() method.

`open()`: a method that restores the deposit by setting the deletedAt field to null.

`total()`: a method that calculates the total value of the deposit. The method sums the value of all product stocks associated with the deposit and returns the result as a formatted string with a dollar sign.

`totalAmount()`: a method that calculates the total amount of the deposit. The method sums the amount of all product stocks associated with the deposit and returns the result as a formatted string.


# Viewset

The DepositViewset viewset provides CRUD (Create, Read, Update, and Delete) operations for the Deposit model.

## Methods

`create`: creates a new instance of Deposit.

`list`: lists all active instances of Deposit.

`retrieve`: retrieves a specific instance of Deposit by ID.

`update`: updates a specific instance of Deposit.

`partial_update`: partially updates a specific instance of Deposit.

`destroy`: marks a specific instance of Deposit as deleted.

The DepositViewset viewset uses the DepositSerializer serializer and the DjangoModelPermissions permission, which ensures that only authenticated and authorized users can access the operations.

The viewset also has a get_queryset() method that returns all active instances of Deposit, filtered by name and company ID (if there are any filter parameters in the query string).

## Endpoints

The following endpoints are available for the DepositViewset viewset:

| Method | URL | Description |
|--------|-----|-------------|
|POST    | /api/deposit/ | Creates a new instance of Deposit.|
|GET     | /api/deposit/ | Lists all active instances of Deposit.|
|GET     | /api/deposit/{id}/ | Retrieves a specific instance of Deposit by ID.|
|PUT     | /api/deposit/{id}/ | Updates a specific instance of Deposit.|
|PATCH   | /api/deposit/{id}/ | Partially updates a specific instance of Deposit.|
|DELETE  | /api/deposit/{id}/ | Marks a specific instance of Deposit as deleted.|

## Parameters

The following parameters are available for the DepositViewset viewset:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name      | string | no     | Filters instances by name.|
| company_id | integer | no   | Filters instances by company ID.|

## Response

The responses for the DepositViewset viewset are in JSON format.

## Permissions

The DepositViewset viewset uses the DjangoModelPermissions permission, which ensures that only authenticated and authorized users can access the operations.
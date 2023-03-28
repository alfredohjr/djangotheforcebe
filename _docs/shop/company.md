# Company model

The Company model represents a company in the system.

## Fields

`name`: a CharField that stores the name of the company. The maximum length of the name is 30 characters.

`createdAt`: a DateTimeField that stores the date and time when the company was created. The value is automatically set when a new company is created.

`updatedAt`: a DateTimeField that stores the date and time when the company was last updated. The value is automatically updated every time a company 
is saved.

`deletedAt`: a DateTimeField that stores the date and time when the company was deleted. If the company has not been deleted, this field is null.

## Methods

`delete()`: a method that marks the company as deleted by setting the deletedAt field to the current date and time. Before a company can be deleted, the method checks if the product stock is not zero and if there are any open documents associated with the company. If any of these conditions are met, the method raises a ValidationError.

`close()`: a method that marks the company as deleted by calling the delete() method.

`open()`: a method that restores the company by setting the deletedAt field to null.


# Viewset

The CompanyViewSets viewset implements CRUD (Create, Read, Update, and Delete) operations for the Company model. The viewset provides the following methods:

`create`: creates a new instance of Company.

`list`: lists all active instances of Company.

`retrieve`: retrieves a specific instance of Company by ID.

`update`: updates a specific instance of Company.

`partial_update`: partially updates a specific instance of Company.

`destroy`: marks a specific instance of Company as deleted.

The CompanyViewSets viewset uses the CompanySerializer serializer and the DjangoModelPermissions permission, which ensures that only authenticated and authorized users can access the operations.

The viewset also has a get_queryset() method that returns all active instances of Company, filtered by name (if there are any filter parameters in the query string).


## Endpoints

The following endpoints are available for the CompanyViewSets viewset:

| Method | URL | Description |
|--------|-----|-------------|
|POST | /api/company/ | Creates a new instance of Company.|
|GET | /api/company/ | Lists all active instances of Company.|
|GET | /api/company/{id}/ |	Retrieves a specific instance of Company by ID.|
|PUT | /api/company/{id}/ |	Updates a specific instance of Company.|
|PATCH | /api/company/{id}/ | Partially updates a specific instance of Company.|
|DELETE | /api/company/{id}/ | Marks a specific instance of Company as deleted.|

## Parameters

The following parameters are available for the CompanyViewSets viewset:

|Parameter | Type | Required | Description |
|----------|------|----------|-------------|
|name      | string | no     | Filters instances by name.|

## Response

The responses for the CompanyViewSets viewset are in JSON format.

## Permissions

The CompanyViewSets viewset uses the DjangoModelPermissions permission, which ensures that only authenticated and authorized users can access the operations.
# Model

The DocumentProduct model represents a product associated with a transaction document, such as an invoice or a receipt.

## Fields

`document`: a ForeignKey that references the Document model and indicates the document associated with the product.

`product`: a ForeignKey that references the Product model and indicates the product associated with the document.

`amount`: a DecimalField that stores the quantity of the product.

`value`: a DecimalField that stores the value of the product.

`isOpen`: a BooleanField that indicates if the document product is open or closed. The default value is True.

`isNew`: a BooleanField that indicates if the document product is new or not. The default value is True.

`createdAt`: a DateTimeField that stores the date and time when the document product was created. The value is automatically set when a new document product is created.

`updatedAt`: a DateTimeField that stores the date and time when the document product was last updated. The value is automatically updated every time a document product is saved.

`deletedAt`: a DateTimeField that stores the date and time when the document product was deleted. If the document product has not been deleted, this field is null.

## Methods

`delete()`: a method that marks the document product as deleted by setting the deletedAt field to the current date and time. The method also logs the deletion of the document product.

`close()`: a method that marks the document product as closed by setting the isOpen field to False.

`open()`: a method that marks the document product as open by setting the isOpen field to True.


# Viewset

The DocumentProductViewset is a Django Rest Framework Viewset that implements CRUD (Create, Read, Update, and Delete) operations for the DocumentProduct model. The Viewset provides the following methods:

`create`: creates a new instance of DocumentProduct.

`list`: lists all active instances of DocumentProduct.

`retrieve`: retrieves a specific instance of DocumentProduct by ID.

`update`: updates a specific instance of DocumentProduct.

`partial_update`: partially updates a specific instance of DocumentProduct.

`destroy`: marks a specific instance of DocumentProduct as deleted.

The DocumentProductViewset uses the DocumentProductSerializer serializer and the DjangoModelPermissions permission, which ensures that only authenticated and authorized users can access the operations.

The Viewset also has a get_queryset() method that returns all active instances of DocumentProduct, filtered by document_id, product_id, isOpen, and isNew (if there are any filter parameters in the query string).

## Endpoints

The following endpoints are available for the DocumentProductViewset:

| Method | URL | Description |
|--------|-----|-------------|
| POST | /api/documentproduct/ | Creates a new instance of DocumentProduct. | 
| GET | /api/documentproduct/ | Lists all active instances of DocumentProduct. | 
| GET | /api/documentproduct/{id}/ | Retrieves a specific instance of DocumentProduct by ID. | 
| PUT | /api/documentproduct/{id}/ | Updates a specific instance of DocumentProduct. | 
| PATCH | /api/documentproduct/{id}/ | Partially updates a specific instance of DocumentProduct. | 
| DELETE | /api/documentproduct/{id}/ | Marks a specific instance of DocumentProduct as deleted. | 

## Parameters

The following parameters are available for the DocumentProductViewset:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| document_id | integer | no | Filters instances by document ID. | 
| product_id | integer | no | Filters instances by product ID. | 
| isOpen | boolean | no | Filters instances by open status (True or False). | 
| isNew | boolean | no | Filters instances by new status (True or False). | 

## Response

The responses for the DocumentProductViewset are in JSON format.

## Permissions

The DocumentProductViewset uses the DjangoModelPermissions permission, which ensures that only authenticated and authorized users can access the operations.
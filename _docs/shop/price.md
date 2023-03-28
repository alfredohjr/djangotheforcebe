# Model

The Price model represents the price of a product at a certain time.

## Fields

`deposit`: a ForeignKey to the Deposit model that represents the deposit where the product is stored.

`product`: a ForeignKey to the Product model that represents the product.

`value`: a DecimalField that stores the price value.

`priceType`: a CharField that stores the price type. The field has two possible values: "OF" (Offer) and "NO" (Normal). The default value is "NO".

`startedAt`: a DateTimeField that stores the date and time when the price became valid.

`finishedAt`: a DateTimeField that stores the date and time when the price expired.

`isValid`: a BooleanField that indicates if the price is currently valid.

`createdAt`: a DateTimeField that stores the date and time when the price was created. The value is automatically set when a new price is created.

`updatedAt`: a DateTimeField that stores the date and time when the price was last updated. The value is automatically updated every time a price is saved.

`deletedAt`: a DateTimeField that stores the date and time when the price was deleted. If the price has not been deleted, this field is null.

## Methods

`delete()`: a method that marks the price as deleted by setting the deletedAt field to the current date and time. The method also logs the deletion of the price.

`close()`: a method that marks the price as deleted by calling the delete() method.

`open()`: a method that restores the price by setting the deletedAt field to null.

`stockBefore()`: a method that returns the stock of the product before the price became valid.

`stockNow()`: a method that returns the current stock of the product.

# Viewset

The PriceViewSets viewset implements CRUD (Create, Read, Update, and Delete) operations for the Price model. The viewset provides the following methods:

`create`: creates a new instance of Price.

`list`: lists all active instances of Price.

`retrieve`: retrieves a specific instance of Price by ID.

`update`: updates a specific instance of Price.

`partial_update`: partially updates a specific instance of Price.

`destroy`: marks a specific instance of Price as deleted.

The PriceViewSets viewset uses the PriceSerializer serializer and the DjangoModelPermissions permission, which ensures that only authenticated and authorized users can access the operations.

The viewset also has a get_queryset() method that returns all active instances of Price, filtered by deposit, product, priceType, and isValid (if there are any filter parameters in the query string).

## Endpoints

The following endpoints are available for the PriceViewSets viewset:

| Method | URL | Description |
|--------|-----|-------------|
|POST	 | /api/price/ | Creates a new instance of Price.|
|GET	 | /api/price/| Lists all active instances of Price.|
|GET	 | /api/price/{id}/| Retrieves a specific instance of Price by ID.|
|PUT	 | /api/price/{id}/| Updates a specific instance of Price.|
|PATCH	 | /api/price/{id}/ | Partially updates a specific instance of Price.|
|DELETE	 | /api/price/{id}/ | Marks a specific instance of Price as deleted.|

## Parameters

The following parameters are available for the PriceViewSets viewset:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
|deposit_id	| integer | no | Filters instances by deposit ID.|
|product_id	| integer | no | Filters instances by product ID.|
|priceType	| string | no | Filters instances by price type (OF for offer or NO for normal).|
|isValid	| boolean | no | Filters instances by validity status (True or False).|

## Response

The responses for the PriceViewSets viewset are in JSON format.

## Permissions

The PriceViewSets viewset uses the DjangoModelPermissions permission, which ensures that only authenticated and authorized users can access the operations.
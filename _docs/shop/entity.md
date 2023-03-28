# Model

The Entity model represents an entity that interacts with the system, such as a client or a supplier.

## Fields

`name`: a CharField that stores the name of the entity.

`identifier`: a CharField that stores the identifier of the entity (CPF for individuals or CNPJ for legal entities).

`identifierType`: a CharField that stores the type of identifier. The field has two possible values: "FI" (individual) and "JU" (legal entity).

`entityType`: a CharField that stores the type of entity. The field has two possible values: "CLI" (client) and "FOR" (supplier).

`isActive`: a BooleanField that indicates if the entity is active or not. The default value is True.

`createdAt`: a DateTimeField that stores the date and time when the entity was created. The value is automatically set when a new entity is created.

`updatedAt`: a DateTimeField that stores the date and time when the entity was last updated. The value is automatically updated every time an entity is saved.

`deletedAt`: a DateTimeField that stores the date and time when the entity was deleted. If the entity has not been deleted, this field is null.

## Methods

`delete()`: a method that marks the entity as deleted by setting the deletedAt field to the current date and time. The method also logs the deletion of the entity.

`close()`: a method that marks the entity as deleted by calling the delete() method.

`open()`: a method that restores the entity by setting the deletedAt field to null.


# Viewset

The EntityViewset is a Django Rest Framework Viewset that implements CRUD (Create, Read, Update, and Delete) operations for the Entity model. The Viewset provides the following methods:

`create`: creates a new instance of Entity.

`list`: lists all active instances of Entity.

`retrieve`: retrieves a specific instance of Entity by ID.

`update`: updates a specific instance of Entity.

`partial_update`: partially updates a specific instance of Entity.

`destroy`: marks a specific instance of Entity as deleted.

The EntityViewset uses the EntitySerializer serializer and the DjangoModelPermissions permission, which ensures that only authenticated and authorized users can access the operations.

The Viewset also has a get_queryset() method that returns all active instances of Entity, filtered by name, identifier, identifierType, entityType, and isActive (if there are any filter parameters in the query string).

## Endpoints

The following endpoints are available for the EntityViewset:

| Method | URL | Description |
|--------|-----|-------------|
| POST   | /api/entity/ | Creates a new instance of Entity. |
| GET    | /api/entity/ | Lists all active instances of Entity. |
| GET    | /api/entity/{id}/ | Retrieves a specific instance of Entity by ID. |
| PUT    | /api/entity/{id}/ | Updates a specific instance of Entity. |
| PATCH  | /api/entity/{id}/ | Partially updates a specific instance of Entity. |
| DELETE | /api/entity/{id}/ | Marks a specific instance of Entity as deleted. |

## Parameters

The following parameters are available for the EntityViewset:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | no | Filters instances by name. |
| identifier | string | no | Filters instances by identifier. |
| identifierType | string | no | Filters instances by identifier type. |
| entityType | string | no | Filters instances by entity type. |
| isActive | boolean | no | Filters instances by activity status (True or False). |

## Response

The responses for the EntityViewset are in JSON format.

## Permissions

The EntityViewset uses the DjangoModelPermissions permission, which ensures that only authenticated and authorized users can access the operations.
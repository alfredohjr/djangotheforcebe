# Model

The Document model represents a document that is associated with a transaction, such as an invoice or a receipt.

## Fields

`key`: a CharField that stores the unique identifier of the document.

`deposit`: a ForeignKey that references the Deposit model and indicates the deposit associated with the document.

`entity`: a ForeignKey that references the Entity model and indicates the entity associated with the document.

`documentType`: a CharField that stores the type of document. The field has two possible values: "IN" (for incoming documents) and "OUT" (for outgoing documents).

`isOpen`: a BooleanField that indicates if the document is open or closed. The default value is True.

`createdAt`: a DateTimeField that stores the date and time when the document was created. The value is automatically set when a new document is created.

`updatedAt`: a DateTimeField that stores the date and time when the document was last updated. The value is automatically updated every time a document is saved.

`deletedAt`: a DateTimeField that stores the date and time when the document was deleted. If the document has not been deleted, this field is null.

## Methods

`delete()`: a method that marks the document as deleted by setting the deletedAt field to the current date and time. The method also logs the deletion of the document.

`close()`: a method that marks the document as closed by setting the isOpen field to False.

`open()`: a method that marks the document as open by setting the isOpen field to True.

`total()`: a property that calculates and returns the total value of the document, which is the sum of the values of all DocumentProduct objects associated with the document.

# Viewset

The DocumentViewset is a Django Rest Framework Viewset that implements CRUD (Create, Read, Update, and Delete) operations for the Document model. The Viewset provides the following methods:

`create`: creates a new instance of Document.

`list`: lists all active instances of Document.

`retrieve`: retrieves a specific instance of Document by ID.

`update`: updates a specific instance of Document.

`partial_update`: partially updates a specific instance of Document.

`destroy`: marks a specific instance of Document as deleted.

The DocumentViewset uses the DocumentSerializer serializer and the DjangoModelPermissions permission, which ensures that only authenticated and authorized users can access the operations.

The Viewset also has a get_queryset() method that returns all active instances of Document, filtered by key, deposit_id, entity_id, documentType, and isOpen (if there are any filter parameters in the query string).

## Endpoints

The following endpoints are available for the DocumentViewset:

| Method | URL | Description |
|--------|-----|-------------|
| POST   | /api/document/ | Creates a new instance of Document. |
| GET    | /api/document/ | Lists all active instances of Document. |
| GET    | /api/document/{id}/ | Retrieves a specific instance of Document by ID. |
| PUT    | /api/document/{id}/ | Updates a specific instance of Document. |
| PATCH  | /api/document/{id}/ | Partially updates a specific instance of Document. |
| DELETE | /api/document/{id}/ | Marks a specific instance of Document as deleted. |

## Parameters

The following parameters are available for the DocumentViewset:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| key | string | no	| Filters instances by key. |
| deposit_id | integer | no | Filters instances by deposit ID. |
| entity_id | integer | no | Filters instances by entity ID. |
| documentType | string | no | Filters instances by document type. |
| isOpen | boolean | no | Filters instances by open status (True or False). |

## Response

The responses for the DocumentViewset are in JSON format.

## Permissions

The DocumentViewset uses the DjangoModelPermissions permission, which ensures that only authenticated and authorized users can access the operations.
# The Log Models

The five Django models provided (`ProductLog`, `EntityLog`, `DocumentLog`, `DepositLog`, and `CompanyLog`) share many similarities. They are all log models that represent changes made to objects in different parts of a system.

In addition, all five models use a Django signal (`pre_save`) to prevent the data from being modified via the application layer. This ensures that changes made to objects are properly recorded in the log, and that the log accurately reflects the state of the system at any given time. By using signals to intercept changes made to objects, these models provide a reliable and consistent way of logging changes across different parts of the system.

The models share other common fields, such as `table`, `transaction`, `message`, `createdAt`, `updatedAt`, and `deletedAt`, as well as common methods like `register()`, `delete()`, `open()`, and `close()`. These fields and methods enable the models to store detailed information about changes made to objects and to manipulate the deletedAt field as needed.

Overall, these models follow a consistent design pattern for logging changes made to objects in a system, while also ensuring that the log accurately reflects the state of the system at any given time by preventing data from being modified via the application layer.
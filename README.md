# The Force Backend

The Force Backend is a sales application that allows you to manage different aspects of your business. It is built on Django Rest Framework and offers a RESTful API that can be used to perform various operations related to sales, inventory, purchasing, and more.

## Features

The following are the main features of The Force Backend:

**Company**: Allows you to register a company, which includes basic information such as name, address, and contact details.[Detail here](_docs/shop/company.md)

![](_docs/shop/gifs/company.gif)

**Deposit**: Allows you to register a warehouse or store where you keep your products. You can assign products to different deposits and manage their inventory accordingly.[Detail here](_docs/shop/deposit.md)

![](_docs/shop/gifs/deposit.gif)

**Product**: Allows you to register different products that you sell. You can specify the name, description, and other details of each product.[Detail here](_docs/shop/product.md)

![](_docs/shop/gifs/product.gif)

**Price**: Allows you to set different prices for your products. You can specify the price for a particular product in a particular currency.[Detail here](_docs/shop/price.md)

![](_docs/shop/gifs/price.gif)

**Entity**: Allows you to register customers and suppliers. You can specify their basic information such as name, address, and contact details.[Detail here](_docs/shop/entity.md)

![](_docs/shop/gifs/entity.gif)

**Document**: Allows you to manage documents such as invoices, purchase orders, and delivery notes. You can specify the type of document, the associated entity, and the products involved.[Detail here](_docs/shop/document.md)

![](_docs/shop/gifs/document.gif)

**DocumentProduct**: Allows you to specify the details of each product in a document. You can specify the quantity, price, and other details for each product.[Detail here](_docs/shop/documentProduct.md)

**Stock**: Allows you to manage the inventory of your products in different deposits. You can view the stock levels of each product in each deposit.[Detail here](_docs/shop/stock.md)

![](_docs/shop/gifs/stock.gif)

**StockMovement**: Allows you to manage the movements of your stock, such as when products are received or shipped out of a particular deposit.[Detail here](_docs/shop/stockMovement.md)

**Logs**: The system records various events such as product creation, inventory changes, and document updates in different log models (CompanyLog, DepositLog, DocumentLog, EntityLog, and ProductLog). These logs provide a detailed history of changes made to the system over time.[Detail here](_docs/shop/tableLogs.md)

## Installation

To install and run The Force Backend on your local machine, follow these steps:

1. Clone the repository to your local machine.
1. Install Python 3 on your machine if you haven't already done so.
1. Create a virtual environment for the project and activate it.
1. Install the required dependencies using `pip install -r requirements.txt`.
1. Set up the database by running `python manage.py migrate`.
1. Start the development server using `python manage.py runserver`.
   
To access the documentation, start the development server and go to http://localhost:8000/swagger/. The Swagger UI allows you to browse the available endpoints and their parameters, and test the API directly from the browser.
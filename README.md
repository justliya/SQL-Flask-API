Order Management System 📦

1. Project Description

The Order Management System is a simple backend project that helps manage users, orders, and products. It allows users to create orders, add products to orders, and retrieve data easily. This project demonstrates basic database operations and relationships using Flask.

What Does the Application Do?

	•	Allows users to create, update, view, and delete their profiles.
	•	Enables users to create orders and associate them with products.
	•	Prevents duplicate products in the same order.
	•	Lets users retrieve all orders and products linked to their profiles.

Why Use These Technologies?

This project was built using Flask and SQLAlchemy because:
	•	Flask is efficient for creating REST APIs.
	•	SQLAlchemy simplifies database management and relationships.
	•	Marshmallow makes it easy to validate and serialize data.

Challenges Faced

	•	Understanding and implementing many-to-many relationships.
	•	Preventing duplicate entries in the order_product association table.
	•	Keeping the code clean and organized.

Possible Features to Implement in the Future

	•	Add user login and authentication.
	•	Track inventory for products.
	•	Build a simple interface for managing orders and products.
	•	Generate reports for orders and sales.

2. How to Use the Application

Example Workflow:

	1.	Manage Users:
	•	Create a user by sending a POST request to /users.
	•	View all users with a GET request to /users.
	•	Retrieve, update, or delete a user with /users/<id>.
	2.	Manage Products:
	•	Add a product with a POST request to /products.
	•	View all products with a GET request to /products.
	•	Retrieve, update, or delete a product with /products/<id>.
	3.	Manage Orders:
	•	Create an order by sending a POST request to /orders.
	•	Add a product to an order with /orders/<order_id>/add_product/<product_id>.
	•	View all products in an order with /orders/<order_id>/products.
	•	Retrieve or delete an order with /orders/<order_id>.

4. Key Features and Functionalities

	•	User Management:
Create, update, view, and delete user profiles.
	•	Order Management:
Create orders, link them to users, and add products.
	•	Product Management:
Add products, update details, and delete them.
	•	Data Validation:
Ensure unique emails for users and prevent duplicate products in orders.



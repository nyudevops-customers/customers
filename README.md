# Customers
[![Build Status](https://app.travis-ci.com/nyudevops-customers/customers.svg?branch=main)](https://app.travis-ci.com/nyudevops-customers/customers)

Created for NYU Devops project, Fall 2021. Microservices built for handling customer data for an e-commerce site.

## API Routes Documentation for Customers

| HTTP Method | URL | Description | Return
| :--- | :--- | :--- | :--- |
| `GET` | `/customers/{customer_id}` | Get customer by ID | Customer Object
| `GET` | `/customers` | Returns a list of all the Customers | Customer Object
| `POST` | `/customers` | Creates a new Customer record in the database | Customer Object
| `PUT` | `/customers/{customer_id}` | Updates/Modify a Customer record in the database | Customer Object
| `DELETE` | `/customers/{customer_id}` | Delete the Customer with the given id number | 204 Status Code


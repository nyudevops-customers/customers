Feature: The customers service back-end
    As a Customer Website
    I need a RESTful catalog service
    So that I can keep track of all my customers

Background:
    Given the following customers
        | firstname   | lastname   | email_id         | address          | phone_number   | card_number   | active   |
        | Bill        | Green      | bg12@gmail.com   | 130 Rriver Drive | 100988814      | 55597572893   | True     |
        | Betty       | Williams   | bw34@gmail.com   | 34th Street      | 999988814      | 66698572893   | True     |
        | Alice       | Brown      | ab56@gmail.com   | 5th Street       | 222333444      | 33398572111   | False    |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Customers RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Customer
    When I visit the "Home Page"
    And I set the "firstname" to "Tom"
    And I set the "lastname" to "Steven"
    And I set the "email_id" to "123@gmail.com"
    And I set the "address" to "102 XYZ St"
    And I set the "phone_number" to "200988884"
    And I set the "card_number" to "48097572893"
    And I select "True" in the "active" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "customer_id" field
    And I press the "Clear" button
    Then the "customer_id" field should be empty
    And the "firstname" field should be empty
    And the "lastname" field should be empty
    And the "email_id" field should be empty
    And the "address" field should be empty
    And the "phone_number" field should be empty
    And the "card_number" field should be empty
    And the "active" field should be empty
    When I paste the "customer_id" field
    And I press the "Retrieve" button
    Then I should see "Tom" in the "firstname" field
    Then I should see "Steven" in the "lastname" field
    Then I should see "123@gmail.com" in the "email_id" field
    Then I should see "102 XYZ St" in the "address" field
    Then I should see "200988884" in the "phone_number" field
    Then I should see "48097572893" in the "card_number" field
    Then I should see "True" in the "active" dropdown

# Scenario: List all Customers
#     When I visit the "Home Page"
#     And I press the "Search" button
#     Then I should see "Bill" in the results
#     And I should see "Betty" in the results


# Scenario: Query customers by first name
#     When I visit the "Home Page"
#     And I set the "firstname" to "Bill"
#     And I press the "Search" button
#     Then I should see "Bill" in the results
#     And I should not see "Betty" in the results
#     And I should not see "Alice" in the results
    
# Scenario: Query customers by last name
#     When I visit the "Home Page"
#     And I set the "lastname" to "Green"
#     And I press the "Search" button
#     Then I should see "Green" in the results  
#     And I should not see "Williams" in the results
#     And I should not see "Brown" in the results


# Scenario: Query customers by email_id
#     When I visit the "Home Page"
#     And I set the "email_id" to "bw34@gmail.com"
#     And I press the "Search" button
#     Then I should see "bw34@gmail.com" in the "email_id" field
#     And I should see "Betty" in the "firstname" field
#     And I should see "Williams" in the "lastname" field
#     And I should not see "bg12@gmail.com" in the results

# Scenario: Query customers by active status
#     When I visit the "Home Page"
#     And I select "True" in the "active" dropdown
#     And I press the "Search" button
#     Then I should see all customers with "true" in the results
   
# Scenario: Update a Customer
#     When I visit the "Home Page"
#     And I set the "firstname" to "Bill"
#     And I press the "search" button
#     Then I should see "Bill" in the "firstname" field
#     And I should see "Green" in the "lastname" field
#     And I should see "bg12@gmail.com" in the "email_id" field
#     And I should see "130 Rriver Drive" in the "address" field
#     When I change "address" to "140 Apt"
#     And I press the "Update" button
#     Then I should see the message "Success"
#     When I copy the "customer_id" field
#     And I press the "Clear" button
#     And I paste the "customer_id" field
#     And I press the "Retrieve" button
#     Then I should see "140 Apt" in the "address" field
#     When I press the "Clear" button
#     And I set the "firstname" to "Bill"
#     And I press the "Search" button
#     #And I should see "Bill" in the "firstname" field
#     #And I should see "Green" in the "lastname" field
#     #And I should see "bg12@gmail.com" in the "email_id" field
#     Then I should see "140 Apt" in the "address" field
#     And I should not see "130 Rriver Drive" in the results
    
# Scenario: Delete a Customer
#     When I visit the "Home Page"
#     And I press the "Search" button
#     And I copy the "customer_id" field
#     And I press the "Clear" button
#     And I paste the "customer_id" field
#     And I press the "Delete" button
#     Then I should see the message "Success"
#     And I should not see "Server error!" in the results
    
   
# Scenario: Activate a Customer
#     When I visit the "Home Page"
#     And I select "False" in the "active" dropdown
#     And I press the "Search" button
#     And I copy the "customer_id" field
#     And I press the "Clear" button
#     And I paste the "customer_id" field
#     And I press the "Activate" button
#     Then I should see the message "Success"
#     When I press the "Clear" button
#     And I select "True" in the "active" dropdown
#     And I press the "Search" button
#     Then I should see all customers with "true" in the results

# Scenario: Deactivate a Customer
#     When I visit the "Home Page"
#     And I select "True" in the "active" dropdown
#     And I press the "Search" button
#     And I copy the "customer_id" field
#     And I press the "Clear" button
#     And I paste the "customer_id" field
#     And I press the "Deactivate" button
#     Then I should see the message "Success"
#     When I press the "Clear" button
#     And I select "False" in the "active" dropdown
#     And I press the "Search" button
#     Then I should see all customers with "false" in the results
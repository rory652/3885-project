# Endpoints

## Users
***
### Register User
#### Request Structure
!!! info
    - Request Type: `POST`
    - Endpoint: `/api/users/`
  
    |    Field    |  Type   |        Description         |
    |:-----------:|:-------:|:--------------------------:|
    |   `email`   | String  |        User's email        |
    |   `name`    | String  |        User's name         |
    | `username`  | String  |      User's username       |
    | `password`  | String  | User's password (unhashed) |
    | `care-home` | Integer |        Care home ID        |
#### Response
???+ success "Register User Successful Response"
    ``` json
    {
        "Response": "Here"
    }
    ```
??? failure "Register User Failure"
    ``` json
    {
        "Error": "Here"
    }
    ```
### Log-in
#### Request Structure
!!! info
    - Request Type: `POST`
    - Endpoint: `/api/login/`

    |   Field    |  Type  |        Description         |
    |:----------:|:------:|:--------------------------:|
    |   `name`   | String |  User's username or email  |
    | `password` | String | User's password (unhashed) |

#### Response
???+ success "Log-in Successful Response"
    ``` json
    {
        "Response": "Here"
    }
    ```
??? failure "Log-in Failure"
    ``` json
    {
        "Error": "Here"
    }
    ```
### Log-out
#### Request Structure
!!! info
    - Request Type: `POST`
    - Endpoint: `/api/logout/`

    |    Field     |  Type   |       Description       |
    |:------------:|:-------:|:-----------------------:|
    | `session-id` | Integer | Session ID for the user |

#### Response
???+ success "Log-out Successful Response"
    ``` json
    {
        "Response": "Here"
    }
    ```
??? failure "Log-out Failure"
    ``` json
    {
        "Error": "Here"
    }
    ```
### Update User
#### Request Structure
!!! info
    - Request Type: `PUT`
    - Endpoint: `/api/users/<user-id>/`

    |     Field      |  Type  |          Description           |
    |:--------------:|:------:|:------------------------------:|
    |     `name`     | Header |    User's username or email    |
    |   `password`   | Header |   User's password (unhashed)   |
    |   `new-name`   | Header |      User's new username       |
    | `new-password` | Header | User's new password (unhashed) |

#### Response
???+ success "Update User Successful Response"
    ``` json
    {
        "Response": "Here"
    }
    ```
??? failure "Update User Failure"
    ``` json
    {
        "Error": "Here"
    }
    ```
### Remove User
#### Request Structure
!!! info
    - Request Type: `DELETE`
    - Endpoint: `/api/users/<user-id>`

    |   Field    |  Type  |        Description         |
    |:----------:|:------:|:--------------------------:|
    |  `email`   | String |        User's email        |
    | `username` | String |      User's username       |
    | `password` | String | User's password (unhashed) |

#### Response
???+ success "Remove User Successful Response"
    ``` json
    {
        "Response": "Here"
    }
    ```
??? failure "Remove User Failure"
    ``` json
    {
        "Error": "Here"
    }
    ```

## Admin
***
### View Care Home
#### Request Structure
!!! info
    - Request Type: `GET`
    - Endpoint: `/api/homes/<care-home-id>/`

    | Field  |      Type      |               Description                |
    |:------:|:--------------:|:----------------------------------------:|
    | `auth` | Authentication | Authentication information for the admin |

#### Response
???+ success "View Care Home Successful Response"
    ``` json
    {
        "Response": "Here"
    }
    ```
??? failure "View Care Home Failure"
    ``` json
    {
        "Error": "Here"
    }
    ```

## Contacts
***
### Get Contacts
#### Request Structure
!!! info
    - Request Type: `GET`
    - Endpoint: `/api/contacts/`
    - Contacts for an individual resident can be accquired using `/api/residents/<resident-id>/contacts`

    | Field  |      Type      |               Description               |
    |:------:|:--------------:|:---------------------------------------:|
    | `auth` | Authentication | Authentication information for the user |

#### Response
???+ success "Get Contacts Successful Response"
    ``` json
    {
        "Response": "Here"
    }
    ```
??? failure "Get Contacts Failure"
    ``` json
    {
        "Error": "Here"
    }
    ```
### Acknowledge Contact
#### Request Structure
!!! info
    - Request Type: `POST`
    - Endpoint: `/api/contacts/<contact-id>`

    |   Field    |      Type      |                      Description                       |
    |:----------:|:--------------:|:------------------------------------------------------:|
    |   `auth`   | Authentication |        Authentication information for the user         |
    | `positive` |    Boolean     | Whether the contact resulted in a positive case or not |

#### Response
???+ success "Aknowledge Contact Successful Response"
    ``` json
    {
        "Response": "Here"
    }
    ```
??? failure "cknowledge Contact Failure"
    ``` json
    {
        "Error": "Here"
    }
    ```

## Cases
***
### Get Cases
#### Request Structure
!!! info
    - Request Type: `GET`
    - Endpoint: `/api/cases/`

    | Field  |      Type      |               Description               |
    |:------:|:--------------:|:---------------------------------------:|
    | `auth` | Authentication | Authentication information for the user |

#### Response
???+ success "Get Cases Successful Response"
    ``` json
    {
        "Response": "Here"
    }
    ```
??? failure "Get Cases Failure"
    ``` json
    {
        "Error": "Here"
    }
    ```
### Register Case
#### Request Structure
!!! info
    - Request Type: `POST`
    - Endpoint: `/api/cases/`

    |     Field     |      Type      |                 Description                  |
    |:-------------:|:--------------:|:--------------------------------------------:|
    |    `auth`     | Authentication |   Authentication information for the user    |
    | `resident-id` |    Integer     |           ID of infected resident            |
    |    `date`     |      Date      | Current date (when the contact was detected) |

#### Response
???+ success "Register Case Successful Response"
    ``` json
    {
        "Response": "Here"
    }
    ```
??? failure "Register Case Failure"
    ``` json
    {
        "Error": "Here"
    }
    ```
### Remove Case
#### Request Structure
!!! info
    - Request Type: `DELETE`
    - Endpoint: `/api/cases/<case-id>/`

    |   Field   |      Type      |               Description               |
    |:---------:|:--------------:|:---------------------------------------:|
    |  `auth`   | Authentication | Authentication information for the user |

#### Response
???+ success "Remove Case Successful Response"
    ``` json
    {
        "Response": "Here"
    }
    ```
??? failure "Remove Case Failure"
    ``` json
    {
        "Error": "Here"
    }
    ```

## Residents
***
### View Residents
#### Request Structure
!!! info
    - Request Type: `GET`
    - Endpoint: `/api/residents/`
    - Information for a specific resident can be accquired using `/api/residents/<resident-id>/`

    | Field  |      Type      |               Description               |
    |:------:|:--------------:|:---------------------------------------:|
    | `auth` | Authentication | Authentication information for the user |

#### Response
???+ success "View Residents Successful Response"
    ``` json
    {
        "Response": "Here"
    }
    ```
??? failure "View Residents Failure"
    ``` json
    {
        "Error": "Here"
    }
    ```
### Add Resident
#### Request Structure
!!! info
    - Request Type: `POST`
    - Endpoint: `/api/residents/`

    | Field  |      Type      |               Description               |
    |:------:|:--------------:|:---------------------------------------:|
    | `auth` | Authentication | Authentication information for the user |
    | `name` |     String     |             Resident's name             |

#### Response
???+ success "Add Resident Successful Response"
    ``` json
    {
        "Response": "Here"
    }
    ```
??? failure "Add Resident Failure"
    ``` json
    {
        "Error": "Here"
    }
    ```
### Remove Resident
#### Request Structure
!!! info
    - Request Type: `DELETE`
    - Endpoint: `/api/residents/<resident-id>/`

    |     Field     |      Type      |               Description               |
    |:-------------:|:--------------:|:---------------------------------------:|
    |    `auth`     | Authentication | Authentication information for the user |

#### Response
???+ success "Remove Resident Successful Response"
    ``` json
    {
        "Response": "Here"
    }
    ```
??? failure "Remove Resident Failure"
    ``` json
    {
        "Error": "Here"
    }
    ```

## Modules
***
### Get Status
#### Request Structure
!!! info
    - Request Type: `GET`
    - Endpoint: `/api/modules/`
    - Status of an individual module can be accquired using `/api/modules/<module-id>/`

    | Field  |      Type      |               Description               |
    |:------:|:--------------:|:---------------------------------------:|
    | `auth` | Authentication | Authentication information for the user |

#### Response
???+ success "Get Status Successful Response"
    ``` json
    {
        "Response": "Here"
    }
    ```
??? failure "Get Status Failure"
    ``` json
    {
        "Error": "Here"
    }
    ```
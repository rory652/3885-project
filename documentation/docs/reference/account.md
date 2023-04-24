# Account Creation

This section contains all the steps necessary to create a new care home, 
a new account for the care home and login to that account

## Create a Care Home
To create a care home, you simply need to make a POST request to the 'carehomes' endpoint (https://api.jerbtracker.co.uk/carehomes).
This request will return three headers:
```json
{
  "id": "87654321",
  "nurse-code": "12345678",
  "admin-code": "12344321"
}
```
- The 'id' header is the ID of the care home. This will be used in all subsequent requests.
- The 'nurse-code' is a hex code that is supplied when creating a nurse account.
- The 'admin-code' is the same but creates an admin account.

## Create an Account
To create an account, you need to make a POST request to the 'users' endpoint (https://api.jerbtracker.co.uk/{carehome}/users).
Replace {carehome} with the ID generated in the previous step. The body for this request is as follows:
```json
{
  "username": "johnSmith1967",
  "password": "strongPassword",
  "code": "12345678"
}
```
Use the code generated in the previous step depending on which role you want the user to have.
These codes should be kept secret so devious users don't have access to data they shouldn't.

## Login
Logging in is very simple, just make a POST request to the 'login' endpoint (https://api.jerbtracker.co.uk/{carehome}/login).
You just need to supply your username and password:
```json
{
  "username": "johnSmith1967",
  "password": "strongPassword"
}
```
This will return a header called 'SESSION-ID'. To interact with the other endpoints, you need to supply this header in subsequent requests.

To logout, just make a DELETE request to the same endpoint with your session ID. The session will be deleted and you will be logged out.
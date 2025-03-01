# Order Management API Postman Collection

This repository contains a Postman collection for testing the Order Management API.

## How to Use

1. **Download the Collection**:

   - Download the `Order_Management_API.postman_collection.json` file from this repository.

2. **Import the Collection into Postman**:

   - Open Postman.
   - Click on the **Import** button.
   - Select the downloaded JSON file.

3. **Set Up Environment Variables**:

   - Create a new environment in Postman.
   - Add the following variables:
     - `base_url`: `http://127.0.0.1:8000`
     - `access_token`: (Leave this blank; it will be populated after logging in.)

4. **Test the Endpoints**:
   - Use the `Register` and `Login` requests to get an access token.
   - Use the token to authenticate other requests.

## Endpoints Included

- **Register**: `POST /api/register/`
- **Login**: `POST /api/login/`
- **Get All Orders**: `GET /api/orders/`
- **Create an Assign**: `POST /api/assigns/`
- **Get Driver-Specific Schedules**: `GET /api/driver-schedules/`
- **Get All Completed Orders**: `GET /api/completed-orders/`

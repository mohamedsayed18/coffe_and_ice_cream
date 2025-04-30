# Irdeto_sw_tasks

## REST API Endpoints

| Endpoint                         | Method | Description                                      | Request Body Example                        |
|----------------------------------|--------|--------------------------------------------------|---------------------------------------------|
| `/login/`                        | POST   | Log in a user                                   | `{ "username": "admin", "password": "1234" }`|
| `/state/`                        | GET    | Get the current system state                    | —                                           |
| `/state/`                        | POST   | Change the system state                         | `{ "new_state": "Dashboard" }`              |
| `/items/`                        | GET    | List items (pagination and filtering supported) | —                                           |
| `/items/`                        | POST   | Create a new item                               | `{ "description": "Item A", "state": "init" }`|
| `/items/<item_id>/`             | GET    | Get a single item by ID                         | —                                           |
| `/items/<item_id>/state/`       | PUT    | Change the state of a specific item             | `{ "state": "pause" }`                      |
| `/user/`                         | PUT    | Update user credentials                         | `{ "username": "new_user", "password": "new_pass" }`|
| `/item-control/`                | PUT    | Allow or deny item control access               | `{ "allowed": true }`                       |

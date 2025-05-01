# Irdeto_sw_tasks
1. [API Design and API Test Design](#api-design-and-api-test-design)
2. [Unit Testing](#unit-testing)
3. [DASH Parsing and Validation](#dash-parsing-and-validation)

## API Design and API Test Design
### REST API Endpoints

| Endpoint                         | Method | Description                                      | Request Body Example                        |
|----------------------------------|--------|--------------------------------------------------|---------------------------------------------|
| `/myapi/login/`                        | POST   | Log in a user                                   | `{ "username": "admin", "password": "1234" }`|
| `/myapi/state/`                        | GET    | Get the current system state                    | —                                           |
| `/myapi/state/`                        | POST   | Change the system state                         | `{ "new_state": "Dashboard" }`              |
| `/myapi/items/`                        | GET    | List items (supports `page`, `page_size`, `sort`, `state`) | —                                           |
|                                  |        | Example(/items/?page=1&page_size=5&sort=desc&state=run) |                                     |
| `/myapi/items/?id=`                        | GET    | List item by id. Example(/items/?id=hbo)| —                                           |
| `/myapi/items/`                        | POST   | Create a new item                               | `{ "id": "A", description": "Item A"}`|
| `/myapi/items/<item_id>/state/`       | PUT    | Change the state of a specific item             | `{ "state": "pause" }`                      |
| `/myapi/user/`                         | PUT    | Update user credentials                         | `{ "username": "new_user", "password": "new_pass" }`|
| `/myapi/item-control/`                | PUT    | Allow or deny item control access               | `{ "allowed": true }`                       |

### State transition diagram
![](./api_mvp/state_transition_diagram.png)

##### Run the demo
```
cd api_mvp/
python manage.py runserver 
```
You can use postman or any other tool to test the server on `http://localhost:8000/`

##### Run tests
```
cd api_mvp/
python manage.py test
```

#### Explanation
I used Django to build a web app and implement the API


## Unit Testing

Run tests: `pytest Math_function/test_discontinuous_function.py`

![](plot.png)

## DASH Parsing and Validation

Run code: `python3 period_checker/period_validity.py`

I check the validity of a Period by checking the following:
* If there is a `start` attribute exists in a `Period` tag
* If there is one or more `adaptationsets`
* If there is one or more `Representation`
* If there is a `SegmentTemplate`
* If there is a media attribute in the SegmentTemplate tag
* If the media format is `$Number$` or `$Time$`

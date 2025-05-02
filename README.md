# Software Challenges
1. [API Design and API Test Design](#api-design-and-api-test-design)
2. [Unit Testing](#unit-testing)
3. [DASH Parsing and Validation](#dash-parsing-and-validation)

## 🛠️ API Design and API Test Design
I used Django to build a web app and implement the API
### REST API Endpoints

| Endpoint                         | Method | Description                                      | Request Body Example                        |
|----------------------------------|--------|--------------------------------------------------|---------------------------------------------|
| `/myapi/login/`                        | POST   | Log in a user                                   | `{ "username": "admin", "password": "1234" }`|
| `/myapi/state/`                        | GET    | Get the current system state, mainly used for testing | —                                           |
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

##### Installation
1. Install dependencies
```bash
pip install -r /api_mvp/requirements.txt
```
2. Apply Migrations (Creates tables)
```bash
cd api_mvp/
python manage.py migrate
```
3. populate initial data into data base
```bash
python manage.py loaddata initial_data.json
```
Then you can run the server and test the api manually using postman or any other tool, the server runs on `http://localhost:8000/`
```bash
python manage.py runserver 
```

Or you can Run tests(Run server is not needed)
```bash
python manage.py test
```

## 🧪 Unit Testing
```bash
pytest Math_function/test_discontinuous_function.py
```
![](./Math_function/plot.png)

## ✅ DASH Parsing and Validation
```bash
python3 period_checker/period_validity.py
```
I started by looking at the DASH format documentation https://developers.broadpeak.io/docs/foundations-dash#periods.
I check the validity of a Period by checking the following:
* If there is a `start` attribute exists in a `Period` tag
* If there is one or more `adaptationsets`
* If there is one or more `Representation`
* If there is a `SegmentTemplate`
* If there is a `media` attribute in the SegmentTemplate tag
* If the media format is `$Number$` or `$Time$`

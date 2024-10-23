# Weather API with Django
This project provides a Weather API built with Django. It includes endpoints to retrieve weather data and statistics, and comes with integrated Swagger and ReDoc documentation for easy API exploration.

# Endpoints
There are 4 endpoints in this project:-
  1. `/api/weather/`
  2. `/api/weather/stats/`
  3. `/swagger`
  4. `/redoc`

# Project Structure
```bash
.
├── venv/
└── weather_app/
    ├── data/
    │   ├── wx_data/
    │   └── yld_data
    ├── screenshots/
    ├── weather_api/
    │   ├── management/
    │   │   └── commands/
    │   │       └── create.py
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── serializers.py
    │   ├── tests.py
    │   └── views.py
    ├── weather_app/
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── .coveragerc
    ├── .gitignore
    ├── approach.md
    ├── docker-compose.yml
    ├── Dockerfile
    ├── manage.py
    ├── pytest.ini
    ├── readme.md
    └── requirements.txt
```
# Project Setup and Installation
1. Clone the project
2. Install the docker using this  [link](https://docs.docker.com/engine/install/).
3. Run the docker container using below command:-
```bash
docker-compose up --build -d
```
```commandline
docker exec -it <container_id> python manage.py makemigrations weather_api
```
```commandline
docker exec -it <container_id> python manage.py migrate
```
```commandline
docker exec -it <container_id> python manage.py create
```

<img src="screenshots/image9.png" alt="coverage output" />


# To access the API endpoints
You can access the following API endpoints:

- **Retrieve Weather Records:** `/api/weather/`
  
- **Retrieve Weather Statistics:** `/api/weather/stats/`

- **View the Swagger Documentation:** `/swagger`

- **View the ReDoc API Documentation:** `/redoc`


# Testing
To run the testcases use this command:-
```bash
python manage.py test
```
# Coverage
To get the coverage use this command:-
```bash
coverage run --source='.' manage.py test
coverage report
```
<img src="screenshots/image2.png" alt="coverage output" />

### Screenshot of Testcase output
<img src="screenshots/image1.png" alt="testcase output" />

# Screenshots of API Response
<img src="screenshots/image3.png" alt="record success response" />
<br><br>
<img src="screenshots/image7.png" alt="record empty response" />
<br><br>
<img src="screenshots/image4.png" alt="stats success response" />
<br><br>
<img src="screenshots/image8.png" alt="stats empty response" />

# Screenshots of Swagger Response
<img src="screenshots/image5.png" alt="swagger record api response" />
<br><br>
<img src="screenshots/image6.png" alt="swagger stats api response" />

##

### To open AWS Deployment Steps please follow the link ([approach.md](/approach.md))

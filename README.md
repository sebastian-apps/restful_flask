# RESTful Flask

To-Do List RESTful API in Flask for tracking tasks and tracking the steps involved for completing tasks.


<br />

## Installation

Clone the repository.

```bash
git clone https://github.com/sebastian-apps/restful_flask.git
```

Create the virtual environment.

```
cd restful_flask
cd web
python -m venv env
```

Activate the virtual environment <i>for OSX</i>.

```
source env/bin/activate
```

Activate the virtual environment <i>for Windows</i>.

```
env\Scripts\activate
```

Install dependencies. The installation works best with Python 3.7.7.

```bash
pip install -r requirements.txt
```

<br />

## Running the application

Run the Flask app.

```bash
flask run
```

In another terminal, run restful_flask/web/test.py as the client for the API.

```bash
python test.py
```

<br />

## Running the Dockerized application

Alternatively, run the API as a Dockerized application. 
Build the Docker container.

```bash
docker build -t todo_flask:latest .
```

Run the container.

```bash
docker run -d -p 5000:5000 todo_flask
```

Check the process status of the application.<br>
todo_flask should be up and running.

```bash
docker ps -a
```


In another terminal, run restful_flask/web/test.py as the client for the API.

```bash
python test.py
```


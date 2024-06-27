# Todo-app

This is a simple Todo application built with Flask and SQLAlchemy. It allows users to create, read, and delete "Things". Each "Thing" has a name and a list of tags(optional).
![Todo-app](https://raw.githubusercontent.com/Pegoku/Todo-app/main/img/image.png)

## Features

- Create, read, and delete "Things"
- Add tags to "Things"
- Filter "Things" by tags
- Bulk delete "Things"

## Installation

1. Clone this repository: `git clone https://github.com/Pegoku/Todo-app.git`
2. Navigate to the project directory: `cd Todo-app`
3. Install the required packages: `pip install -r requirements.txt`
4. Run the application: `python start.py`

## Docker

This application can also be run using Docker. Here are the steps to do so:

1. Build the Docker image: `docker build -t todo-app .`
2. Run the Docker container mounting the folder where the db will be stored: `docker run -p 5000:5000 -v /path/to/local/dir:/app/instance/ todo-app` 

After running these commands, you can access the application at `http://localhost:5000`.

## Usage

Open your web browser and navigate to `http://localhost:5000` to start using the application.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

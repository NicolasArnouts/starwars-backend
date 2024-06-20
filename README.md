# Star Wars Backend

This project is a backend service for managing Star Wars characters and teams. It is built with Django and Django REST Framework and uses PostgreSQL as its database.

## Table of Contents

- [Star Wars Backend](#star-wars-backend)
  - [Table of Contents](#table-of-contents)
  - [Project Setup](#project-setup)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
      - [Docker Installation](#docker-installation)
      - [Manual Installation](#manual-installation)
    - [Environment Variables](#environment-variables)
  - [Usage](#usage)
    - [Running the Project](#running-the-project)
    - [Accessing the API](#accessing-the-api)
  - [API Endpoints](#api-endpoints)
    - [Authentication](#authentication)
    - [Characters](#characters)
    - [Teams](#teams)
  - [Running Tests](#running-tests)
  - [Fetching Characters](#fetching-characters)
  - [Creating a Superuser](#creating-a-superuser)
  - [Postman Collection](#postman-collection)
  - [Useful Docker Commands](#useful-docker-commands)
  - [License](#license)

## Project Setup

### Prerequisites

- Docker
- Docker Compose

### Installation

#### Docker Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/NicolasArnouts/starwars-backend.git
    cd starwars-backend
    ```

2. Create a `.env` file based on `.env.example`:

    ```bash
    cp .env.example .env
    ```

3. Update the `.env` file with your own configuration values.

4. Build and start the Docker containers:

    ```bash
    docker-compose up --build -d
    ```
5. Create a superuser:
  [Creating a Superuser](#creating-a-superuser)

6. Optional: (re)Fetch data:
   [Fetching Characters](#fetching-characters)

#### Manual Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/NicolasArnouts/starwars-backend.git
    cd starwars-backend
    ```

2. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:

      ```bash
      .\venv\Scripts\activate
      ```

    - On macOS and Linux:

      ```bash
      source venv/bin/activate
      ```

4. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Create a `.env` file based on `.env.example`:

    ```bash
    cp .env.example .env
    ```

6. Update the `.env` file with your own configuration values.

7. Apply the migrations:

    ```bash
    python manage.py migrate
    ```

8. Fetch initial character data:

    ```bash
    python manage.py fetch_characters
    ```

9. Start the Django development server:

    ```bash
    python manage.py runserver
    ```

### Environment Variables

The project requires the following environment variables to be set:

- `SECRET_KEY`: Django secret key.
- `DEBUG`: Debug mode (set to `True` for development).
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts.
- `DB_NAME`: Database name.
- `DB_USER`: Database user.
- `DB_PASSWORD`: Database password.
- `DB_HOST`: Database host (typically `db` when using Docker Compose).
- `DB_PORT`: Database port (typically `5432` for PostgreSQL).
- `APP_PORT`: Application port (e.g., `8088`).
- `APP_HOST`: Application host (e.g., `0.0.0.0`).

## Usage

### Running the Project

To run the project, use Docker Compose:

```bash
docker-compose up -d
```

### Accessing the API

Once the project is running, you can access the API at:

```
http://localhost:8088/api/
```

## API Endpoints

### Authentication

- `POST /api/token/`: Obtain JWT token.
- `POST /api/token/refresh/`: Refresh JWT token.

### Characters

- `GET /api/characters/`: List all characters.
- `GET /api/characters/{id}/`: Retrieve a specific character.
- `GET /api/characters/?name={name}&height={height}&mass={mass}&gender={gender}&homeworld={homeworld}&species={species}&hairColor={hairColor}&eyeColor={eyeColor}&skinColor={skinColor}&born={born}&died={died}`: Filter characters by various parameters.

### Teams

- `GET /api/team/`: List all teams.
- `POST /api/team/`: Create a new team.
- `DELETE /api/team/{id}/`: Delete a team.
- `POST /api/team/{id}/add_member/`: Add a member to a team.
- `POST /api/team/{id}/remove_member/`: Remove a member from a team.

## Running Tests

To run the tests in Docker, use the following command:

```bash
docker-compose exec web pytest
```

## Fetching Characters

To fetch the Star Wars characters using Docker, use the following command:

```bash
docker-compose exec web python manage.py fetch_characters
```

## Creating a Superuser

To create a superuser in the bash shell within the Docker container, use the following command:

1. Open a bash shell inside the running web container:

    ```bash
    docker-compose exec web /bin/bash
    ```

2. Create a superuser:

    ```bash
    python manage.py createsuperuser
    ```

Remember this info as you will need it to authenticate to the API

## Postman Collection

A Postman collection is included in the repository. You can find it at `postman_collection.json`. Import this collection into Postman to interact with the API endpoints easily. Make sure you change the collection environment values to django_username, django_password which are valid account credentials.

## Useful Docker Commands

Here are some additional Docker commands that might be useful for managing your development environment:

- To open a bash shell inside the running web container:

    ```bash
    docker-compose exec web /bin/bash
    ```

- To rebuild and start the Docker containers in detached mode:

    ```bash
    docker-compose up --build -d
    ```

- To stop and remove the containers, along with the associated volumes:

    ```bash
    docker-compose down -v
    ```

- To view the logs of the running containers:

    ```bash
    docker-compose logs -f
    ```

- To list all Docker containers (running and stopped):

    ```bash
    docker ps -a
    ```

- To remove all stopped containers:

    ```bash
    docker container prune
    ```

- To remove all unused images:

    ```bash
    docker image prune -a
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
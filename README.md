# url-shortener

A simple URL shortener using FastAPI and Redis. The shortened URLs are based on strings of a defined length.
The shortened URLs are strings of lowercase and uppercase letters. The API also provide a rate limiter to avoid abuse.
This rate limiting is only applied to the endpoint allowing people to shorten URLs. The shortened URLs are 
available during a defined period of time.

## Installation

### On System

1. Clone the repository
2. Install the dependencies using `pip install -r requirements.txt`
3. Install Redis
4. Start the Redis server
5. Create a `.env` file based on the `.env.example` file
6. Run the server using `uvicorn app.main:app --reload`

### Using Docker

1. Clone the repository
2. Create a `.env` file based on the `.env.example` file
3. Modify if necessary the `docker-compose.yml` file (about ports exposed and volumes mounted)
4. Run `docker-compose up -d --build`

## Usage

To see how to use the API, go to the `/docs` endpoint.
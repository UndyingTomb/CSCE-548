# Pokémon Card Tracker

CSCE 548 -- N-Tier Application Project\
Student: Preston Sands

## Overview

The Pokémon Card Tracker is a multi-tier application developed for CSCE
548.\
The system allows users to browse Pokémon card sets, view individual
cards, and manage a personal inventory of collected cards.

The application demonstrates a layered architecture consisting of:

-   Client Layer
-   Service Layer (API)
-   Business Logic Layer
-   Data Layer (Database)

The client communicates with the API through HTTP requests. The API
calls the business layer, which interacts with the database to retrieve
or update card and inventory information.

------------------------------------------------------------------------

## System Architecture

Client Layer\
↓\
Service Layer (FastAPI)\
↓\
Business Logic Layer\
↓\
Data Layer (SQLite Database)

Each layer has a specific responsibility:

Client Layer -- Provides the interface used to interact with the
system.\
Service Layer -- Exposes REST API endpoints used by the client.\
Business Layer -- Contains validation and business rules.\
Data Layer -- Handles database queries and storage.

------------------------------------------------------------------------

## Technologies Used

-   Python 3
-   FastAPI
-   Uvicorn
-   SQLite
-   HTML / JavaScript (Client Interface)
-   Git / GitHub

------------------------------------------------------------------------

## Project Structure

CSCE-548 │ ├── pokemon-card-tracker │ ├── api.py │ ├── business.py │ ├──
repositories.py │ ├── client_console.py │ ├── index.html │ ├──
pokemon_cards.db │ └── requirements.txt │ ├── README.md └──
Project4_Deployment_System_Test.pdf

------------------------------------------------------------------------

## Installation

Clone the repository:

git clone https://github.com/UndyingTomb/CSCE-548.git cd
CSCE-548/pokemon-card-tracker

Create a virtual environment.

Linux / Mac:

python3 -m venv .venv source .venv/bin/activate

Windows:

python -m venv .venv .venv`\Scripts`{=tex}`\activate`{=tex}

Install dependencies:

pip install -r requirements.txt

------------------------------------------------------------------------

## Running the API Server

Start the FastAPI service:

uvicorn api:app --reload

If successful, the terminal will display:

Uvicorn running on http://127.0.0.1:8000

------------------------------------------------------------------------

## API Documentation

FastAPI automatically generates interactive API documentation.

Open in a browser:

http://127.0.0.1:8000/docs

This interface allows testing API endpoints such as:

-   GET /sets
-   GET /cards
-   GET /inventory
-   POST /inventory
-   PUT /inventory/{item_id}
-   DELETE /inventory/{item_id}

------------------------------------------------------------------------

## Running the Client

The project includes a simple web client interface.

Open the file:

pokemon-card-tracker/index.html

Or run a simple local server:

python -m http.server 5500

Then open:

http://127.0.0.1:5500/index.html

The client communicates with the API running on port 8000.

------------------------------------------------------------------------

## Database

The application uses SQLite.

Database file:

pokemon_cards.db

To inspect the database:

sqlite3 pokemon_cards.db

Example queries:

SELECT \* FROM inventory_item; SELECT \* FROM cards; SELECT \* FROM
sets;

------------------------------------------------------------------------

## Full System Test

The system was tested to verify communication between all layers:

Client → API → Business Logic → Database

The following functionality was tested:

-   Retrieve all inventory items
-   Retrieve inventory item by ID
-   Insert new inventory item
-   Update inventory item
-   Delete inventory item (optional)

Complete deployment instructions and screenshots are provided in:

Project4_Deployment_System_Test.pdf

------------------------------------------------------------------------

## Repository

GitHub Repository:

https://github.com/UndyingTomb/CSCE-548

------------------------------------------------------------------------

## Notes

This project was completed for CSCE 548 and demonstrates building a
multi-tier application using generative AI assistance.

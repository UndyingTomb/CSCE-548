Pokémon Card Tracker
Description

The Pokémon Card Tracker is a multi-tier web application developed for CSCE 548. The system allows users to browse Pokémon card sets, view individual cards, and manage a personal inventory of collected cards.

The project demonstrates an n-tier architecture consisting of a client layer, service layer, business logic layer, and data layer. These layers work together to provide a functional application for viewing and managing Pokémon card data.

The goal of the project is to demonstrate how a full stack application can be designed, deployed, and tested using modern development tools and APIs.

Table of Contents

Description

Features

Architecture

Technologies Used

Installation

Running the Application

API Usage

System Testing

Repository Structure

License

Features

The Pokémon Card Tracker provides the following functionality:

• View all Pokémon card sets
• View cards within a specific set
• Retrieve card details
• View inventory records
• Insert new inventory items
• Update existing inventory items
• Retrieve items by unique identifier

Delete functionality is optional but may also be included depending on the implementation.

Architecture

The system follows a four-layer n-tier architecture:

Client Layer
The client provides the user interface for interacting with the application.

Service Layer
The service layer hosts the API endpoints used by the client.

Business Layer
The business layer contains the application logic and processes requests.

Data Layer
The data layer interacts with the database and stores application data.

Data flows through the layers in the following order:

Client → Service Layer → Business Layer → Data Layer

Technologies Used

The project was implemented using the following technologies:

• Python
• FastAPI / Flask (depending on your implementation)
• SQLite database
• HTML / JavaScript client interface
• GitHub for version control

Installation

To install the project locally, follow the steps below.

Clone the repository:

git clone <repo-link>

Navigate into the project directory:

cd pokemon-card-tracker

Install the required Python packages:

pip install -r requirements.txt
Running the Application

Start the backend service using the following command:

uvicorn main:app --reload

The API server will start and be available at:

http://127.0.0.1:8000

Once the server is running, open the client interface in a web browser to interact with the system.

If the application loads successfully and displays card data, the system has been configured correctly.

API Usage

Example endpoints include:

Retrieve all cards

http://127.0.0.1:8000/cards

Retrieve inventory records

http://127.0.0.1:8000/inventory

Retrieve a specific inventory item

http://127.0.0.1:8000/inventory/{id}

These endpoints allow the client layer to retrieve and modify data stored in the database.

System Testing

A full system test was performed to verify that the application functions correctly across all layers.

The following operations were tested:

• Retrieve all inventory items
• Retrieve a single inventory item
• Insert a new inventory record
• Update an existing inventory record

Each test was verified through both the client interface and database queries.

Screenshots and detailed testing instructions are included in the Project4_Deployment_and_System_Test.pdf document located in the root of the repository.

Repository Structure
pokemon-card-tracker
│
├── main.py
├── api.py
├── repositories.py
├── client_console.py
├── database files
├── README.md
└── Project4_Deployment_and_System_Test.pdf

The repository contains all source code, documentation, and testing artifacts required to deploy and evaluate the project.

License

This project was developed as coursework for CSCE 548 at the University of South Carolina.

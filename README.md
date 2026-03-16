Pokémon Card Tracker

This project is a multi-tier Pokémon Card Tracker application developed for CSCE 548.

The application allows users to browse Pokémon card sets, view cards, and manage a personal inventory of collected cards.

Features

• View Pokémon card sets
• Browse cards within sets
• View card details
• Manage card inventory
• Insert new inventory records
• Update existing inventory records
• Retrieve card and inventory information through an API

Architecture

This application follows an n-tier architecture:

Client Layer – Web interface used by the user
Service Layer – API server handling HTTP requests
Business Layer – application logic
Data Layer – database storing Pokémon card information and inventory

Technologies Used

Python
FastAPI / Flask
SQLite Database
HTML / JavaScript Client Interface

Running the Project

Clone the repository:

git clone <repo-link>
cd pokemon-card-tracker

Install dependencies:

pip install -r requirements.txt

Start the API server:

uvicorn main:app --reload

Open the client interface in a web browser.

API Example

Retrieve all cards:

http://127.0.0.1:8000/cards

Retrieve inventory items:

http://127.0.0.1:8000/inventory
Deployment and System Testing

Detailed deployment instructions and system test documentation can be found in the Project4_Deployment_and_System_Test.pdf file located in the root of the repository.

Repository Structure
pokemon-card-tracker
│
├── main.py
├── api.py
├── client_console.py
├── repositories.py
├── database files
├── README.md
└── Project4_Deployment_and_System_Test.pdf
Course

University of South Carolina
CSCE 548 – Software Architecture

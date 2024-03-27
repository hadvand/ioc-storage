# IOC Storage CLI
## Overview
This is a command-line application designed to process and store malicious Indicators of Compromise (IOCs) from various data sources on the internet into a relational database. It allows users to initialize the database, add new IOCs, list all IOCs, remove specific IOCs by ID, and clear all IOCs from the database.

## Features
- Initialize database: Set up the storage database for IOCs.
- Add IOC: Add a new IOC to the database, specifying the link and its data source.
- List IOCs: View all IOCs stored in the database.
- Remove IOC: Remove a specific IOC from the database by providing its ID.
- Clear all IOCs: Delete all IOCs stored in the database.

## Requirements
- Python 3.8 or higher
- PostgreSQL database

## Installation
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies by running:

`pip install -r requirements.txt`

## Usage
Initialize Database: Run the following command to set up the database:
`python -m ioc_storage init`

Replace <database_path> with the desired path to the database file.

Add IOC: To add a new IOC to the database, use the command:

`python ioc_storage/cli.py add <link> <source>`

Replace <link> with the IOC link and <source> with the data source.

List IOCs: View all stored IOCs by executing:

`python ioc_storage/cli.py list`

Remove IOC: Remove a specific IOC by providing its ID:

`python ioc_storage/cli.py remove <ioc_id>`

Replace <ioc_id> with the ID of the IOC to be removed.

Clear all IOCs: Delete all IOCs stored in the database:

`python ioc_storage/cli.py clear --force`

## Database Schema
Separate tables for storing IP addresses and URLs.
Each IOC (URL or IP address) is stored as a separate row in the respective table.
A table containing the origin of each data source is maintained for association.
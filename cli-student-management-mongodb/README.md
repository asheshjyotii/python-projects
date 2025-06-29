## CLI based student management system using **MongoDB**

---
![banner](https://github.com/user-attachments/assets/8c2dca31-fc44-403b-b313-454802fd843f)

---
###  Project Setup

*   Initialize project folder and create virtual environment
    
*   Install dependencies: pymongo, rich, python-dotenv
    
*   Setup .gitignore and optional .env for MongoDB URI
    
*   student_management/
├── main.py
├── db.py
├── models.py
├── services.py
├── utils.py
├── cli.py
├── logger.py
└── .env

    

###  Core Functionalities (CRUD with MongoDB)

*   Connect to MongoDB using pymongo in db.py
    
*   Define student data model (name, roll, age, course, etc.)
    
*   Implement add\_student() with validation and logging
    
*   Implement view\_students() with pretty table output
    
*   Implement search\_student() by ID/roll/name
    
*   Implement update\_student() with validation and logs
    
*   Implement delete\_student() (hard delete)
    

###  Command Line Interface

*   Build interactive CLI menu in main.py
    
*   Use rich for colorful CLI output
    
*   Display messages using colors (success, error, info)
    
*   Print student list as a formatted table using rich
    

###  Logging and Debugging

*   Configure logger.py with rotating log file support
    
*   Add logging to all CRUD operations
    
*   Log both info and error levels with context
    

###  Utilities and Best Practices

*   Create reusable input validators in utils.py
    
*   Add error handling (try-except) in all critical areas
    
*   Use .env file and load secrets with dotenv
    
*   Follow modular and DRY principles
    

###  Testing and Polish

*   Manually test all functions from CLI
    
*   Validate user input edge cases
    
*   Check and clean up error handling and logs
    
*   Comment/document all public functions
    
*   Polish CLI with consistent spacing and text formatting
    

###  Optional Stretch Goals

*   Add export to CSV feature
    
*   Add pagination to student listings
    
*   Implement soft-delete (move to deleted\_students collection)
    
*   Add basic unit tests for services.py
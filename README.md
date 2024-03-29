# Server

## About the Project
This is a django app made for the Catalogue Scoring Service working hand in hand with ONDC market place.

## Installation 

To install the following app on your local system follow the steps given below:

- Install Python 3.10.7

- Install virtualenv

- Create a folder by whatever name your want to give. Example: Catalogue-Scoring

- Open the Catalogue-Scoring folder in VS Code. Open the terminal.

- Create a virtual environment: 

    ```
    virtualenv env
    ```

- Switch to the newly created environment:

    ```
    cd env/Scripts
    ```

    ```
    ./activate
    ```

- Return Back to the parent directory:

    ```
    cd ../../
    ```

- Clone the repository:

    ```
    git clone https://github.com/ONDC-Hackathon/server.git
    ```

- Change directory to newly cloned repository:

    ```
    cd server
    ```

- Build the environment using the given requirements:

    ```
    pip install -r requirements/local.txt
    ```

- Start the django server:

    ```
    python manage.py runserver
    ```
# TakeHome_RachelTanXueQi_25Feb2020

## About
A terminal application to retrieve data about the Pokemon when queried.
The program has the following functionality:
- Ability to cache the stored information locally (using a text file)
- Ability to search by Pokemon Name or ID.
- Display​ only​ the following information
    - Pokemon ID
    - Pokemon Name
    - Pokemon Type(s)
    - Pokemon Encounter Location(s) and method(s) in ​Kanto​ only
        - If there are no encounter location in Kanto, display ‘-’ Pokemon stats (speed, def, etc etc)
- If the stored information is over a week old, the data should be retrieved again from the API. If not, the data should be retrieved from the text file

### System Architecture 
![](assets/architecture_diagram.png)


### Sequence Diagram
![](assets/sequence_diagram.png)

### Design Decisions


## Project Dependencies
This project is done in `python version 3.7` with macOS.

Make you sure you have the python version installed or visit https://www.python.org/downloads/ and follow the documentation for python installation.

It uses a few open source project to run:
- certifi==2020.12.5
- chardet==4.0.0
- idna==2.10
- importlib-metadata==3.7.0
- requests==2.25.1
- rope==0.18.0
- terminaltables==3.1.0
- typing-extensions==3.7.4.3
- urllib3==1.26.3
- zipp==3.4.0


## Installation and Setup Guide
#### 1. Open Terminal 
#### 2. Change the current working directory to the location where you want the cloned directory.

#### 3. Type git clone, and then paste this git project URL.
    git clone https://github.com/racheltanxueqi/TakeHome_RachelTanXueQi_25Feb2020.git

#### 4. Once completed, run the following command to install the dependencies. 

    pip install requirements.txt

## Running the Terminal Application

### Once all the setup has been done, you may
#### 1. Go to `src/` direction

    cd src/

#### 2. Input the command line in the following format:
    
    python pokemon_app.py -p yourSearchValue

    
`yourSearchValue can be pokemon name or id`

#### 3. View the displayed information

`Sample Test result`

Input to terminal:

    python pokemon_app.py -p 121

Output in terminal:

![](assets/sample_output.png)



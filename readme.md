# OXYGEN 

OXYGEN is a [ROBOT FRAMEWORK](https://robotframework.org/) library that empowers the user to convert the results of any testing framework to the [ROBOT FRAMEWORK's test results](https://robotframework.org/robotframework/2.1.2/RobotFrameworkUserGuide.html#created-outputs). 

OXYGEN has built-in parsers for 3 testing frameworks. 

1. [JUnit](https://en.wikipedia.org/wiki/JUnit) - unit testing framework for Java.
2. [Gatling](https://en.wikipedia.org/wiki/Gatling_(software)) - load and performance testing framework.
3. [Zed Attack Proxy(ZAP)](https://www.zaproxy.org/) - web security tool. 

Additionally, users can add your own parsers for any other testing framework tools to get the results in the ROBOT FRAMEWORK's test results. 

# Table of Contents
1. [Getting Started](#getting-started)
2. [Running sample tests](#running-the-tests)
3. [Deployment](#deployment)
4. [Built With](#built-with)
5. [Contributing](#contributing)
6. [License](#license)
7. [Acknowledgments](#acknowledgments)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

OXYGEN requires `Python 3.0` or above to be installed in the environment the OXYGEN tool is to be deployed. 

Check the Python version on the command line:
```
python --version
```

Upgrade the python version if python version is less than `Python 3.0`. Follow the link for [python3](https://realpython.com/installing-python/) installation.

##### IMPORTANT!! --  OXYGEN requires the git repository to be cloned to a directory where there is no 'spaces' in the directory path.

### Installing

Clone the OXYGEN repository to the enviromnent where you want to the run the tool. Make sure that there are no 'spaces' in the directory path where the oxygen-core folder is cloned into.

Clone oxygen-core directory from the command line using:

```
git clone https://git.dev.eficode.io/scm/ox/oxygen-core.git
```
Change directory into the oxygen-core directory from command line:
```
cd oxygen-core
```
OXYGEN requires a set of dependencies to be installed. List of dependencies are liste in the [requirements](https://git.dev.eficode.io/projects/OX/repos/oxygen-core/browse/requirements.txt) file. 

Install the dependencies for OXYGEN from the command line. 

```
pip install -r requirements.txt
```

## Running sample tests

Few sample tests has been written in the directory `test`in the oxgyen-core directory. To run the sample tests run the invoke command on the command line.

```
invoke atest
```
```
invoke utest
```
```
invoke test
```
Invoke is python library which provides a cleaner way to run shell commmands from a python file. `tasks.py` is the file associated with the invoke command. 

### Break down into end to end tests
```
TO BE UPDATED
```

### And coding style tests
```
TO BE UPDATED
```
## Deployment
```
TO BE UPDATED
```
## Built With
```
TO BE UPDATED
```
## Contributing
```
TO BE UPDATED
```
## License

OXYGEN tool  was developed by Eficode Oy as part of [Testomat Project](link) with association with `SHOULD WE ADD DETAILS OF PARTNERS?`.

## Acknowledgments
TO BE UPDATED
```

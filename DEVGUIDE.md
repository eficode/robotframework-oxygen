## Oxygen developer guide

Oxygen library has inbuilt functionality to perform a unit testing for java programing([junit](https://junit.org/junit5/)), a load testing ([gatling](https://gatling.io/)) and a security testing ([ZAP](https://www.zaproxy.org/)) on robotframework. Refer oxygen [documentation](https://github.com/eficode/robotframework-oxygen) if you are trying to use junit, zap or gatling in your project.
However, if you are aiming to use any other testing tool for your business or project, oxygen provides a framework to integrate and run your testing tool on robotframework. Thus empowering you to bring all your testing tools under the same roof with a user-friendly results file.

# Getting started

## Prerequisites

1. Basics of [Python3](https://docs.python.org/3/).
2. Python virtual environment - [venv](https://docs.python.org/3/library/venv.html).
3. Basics of [robotframework](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html).
4. Basics of [robotframework-oxygen](https://github.com/eficode/robotframework-oxygen).


## What is our goal? 

Oxygen developer guide, will walk through the process of how to use the oxygen framework to integrate and run your preferred testing tool on robot framework.
The guide will use a load testing tool([locust](https://locust.io/)) as an example of how to use oxygen library to run a testing tool on robot framework. 



## What's Locust? 

[Load software testing](https://en.wikipedia.org/wiki/Load_testing) is the process of putting demand on a system and measuring its response.
The load tests in locust are defined in python files, `locustfile.py` which look like following:

```py
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(5000, 15000)

    @task
    def index_page(self):
        self.client.get("/")

```

And the output of the tests are .csv files which look like following:

```csv
"Type","Name","Request Count","Failure Count","Median Response Time","Average Response Time","Min Response Time","Max Response Time","Average Content Size","Requests/s","Failures/s","50%","66%","75%","80%","90%","95%","98%","99%","99.9%","99.99%","99.999%","100%"
"GET","/",10,0,72,75,66,89,2175,0.26,0.00,73,75,86,87,89,89,89,89,89,89,89,89
"POST","/",5,5,300,323,288,402,157,0.13,0.13,300,330,330,400,400,400,400,400,400,400,400,400
"GET","/item",24,0,80,79,67,100,2175,0.63,0.00,81,85,86,86,89,92,100,100,100,100,100,100
"None","Aggregated",39,5,81,109,66,402,1916,1.03,0.13,81,86,87,89,300,330,400,400,400,400,400,400
```

We will look into writing a `locustfile.py` and running it in the following sections. 
In the following sections we will write a handler, which is able to execute the locust tests on Robot Framework and provide the test results in user-friendly format.


## Start developing

Let's start developing by creating a `python3` virtual environment using [venv](https://docs.python.org/3/library/venv.html) and install then install the  oxygen library in it.


```bash
python3 -m venv locustenv
source locustenv/bin/activate
```

Install Oxygen by running the following:

```bash
$ pip install robotframework-oxygen
```

Robotframework will be installed into the virtual environment while doing the pip install for oxygen as robotframework is listed as a dependency for oxygen.

Now we will create a working folder for writing the Locusthandler and the unit tests. 

```bash
cd locustenv
mkdir locusthandler
cd locusthandler
```


### Writing LocustHandler and unit tests

**Create an empty python file in locustenv/locusthandler folder and name it `__init__.py`.** This is done to follow the folder structure of [python packaging](https://packaging.python.org/tutorials/packaging-projects/). Our goal is to write locusthandler code and package it so that it can be installed in any other virtual environment. 
Next we can create `locusthandler.py` to `locustenv/locusthandler` folder.

```bash
touch __init__.py 
touch locusthandler.py
```
To check if we have followed the the user guide correctly, you could verify if the folder structure in the locustenv folder and it looks like the following.  


```
> locustenv
    > bin (contains other files and sub-directories)
    > include (contains other files and sub-directories)
    > lib (contains other files and sub-directories)
    > locusthandler
        __init__.py
        locusthandler.py
    pyvenv.cfg

```

Write the following python code in the `locusthandler.py` file in the locusthandler folder.


```py
import json
import csv

from oxygen import BaseHandler
from robot.api import logger

from oxygen.errors import SubprocessException
from oxygen.utils import run_command_line, validate_path


class LocustHandler(BaseHandler):


    def run_locust(self, result_file, command, check_return_code=False, **env):
        try:
            output = run_command_line(command, check_return_code, **env)
        except SubprocessException as e:
            raise LocustHandlerException(e) ## It is best practice to raise LocustHandlerException so we know that LocustHandler caused the error.
        logger.info(output)
        logger.info('Result file: {}'.format(result_file))
        return result_file

    def parse_results(self, result_file):
        return self._transform_tests(validate_path(result_file).resolve())


    def _transform_tests(self, file):
        with open(file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            test_cases = []
            for row in reader:
                failure_count = row['Failure Count']
                success = failure_count == '0'
                keyword = {
                    'name': " | ".join(row),
                    'pass': success,
                }                               
                test_case = {
                'name': 'Locust test case',
                'keywords': [keyword]
                }
                test_cases.append(test_case)
            test_suite = {
            'name': 'Locust Scenario',
            'tests': test_cases,
            }
            return test_suite

class LocustHandlerException(Exception):
    pass
```

  Method `run_locust` can be used from robot tests, and it executes the command which runs the locust tests. It returns a path to the locust test results, which is processed by method `parse_results`, which calls `_transform_tests` function which purpose is to transfer the locust result file into a format which can be seen in the Robot Framework log files. 

  Let's create a `locustenv/locusthandler/tests` folder. Then we write there test file `test_locust.py` with following content:

```py
from unittest import TestCase

from pathlib import Path
from locusthandler import LocustHandler

class TestLocust(TestCase):
    
    def setUp(self):
        config = {'handler': 'LocustHandler', 'keyword': 'run_locust', 'tags': 'LOCUST'}
        self.handler = LocustHandler(config)
        path = Path.cwd() / 'resources/requests.csv'
        self.test_suite = self.handler.parse_results(path)

    def test_suite_has_four_cases(self):
        self.assertEqual(len(self.test_suite['tests']),4)

    def test_pass_is_true_when_failure_request_is_zero(self):
        self.assertEqual(self.test_suite['tests'][0]['keywords'][0]['pass'], True)

    def test_pass_is_false_when_failure_request_is_not_zero(self):
        self.assertEqual(self.test_suite['tests'][1]['keywords'][0]['pass'], False)
```


Next we create `locustenv/locusthandler/resources` folder and add the following .cdv data into the test data file `requests.csv`.
`requests.csv` file is created for the successful operation of the unit tests.

```csv
"Type","Name","Request Count","Failure Count","Median Response Time","Average Response Time","Min Response Time","Max Response Time","Average Content Size","Requests/s","Failures/s","50%","66%","75%","80%","90%","95%","98%","99%","99.9%","99.99%","99.999%","100%"
"GET","/",10,0,72,75,66,89,2175,0.26,0.00,73,75,86,87,89,89,89,89,89,89,89,89
"POST","/",5,5,300,323,288,402,157,0.13,0.13,300,330,330,400,400,400,400,400,400,400,400,400
"GET","/item",24,0,80,79,67,100,2175,0.63,0.00,81,85,86,86,89,92,100,100,100,100,100,100
"None","Aggregated",39,5,81,109,66,402,1916,1.03,0.13,81,86,87,89,300,330,400,400,400,400,400,400
```

Now we can run unit tests from the `locustenv/locusthandler` folder with command.  
**!! Make sure to be in the right directory before running the `test_locust.py` file.**

````bash
python -m unittest tests/test_locust.py
````

and all 3 tests should pass. 

In case of failure, please check if you have all the files as folders as following. 

```
> locustenv
    > bin (contains other files and sub-directories)
    > include (contains other files and sub-directories)
    > lib (contains other files and sub-directories)
    > locusthandler
        > resources
            requests.csv
        > tests
            test_locust.py
        __init__.py
        locusthandler.py
    pyvenv.cfg

```


### Configuring LocustHandler to Oxygen

To check if we have coded locusthandler properly,  let's open the python interpreter by running `python` from the `locustenv` directory and check that we can import the locusthandler. 

**!! Make sure to be in the right directory before starting the python interpreter.**


```bash
(locustenv) $ python
Python 3.7.7 
Type "help", "copyright", "credits" or "license" for more information.
>>> import locusthandler.locusthandler
>>>
```

Running this should not produce any errors, and we can import file `locusthandler.py` from `/locusthandler` folder we created. [Read more about packaging python projects from here.](https://packaging.python.org/tutorials/packaging-projects/) Next we can exit the python interpreter (CTRL + D).

We will now append the following lines to the end of `lib/python3.7/site-packages/oxygen/config.yml` file. This is how we configure the locusthandler to the oxygen.  

```yml
locusthandler.locusthandler:
  handler: LocustHandler
  keyword: run_locust
  tags: oxygen-locusthandler
```

Locusthandler has been configured. Now let's test your edit by running the following command in the **`locustenv` folder**:

**!! Make sure to be in the right directory**

```bash
$ python -m oxygen --version
```

You shouldn't get any errors. If you do, check that your edits are valid [YAML](https://yaml.org/) syntax.

### Install demoapp to run Locust tests against

We will now fetch, install and run a [demo application](https://github.com/robotframework/WebDemo) on your local machine to perform the locust load tests on. 

You can install the demo application on anywhere in your computer. However, its recommended to install it inside the `locustenv` to have all you project files in same folder. 

**Open up a new terminal** and run following commands:

```bash
git clone https://github.com/robotframework/WebDemo.git
cd WebDemo
python3 demoapp/server.py
```

Demo server is up and running now. You can check if the demo application is running from your browser in http://localhost:7272/. Note to replace `7272` with the port number in case the demo application is running on a different port number.

### Running Locust with LocustHandler in Robot test

Once we have installed the demo application, let's get back to the `locustenv` python virtual environment. If you have opened a new terminal for the previous step of installing the demo application you just need to go back to the old terminal where we were before installing the demo application. 


We will now install Locust load testing tool to our `locustenv` virtualenv:

```bash
pip install locust
```

Now we add `locustfile.py` file to `locustenv/locusthandler` folder which contains the commands for the performance test. Write the following code into  `locustfile.py`.

```python
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(5000, 15000)

    @task
    def index_page(self):
        self.client.get("/")
```

Let's try and run the locust test on the demo application by running the following code on the command line in the `locustenv` folder. 
**!! Make sure to be in the right directory**

```bash
locust -f locusthandler/locustfile.py --headless --host http://localhost:7272 -u 5 -r 1 --run-time 1m --csv=example
```

If the `locsutfile.py` is coded correctly, it will run load test on the demo application for 1 min and the results will be displayed on the terminal. It will also generate 3 .csv results files in the `locustenv` folder namely `example_failures.csv`,`example_stats.csv`,and `example_stats_history.csv`.

Refer locust [documentation](https://docs.locust.io/en/stable/configuration.html#command-line-options) to read more about running locust tests. 

Now let's write the robot test to run the same locust tests on the demo application on robotframework. Write `test.robot` file to `locustenv/locusthandler` folder which contains test case that runs locust from command line:

```RobotFramework

*** Settings ***
Library   oxygen.OxygenLibrary
Library   OperatingSystem

*** Variables ***
${STATS_FILE}       ${CURDIR}/../example_stats.csv
${FAILURE_FILE}     ${CURDIR}/../example_failures.csv
${HISTORY_FILE}     ${CURDIR}/../example_stats_history.csv
${LOCUSTFILEPATH}   ${CURDIR}/locustfile.py
${LOCUSTCOMMAND}    locust -f ${LOCUSTFILEPATH} --headless --host http://localhost:7272 -u 5 -r 1 --run-time 1m --csv=example

*** Keywords ***

Remove csv file
  [Arguments]             ${path}
  Remove file             ${path}
  File should not exist   ${path}

Remove csv files
  Remove csv file         ${STATS_FILE}
  Remove csv file         ${FAILURE_FILE}
  Remove csv file         ${HISTORY_FILE}


*** Test Cases ***

Performance test should pass
  [Tags]                  performance-tests
  Remove csv files
  Run Locust
    ...   ${STATS_FILE}
    ...   ${LOCUSTCOMMAND}
```

Refer [robotframework user guide](http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html) to read more about writing a robot test. 

Let' run the robot test from `locustenv` folder by using command.

**!! Make sure to be in the right directory**

```
robot --listener oxygen.listener --pythonpath . --variable LOCUSTFILEPATH:locusthandler/locustfile.py locusthandler/test.robot
```


The robot test should execute for about 60 seconds. Once the test completes, we wil observe that the locust load test results has been logged in the form of robot results in  `log.html`, `report.html` and `output.xml` files. We encourage you to open these files to see how human-friendly the robot results are are compared to the .csv  results files produced by locust. 

We have successfully reached our goal of configuring and running  the locust on robotframework using the robotframework-oxygen library. You are run any other testing tool on robotframework using robotframework-oxygen library referring to this example.


If the test case fails, check first that Oxygen's `config.yml` is correctly configured from the previous section. You can set variable `check_return_code` to "True" in order to get more specific logging:

```RobotFramework

*** Test Cases ***

Performance test should pass
  [Tags]                  performance-tests
  Remove csv files
  Run Locust
    ...   ${STATS_FILE}
    ...   ${LOCUSTCOMMAND}
    ...   check_return_code=${True}
```

This action will toggle the debugging mode of the robotframework-oxygen library in case you are hitting some kind of roadblocks, making it easy to debug the errors. Check Oxygen [Keyword documentation](https://eficode.github.io/robotframework-oxygen/) to read the more about toggling debug mode ON.

## Defining your own parameters

 The Locust test case will give results as fail, if even one request fails during the load testing. However this might not be the best way to determine was the performance test successfully or not. At certain situations, we might want to label test as passed if it passes more than certain percent of the tests. Let's implement a solution, where you can define `failure_percentage` , which is the highest percentage of failed request that is allowed in order that the test still passes.

Let's define the value of `failure_percentage` in `/lib/python3.7/site-packages/oxygen/config.yml`:

```yml
locusthandler.locusthandler:
  handler: LocustHandler
  keyword: run_locust
  tags: oxygen-locusthandler
  failure_percentage: 20
```

Let's implement function to return the failure_percentage. **Add the following code in the `LocustHandler` class in the python file `locustenv/locusthandler/locusthandler.py`**

```python
    def _get_treshold_failure_percentage(self):
        failure_percentage = self._config.get('failure_percentage', None)

        if failure_percentage is None:
            print('No failure percentage configured, defaulting to 0')
            return 0

        failure_percentage = int(failure_percentage)

        if failure_percentage > 100:
            print('Failure percentage is configured too high, maximizing at 100')
            return 100

        return failure_percentage
```
and let's use it in `_transform_tests` function in the same python file. **Make necessary changes as per the following code snippet to the `_transform_tests` function or  replace the `_transform_tests` function with the code below.**

```python
    def _transform_tests(self, file):
        with open(file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            test_cases = []
            for row in reader:
                failure_count = row['Failure Count']
                request_count = row['Request Count']
                failure_percentage = 100 * int(failure_count) / int(request_count)
                treshold_failure_percentage = self._get_treshold_failure_percentage()
                success = failure_percentage <= treshold_failure_percentage
                keyword = {
                    'name': " | ".join(row),
                    'pass': success,
                }                               
                test_case = {
                'name': 'Locust test case',
                'keywords': [keyword]
                }
                test_cases.append(test_case)
            test_suite = {
            'name': 'Locust test suite, failure percentage {}'.format(treshold_failure_percentage),
            'tests': test_cases,
            }
            return test_suite
```


Now that we have defined the failure percentage function in locusthandler, next we update the unit tests in `locusthandler/tests/test_locust.py` to test that the pass value is calculated correctly depending on the value of `failure_percentage`.

 **Make the necessary changes to  `locusthandler/tests/test_locust.py` file according to the following code snippet or replace the whole `test_locust.py` with the following code.**  

```python
from unittest import TestCase

from pathlib import Path
from locusthandler import LocustHandler

class TestLocust(TestCase):
    
    def setUp(self):
        config = {'handler': 'LocustHandler', 'keyword': 'run_locust', 'tags': 'LOCUST'}
        self.handler = LocustHandler(config)
        path = Path.cwd() / 'resources/requests.csv'
        self.test_suite = self.handler.parse_results(path)

    def test_suite_has_four_cases(self):
        self.assertEqual(len(self.test_suite['tests']),4)

    def test_pass_is_true_when_failure_request_percentage_is_below_default_value(self):
        config = config = {'handler': 'LocustHandler', 'keyword': 'run_locust', 'tags': 'LOCUST', 'failure_percentage': '10'}
        handler = LocustHandler(config)
        path = Path.cwd() / 'resources/requests.csv'
        test_suite = handler.parse_results(path)
        self.assertEqual(self.test_suite['tests'][0]['keywords'][0]['pass'], True)

    def test_pass_is_true_when_failure_request_percentage_is_default_value(self):
        self.assertEqual(self.test_suite['tests'][2]['keywords'][0]['pass'], True)

    def test_pass_is_false_when_failure_request_percentage_is_above_default_value(self):
        self.assertEqual(self.test_suite['tests'][1]['keywords'][0]['pass'], False)

    def test_failure_percentage_max_amount_is_one_hundred(self):
        config = config = {'handler': 'LocustHandler', 'keyword': 'run_locust', 'tags': 'LOCUST', 'failure_percentage': '101'}
        handler = LocustHandler(config)
        failure_percentage = handler._get_treshold_failure_percentage()
        self.assertEqual(failure_percentage, 100)
```

Let's verify if the changes made to the `test_locust.py` file is correct by running the tests **from `locustenv/locusthandler` folder** with the following command:

**!! Make sure to be in the right directory before running the tests**

````bash
python -m unittest tests/test_locust.py
````

We should be able to run all the 5 tests if everything is done correctly.

And we can also try out the robot tests using the new .yaml configuration. Run the tests **from `locustenv` folder** by using command.

**!! Make sure to be in the right directory before running the tests**

```bash
robot --listener oxygen.listener --pythonpath . --variable LOCUSTFILEPATH:locusthandler/locustfile.py locusthandler/test.robot
```

We should be able to run the robot tests successfully now. It's encouraged to check the robot result files `log.html` and `report.html` to see the difference in the results before and after defining our own parameters. 

## Adding failure percentage as an robot test parameter

Our current solution works quite nicely, but let's imagine a situation where we run the performance tests on different parts of the software, where we want to determine different values for `failure_percentage`. 

Let's change the functionality of `locusthandler/locusthandler.py`. Replace the code in the `locusthandler.py` file with the following code.

```python
import json
import csv

from oxygen import BaseHandler
from robot.api import logger

from oxygen.errors import SubprocessException
from oxygen.utils import run_command_line, validate_path


class LocustHandler(BaseHandler):

    def run_locust(self, result_file, command, check_return_code=False, failure_percentage=None, **env):
        try:
            output = run_command_line(command, check_return_code, **env)
        except SubprocessException as e:
            raise LocustHandlerException(e) ## It is best practice to raise LocustHandlerException so we know that LocustHandler caused the error.
        logger.info(output)
        logger.info('Result file: {}'.format(result_file))
        dictionary = dict()
        dictionary['result_file'] = result_file
        dictionary['failure_percentage'] = failure_percentage
        return dictionary

    def parse_results(self, dictionary):
        result_file = dictionary['result_file']
        failure_percentage = dictionary['failure_percentage']
        if failure_percentage is None:
            failure_percentage = self._config.get('failure_percentage', None)
        treshold_failure_percentage = self._get_treshold_failure_percentage(failure_percentage)
        return self._transform_tests(validate_path(result_file).resolve(), treshold_failure_percentage)

    def _transform_tests(self, file, treshold_failure_percentage):
        with open(file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            test_cases = []
            for row in reader:
                failure_count = row['Failure Count']
                request_count = row['Request Count']
                failure_percentage = 100 * int(failure_count) / int(request_count)
                success = failure_percentage <= treshold_failure_percentage
                keyword = {
                    'name': " | ".join(row),
                    'pass': success,
                }                               
                test_case = {
                'name': 'Locust test case',
                'keywords': [keyword]
                }
                test_cases.append(test_case)
            test_suite = {
            'name': 'Locust test suite, failure percentage {}'.format(treshold_failure_percentage),
            'tests': test_cases,
            }
            return test_suite

    def _get_treshold_failure_percentage(self, failure_percentage):
        if failure_percentage is None:
            print('No failure percentage configured, defaulting to 0')
            return 0

        failure_percentage = int(failure_percentage)

        if failure_percentage > 100:
            print('Failure percentage is configured too high, maximizing at 100')
            return 100

        return failure_percentage

class LocustHandlerException(Exception):
    pass
```

Notice that we return an dictionary object instead of result file in the `run_locust` method. This way we can use the `failure_percentage` value if it is defined. If it's not defined we will use the value what is defined in `/lib/python3.7/site-packages/oxygen/config.yml`. 

Now we can rewrite the robot tests in `locusthandler/test.robot`, one assigns the value from the parameter and the second test doesn't.

Replace the `Test Cases` part of the `test.robot` file with the following code. Remember to follow [robot code syntax](http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#creating-test-cases) while editing the robot file. 

```RobotFramework
*** Test Cases ***

Critical performance test
  [Tags]                  performance-tests
  Remove csv files
  Run Locust
    ...   ${STATS_FILE}
    ...   ${LOCUSTCOMMAND}
    ...   failure_percentage=${1}


Normal performance test
  [Tags]                  performance-tests
  Remove csv files
  Run Locust
    ...   ${STATS_FILE}
    ...   ${LOCUSTCOMMAND}
```

In this case the `Critical performance test` could be a performance test for a system where the consequences of failure is much larger: Thus we define the failure_percentage to 1%. In the `Normal performance test` we use the value that is defined in the `/lib/python3.7/site-packages/oxygen/config.yml`.

Run the tests in `locustenv/` folder with the command:

**!! Make sure to be in the right directory before running the tests**

```bash
robot --listener oxygen.listener --pythonpath . --variable LOCUSTFILEPATH:locusthandler/locustfile.py locusthandler/test.robot
```

However now when you run the unit tests from `locusthandler/` folder they fail:

```bash
python -m unittest tests/test_locust.py
```

Because we changed the functionality to use dictionary instead of result file path. To fix that, let's write a function, `dictionary_with_result_file` in the `TestLocust` class at `tests/test_locust.py` file. We will also update the `setUp` function to match the `dictionary_with_result_file` function. 
 
```python
    def dictionary_with_result_file(self):
        path = Path.cwd() / 'resources/requests.csv'
        dictionary = dict()
        dictionary['result_file'] = path
        return dictionary
```
```python

    def setUp(self):
        config = {'handler': 'LocustHandler', 'keyword': 'run_locust', 'tags': 'LOCUST'}
        self.handler = LocustHandler(config)
        dictionary = self.dictionary_with_result_file()
        dictionary['failure_percentage'] = None
        self.test_suite = self.handler.parse_results(dictionary)
```

and run tests again from the `locusthandler/` folder.
Still two test cases fail. This is because the `_get_treshold_failure_percentage` has an argument now instead of reading the value from the config. Let's update the failing test cases by replacing `test_pass_is_true_when_failure_request_percentage_is_below_default_value` and `test_failure_percentage_max_amount_is_one_hundred` functions in `tests/test_locust.py` file. 

```python
    def test_pass_is_true_when_failure_request_percentage_is_below_default_value(self):
        config = config = {'handler': 'LocustHandler', 'keyword': 'run_locust', 'tags': 'LOCUST'}
        handler = LocustHandler(config)
        dictionary = self.dictionary_with_result_file()
        dictionary['failure_percentage'] = 10
        test_suite = handler.parse_results(dictionary)
        self.assertEqual(self.test_suite['tests'][0]['keywords'][0]['pass'], True)
```
```python

    def test_failure_percentage_max_amount_is_one_hundred(self):
        failure_percentage = self.handler._get_treshold_failure_percentage(101)
        self.assertEqual(failure_percentage, 100)
```

Now all tests should pass, when running the following command from the `locusthandler/` directory.

```bash
python -m unittest tests/test_locust.py
```

We will be able to run all the 5 tests without fail now.

Let's add two more test cases to the  `tests/test_locust.py` so that the `failure_precentage` is set correctly from the parameter or config file.

```python
    def test_parse_results_takes_failure_percentage_from_parameter_prior_to_config(self):
        config = {'handler': 'LocustHandler', 'keyword': 'run_locust', 'tags': 'LOCUST', 'failure_percentage': '70'}
        self.handler = LocustHandler(config)
        dictionary = self.dictionary_with_result_file()
        dictionary['failure_percentage'] = 75
        test_suite = self.handler.parse_results(dictionary)
        self.assertEqual(test_suite['name'], 'Locust test suite, failure percentage 75')

    def test_parse_results_takes_failure_percentage_correctly_from_config(self):
        config = {'handler': 'LocustHandler', 'keyword': 'run_locust', 'tags': 'LOCUST', 'failure_percentage': '70'}
        self.handler = LocustHandler(config)
        dictionary = self.dictionary_with_result_file()
        dictionary['failure_percentage'] = None
        test_suite = self.handler.parse_results(dictionary)
        self.assertEqual(test_suite['name'], 'Locust test suite, failure percentage 70')
```

We will have 7 unit tests now. Running the unit tests from the `locusthandler/` folder with `python -m unittest tests/test_locust.py` command, we can notice that all 7 tests are run successfully.  We have completed an LocustHandler with unit tests which test the most important functionalities.



## How to package your project

Let's package our project in the same virtual environment `locustenv` . 
Check [python packaging documentation](https://packaging.python.org/tutorials/packaging-projects/) to learn about it in detail. Python packaging is highly dependent on the folder and file structure, so we have to make sure all the files mentioned in the [python packaging user guide](https://packaging.python.org/tutorials/packaging-projects/) are present in our project folder. 

To match, the python packaging requirements, let's create files `setup.py` `README.md` to the `locustenv/` folder. 

Run the terminal command from `locusthandler/` directory:

```bash
touch setup.py
touch README.md
```

Let's add the following code to `setup.py` in the `locustenv/` directory. 

```python
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python_package_for_locusthandler", # Replace with your package name
    version="0.0.1",
    author="Example Author",                 # Replace with your name
    author_email="author@example.com",       # Replace with your mail id
    description="A small example package",   # Add the package description
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",    # Add your project github repo
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
           'robotframework-oxygen>=0.1',
           'locust>=1.1',
      ],
)
```

Note that, we have given **robotframework-oxygen** and **locust** as pre-requisites for the package. Which means that, when we install the handler package in another environment, the pre-requisites will also be installed. 

Whatever details about your handler needed to be to mentioned can be added in `README.md` in the `locustenv/` folder. For now we will leave `README.md` empty.


Before packaging the handler let's cross check the `locustenv/` folder to verify if you have followed all the steps correctly. 


```
> locustenv
    > bin (contains other files and sub-directories)
    > include (contains other files and sub-directories)
    > lib (contains other files and sub-directories)
    > locusthandler
        > resources
            requests.csv
        > tests
            test_locust.py
        __init__.py
        locustfile.py
        locusthandler.py
        test.robot
    example_failures.csv
    example_stats.csv
    example_stats_history.csv
    log.html
    output.xml
    pyvenv.cfg
    README.me
    report.html
    setup.py 

```

Check if you have all the folders listed above in your `locustenv/` directory.  If not, you should scroll up and check the user-guide to see where you have missed the files. (You might have some `__pycache__` folders in addition to the folders listed above. Let's ignore them for now.)

We will now package the handler created by running the following terminal commands from `locustenv/` folder.

```bash
pip install wheel
python setup.py bdist_wheel
```

Running this command will create 3 new folders namely `build/`, `bdist/` and `python_package_for_locusthandler.egg-info/` in the `locustenv/` directory.  

**If you were to create the package again by running the above commands, make sure you delete these 3 folders before re-building the package.** 


## Verifying the handler packaging 

 Next we will ensure that the installation works by creating another virtualenv. 
 
 Open up another terminal,  and go backwards with `cd ..` same path where `locustenv/` is and run following commands:

```bash
python3 -m venv packagenv
source packagenv/bin/activate
pip install locustenv/dist/python_package_for_locusthandler-0.0.1-py3-none-any.whl
```

You should now have a version of locusthandler in your `packagenv` python virtual environment. Let's verify this by opening python interpreter:

```bash
$ python
Python 3.7.7 
Type "help", "copyright", "credits" or "license" for more information.
>>> import locusthandler.locusthandler
>>>
```

Which should succeed. Exit interpreter with CTRL+ D. 

Next we can append following code to the `packagenv/lib/python3.7/site-packages/oxygen/config.yml` file:

```yml
locusthandler.locusthandler:
  handler: LocustHandler
  keyword: run_locust
  tags: oxygen-locusthandler
  failure_percentage: 20
```
**Remember to follow the [syntax of .yml files](https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html).**

 Next let's run the robot test case to make sure that it works. Next let's copy `test.robot` and `locustfile.py` files from `locustenv/locusthandler/`to `packagenv/` folder so that we can run them easily from our new environment. 
 
 Replace the `Variables` section in the `test.robot` file with the following code.

```RobotFramework
*** Variables ***
${STATS_FILE}       ${CURDIR}/example_stats.csv
${FAILURE_FILE}     ${CURDIR}/example_failures.csv
${HISTORY_FILE}     ${CURDIR}/example_stats_history.csv
${LOCUSTFILEPATH}   locustfile.py
${LOCUSTCOMMAND}    locust -f ${LOCUSTFILEPATH} --headless --host http://localhost:7272 -u 5 -r 1 --run-time 1m --csv=example
```

Now we will be able to run the robot tests **from `packagenv/` folder** with command:
**!! Make sure to be in the right directory before running the robot tests**

```
robot --listener oxygen.listener --pythonpath . test.robot
```

And the tests should run normally creating the locust results files(`example_failures.csv`,`example_stats.csv` and `example_stats_history.csv`) and robot results files(`log.html`,`report.html`and`output.xml`) in the `packagenv/` folder. It's recommended to open results files `log.html`and`report.html` on your browser, to see how your handler results look like.

 Now we have verified that the packaging has been done correctly.  


## Improving the test result report

Our locusthandler works fine, but we could make the test results more clear in the robot results. Let's replaced the `transform_tests` function in the `locusthandler.py` file to make more clear test suite and keyword names, and show the performance test results as keyword messages:

```py
    def _transform_tests(self, file, treshold_failure_percentage):
        with open(file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            test_cases = []
            for row in reader:
                messages = []
                for element in row:
                    messages.append('{}: {}'.format(element, row[element]))
                failure_count = row['Failure Count']
                request_count = row['Request Count']
                failure_percentage = 100 * int(failure_count) / int(request_count)
                success = failure_percentage <= treshold_failure_percentage
                keyword_name = '{} requests with {} failures '.format(request_count, failure_count)
                keyword = {
                    'name': keyword_name,
                    'pass': success,
                    'messages': messages,
                }
                type_of_request = row['Type']
                path = row['Name']
                test_case_name = 'Testing {} requests to path {}'.format(type_of_request, path)
                if path == 'Aggregated':
                    test_case_name = 'Aggregated results of all Locust test cases:'              
                test_case = {
                'name': test_case_name,
                'keywords': [keyword]
                }
                test_cases.append(test_case)
            test_suite = {
            'name': 'Locust test case, failure percentage {}'.format(treshold_failure_percentage),
            'tests': test_cases,
            }
            return test_suite
```

Now run the robot tests again **from `locustenv/` folder** with the following command.
**!! Make sure to be in the right directory before running the robot tests**

```bash
robot --listener oxygen.listener --pythonpath . --variable LOCUSTFILEPATH:locusthandler/locustfile.py locusthandler/test.robot
```

And see the new test format in the generated `log.html` file on your browser.

Let's run the unit tests **from `locustenv/locusthandler` folder**:
**!! Make sure to be in the right directory**

```bash
python -m unittest tests/test_locust.py
```

 We notice that two fail because we changed the name of test suite. Let's update the assert statements of the failing tests by replacing the `test_parse_results_takes_failure_percentage_from_parameter_prior_to_config` and `test_parse_results_takes_failure_percentage_correctly_from_config` functions in `locustenv/locusthandler/tests/test_locust.py` file.

```py
    def test_parse_results_takes_failure_percentage_from_parameter_prior_to_config(self):
        config = {'handler': 'LocustHandler', 'keyword': 'run_locust', 'tags': 'LOCUST', 'failure_percentage': '70'}
        self.handler = LocustHandler(config)
        dictionary = self.dictionary_with_result_file()
        dictionary['failure_percentage'] = 75
        test_suite = self.handler.parse_results(dictionary)
        self.assertEqual(test_suite['name'], 'Locust test case, failure percentage 75')
```
```py
    def test_parse_results_takes_failure_percentage_correctly_from_config(self):
        config = {'handler': 'LocustHandler', 'keyword': 'run_locust', 'tags': 'LOCUST', 'failure_percentage': '70'}
        self.handler = LocustHandler(config)
        dictionary = self.dictionary_with_result_file()
        dictionary['failure_percentage'] = None
        test_suite = self.handler.parse_results(dictionary)
        self.assertEqual(test_suite['name'], 'Locust test case, failure percentage 70')
```
 Let's re-run the unit tests **from `locustenv/locusthandler` folder** with `python -m unittest tests/test_locust.py`.

We should have all the 7 tests successfully executed. Now we are done! 

# Teardown

If you wish to delete your virtual environment do following: 

```
deactivate
rm -rf locustenv
```

And shutdown the demo-app which was tested by locust with CTRL+D. You can also deactivate and delete `packagenv` virtual environment if you wish.
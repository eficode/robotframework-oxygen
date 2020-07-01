## Oxygen developer guide

This is a developer guide for Oxygen. We will write a handler for [https://locust.io/](https://locust.io/), which is a performance testing tool.

# Getting started

## Prerequisites

Python 3


## Start developing

Let's create a virtual environment and install oxygen.


```
python3 -m venv locustenv
source locustenv/bin/activate
```

Install Oxygen by running the following:
```
$ pip install robotframework-oxygen
```

Let's start developing by creating a working folder
````
cd locustenv
mkdir locust
cd locust
````


### Writing LocustHandler and unit tests

Let's create `__init__.py`  to our `locustenv/locust` folder. Next we can write `locusthandler.py` with following content:

```
import json
import csv

from oxygen import BaseHandler
from robot.api import logger

from oxygen.errors import SubprocessException
from oxygen.utils import run_command_line, validate_path


class LocustHandler(BaseHandler):


    def run_locust(self, result_file, command, check_return_code=False, **env):
        '''Run Locust performance testing tool with command
        ``command``.

        See documentation for other arguments in \`Run Gatling\`.
        '''
        try:
            output = run_command_line(command, check_return_code, **env)
        except SubprocessException as e:
            raise LocustHandlerException(e)
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
                    'tags': [],
                    'messages': [],
                    'teardown': [],
                    'keywords': [],
                }                               
                test_case = {
                'name': 'Locust test case',
                'tags': [],
                'setup': [],
                'teardown': [],
                'keywords': [keyword]
                }
                test_cases.append(test_case)
            test_suite = {
            'name': 'Locust Scenario',
            'tags': self._tags,
            'setup': [],
            'teardown': [],
            'suites': [],
            'tests': test_cases,
            }
            return test_suite

class LocustHandlerException(Exception):
    pass
```

  Let's create a `tests` folder in `locustenv/locust` . Then we write test file `test_locust.py` with following content:

```
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


next we create `resources` folder in `locustenv/locust` and add there test data file `requests.csv` which has the following:
```
"Type","Name","Request Count","Failure Count","Median Response Time","Average Response Time","Min Response Time","Max Response Time","Average Content Size","Requests/s","Failures/s","50%","66%","75%","80%","90%","95%","98%","99%","99.9%","99.99%","99.999%","100%"
"GET","/",10,0,72,75,66,89,2175,0.26,0.00,73,75,86,87,89,89,89,89,89,89,89,89
"POST","/",5,5,300,323,288,402,157,0.13,0.13,300,330,330,400,400,400,400,400,400,400,400,400
"GET","/item",24,0,80,79,67,100,2175,0.63,0.00,81,85,86,86,89,92,100,100,100,100,100,100
"None","Aggregated",39,5,81,109,66,402,1916,1.03,0.13,81,86,87,89,300,330,400,400,400,400,400,400
```

Now we can run unit tests from the `locustenv/locust` folder with command 

````
python -m unittest tests/test_locust.py
````

and all 3 tests should pass.


### Configuring LocustHandler to Oxygen

Let's open the python interpreter from the `locustenv` directory and check that we can import the locusthandler:

```
python
import locust.locusthandler
```

running this should not produce any errors, and we can import file `locusthandler.py` from `/locust` folder we created. [Read more about packaging python projects from here.](https://packaging.python.org/glossary/#term-import-package) Next we can exit the python intepreter (CTRL + D) and write following lines to the end of `lib/python3.7/site-packages/oxygen/config.yml`:

```
locust.locusthandler:
  handler: LocustHandler
  keyword: run_locust
  tags: oxygen-locusthandler
```

### Install demoapp to run tests against

[Next we we install and run demo-app that we run the locust tests against.](https://github.com/robotframework/WebDemo)

Open up another terminal and run following commands:


```
git clone https://github.com/robotframework/WebDemo.git
cd WebDemo
python3 -m venv myenv
source myenv/bin/activate

pip install -r requirements.txt
python demoapp/server.py
```

### Running Locust with LocustHandler in Robot test

First we install locust to our locustenv virtualenv:

```
pip install locust
```

Then we add `locustfile.py` file to `locustenv/locust` folder which contains the commands for the performance test:

```
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(5000, 15000)

    @task
    def index_page(self):
        self.client.get("/")

```



Let's write `locustenv/locust/test.robot` file which contains test case that runs locust from command line:

```
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

My Locust test
  [Tags]                  LOCUST_ROBOT_TAG
  Remove csv files
  run_locust
    ...   ${STATS_FILE}
    ...   ${LOCUSTCOMMAND}
```


 We can run the test from `locustenv` folder by using command

```
robot --listener oxygen.listener --pythonpath . --variable LOCUSTFILEPATH:locust/locustfile.py locust/test.robot
```

The test should execute for about 60 seconds. After this you can see the statistics of the performance tests in `log.html` and `report.html`. 


If the test case fails, you can set variable `check_return_code` to "True" in order to get more specific logging:

```
*** Test Cases ***

My Locust test
  [Tags]                  LOCUST_ROBOT_TAG
  Remove csv files
  run_locust
    ...   ${STATS_FILE}
    ...   ${LOCUSTCOMMAND}
    ...   check_return_code=${True}
```


## Defining your own parameters

In our first solution the Locust test case will fail if even one request fails during the performance testing. However this might not be the best way to determine was the performance test successfull or not. Let's implement a solution, where you can define `failure_percentage` , which is the highest percentage of failed request that is allowed in order that the test still passes.

Let's define define the value of `failure_percentage` in `/lib/python3.7/site-packages/oxygen/config.yml`:

```
locust.locusthandler:
  handler: LocustHandler
  keyword: run_locust
  tags: oxygen-locusthandler
  failure_percentage: 10
```


Let's implement function, which returns the failure_percentage to `locustenv/locust/locusthandler.py`:

```
    def _get_treshold_failure_percentage(self):
        failure_percentage = self._config.get('failure_percentage', None)

        if failure_percentage is None:
            print('No failure percentage configured, defaulting to 10')
            return 10

        failure_percentage = int(failure_percentage)

        if failure_percentage > 100:
            print('Failure percentage is configured too high, maximizing at 100')
            return 100

        return failure_percentage
```
and let's use it in `_transform_tests` function:

```
    def _transform_tests(self, file):
        with open(file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            test_cases = []
            for row in reader:
                failure_count = row['Failure Count']
                request_count = row['Request Count']
                failure_percentage = 100 * int(failure_count) / int(request_count)
                success = failure_percentage <= self._get_treshold_failure_percentage()
                keyword = {
                    'name': " | ".join(row),
                    'pass': success,
                    'tags': [],
                    'messages': [],
                    'teardown': [],
                    'keywords': [],
                }                               
                test_case = {
                'name': 'Locust test case',
                'tags': [],
                'setup': [],
                'teardown': [],
                'keywords': [keyword]
                }
                test_cases.append(test_case)
            test_suite = {
            'name': 'Locust Scenario',
            'tags': self._tags,
            'setup': [],
            'teardown': [],
            'suites': [],
            'tests': test_cases,
            }
            return test_suite
```

Let's update the tests to match the current functionality. Let's start by defining new data set in `locustenv/locust/resources/requests.csv`:

```
"Type","Name","Request Count","Failure Count","Median Response Time","Average Response Time","Min Response Time","Max Response Time","Average Content Size","Requests/s","Failures/s","50%","66%","75%","80%","90%","95%","98%","99%","99.9%","99.99%","99.999%","100%"
"GET","/",10,0,72,75,66,89,2175,0.26,0.00,73,75,86,87,89,89,89,89,89,89,89,89
"POST","/",5,5,300,323,288,402,157,0.13,0.13,300,330,330,400,400,400,400,400,400,400,400,400
"GET","/item",30,3,80,79,67,100,2175,0.63,0.00,81,85,86,86,89,92,100,100,100,100,100,100
"None","Aggregated",39,5,81,109,66,402,1916,1.03,0.13,81,86,87,89,300,330,400,400,400,400,400,400
```

now we can update the unit tests in `locust/tests/test_locust.py`:

```
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

    def test_pass_is_true_when_failure_request_percentage_is_zero(self):
        self.assertEqual(self.test_suite['tests'][0]['keywords'][0]['pass'], True)

    def test_pass_is_true_when_failure_request_percentage_is_ten(self):
        self.assertEqual(self.test_suite['tests'][2]['keywords'][0]['pass'], True)

    def test_pass_is_false_when_failure_request_percentage_is_above_ten(self):
        self.assertEqual(self.test_suite['tests'][1]['keywords'][0]['pass'], False)

    def test_failure_percentage_is_ten_by_default(self):
        failure_percentage = self.handler._get_treshold_failure_percentage()
        self.assertEqual(failure_percentage, 10)

    def test_failure_percentage_max_amount_is_one_hundred(self):
        config = config = {'handler': 'LocustHandler', 'keyword': 'run_locust', 'tags': 'LOCUST', 'failure_percentage': '101'}
        self.handler = LocustHandler(config)
        failure_percentage = self.handler._get_treshold_failure_percentage()
        self.assertEqual(failure_percentage, 100)
```

Now the unit tests should pass, run the tests from `locustenv/locust` folder with command:

````
python -m unittest tests/test_locust.py
````

And we can also try out the robot tests using the new .yaml configuration. Run the tests from `locustenv` folder by using command

```
robot --listener oxygen.listener --pythonpath . --variable LOCUSTFILEPATH:locust/locustfile.py locust/test.robot
```

## Adding failure percentage as an robot test parameter

Our current solution works quite nicely, but let's imagine a situation where we run the performance tests on different parts of the software, where we wan't to determine different values for the amount of `failure_percentage`. 

Let's change the functionality of `locust/locusthandler.py`:

```
import json
import csv

from oxygen import BaseHandler
from robot.api import logger

from oxygen.errors import SubprocessException
from oxygen.utils import run_command_line, validate_path


class LocustHandler(BaseHandler):

    def run_locust(self, result_file, command, check_return_code=False, failure_percentage=None, **env):
        '''Run Locust performance testing tool with command
        ``command``.

        See documentation for other arguments in \`Run Gatling\`.
        '''
        try:
            output = run_command_line(command, check_return_code, **env)
        except SubprocessException as e:
            raise LocustHandlerException(e)
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
        print('treshold is: {}'.format(treshold_failure_percentage))
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
                    'tags': [],
                    'messages': [],
                    'teardown': [],
                    'keywords': [],
                }                               
                test_case = {
                'name': 'Locust test case',
                'tags': [],
                'setup': [],
                'teardown': [],
                'keywords': [keyword]
                }
                test_cases.append(test_case)
            test_suite = {
            'name': 'Locust Scenario',
            'tags': self._tags,
            'setup': [],
            'teardown': [],
            'suites': [],
            'tests': test_cases,
            }
            return test_suite

    def _get_treshold_failure_percentage(self, failure_percentage):
        if failure_percentage is None:
            print('No failure percentage configured, defaulting to 10')
            return 10

        failure_percentage = int(failure_percentage)

        if failure_percentage > 100:
            print('Failure percentage is configured too high, maximizing at 100')
            return 100

        return failure_percentage

class LocustHandlerException(Exception):
    pass
```

Notice that we return an dictionary object instead of result file in the `run_locust` method. This way we can use the `failure_percentage` value if it is defined. If it's not defined we will use the value what is defined in `/lib/python3.7/site-packages/oxygen/config.yml`. Now we can rewrite the robot tests in `locust/test.robot`, one assigns the value from the parameter and the second test doesn't: 

```
*** Test Cases ***

Critical test
  [Tags]                  LOCUST_ROBOT_TAG
  Remove csv files
  run_locust
    ...   ${STATS_FILE}
    ...   ${LOCUSTCOMMAND}
    ...   failure_percentage=${1}


Normal test
  [Tags]                  LOCUST_ROBOT_TAG
  Remove csv files
  run_locust
    ...   ${STATS_FILE}
    ...   ${LOCUSTCOMMAND}
```

In this case the `Critical test` could be a performance test for a system where the consequences of failure is much larger: Thus we define the failure_percentage to 1%. In the `Normal test` we use the value that is defined in the `/lib/python3.7/site-packages/oxygen/config.yml`.

Run the tests in `locustenv/` folder with 

```
robot --listener oxygen.listener --pythonpath . --variable LOCUSTFILEPATH:locust/locustfile.py locust/test.robot
```

However now when you run the unit tests from `locust/` folder they fail:

```
python -m unittest tests/test_locust.py
```

because we changed the functionality to use dictionary instead of result file path. Let's update the test case setup:

```
    def setUp(self):
        config = {'handler': 'LocustHandler', 'keyword': 'run_locust', 'tags': 'LOCUST'}
        self.handler = LocustHandler(config)
        path = Path.cwd() / 'resources/requests.csv'
        dictionary = dict()
        dictionary['result_file'] = path
        dictionary['failure_percentage'] = None
        self.test_suite = self.handler.parse_results(dictionary)
```

and run tests again. Still two test cases fail. This is because the `_get_treshold_failure_percentage` has an argument now instead of reading the value from the config. Let's update the test cases: 

```
    def test_failure_percentage_is_ten_by_default(self):
        failure_percentage = self.handler._get_treshold_failure_percentage(None)
        self.assertEqual(failure_percentage, 10)

    def test_failure_percentage_max_amount_is_one_hundred(self):
        failure_percentage = self.handler._get_treshold_failure_percentage(101)
        self.assertEqual(failure_percentage, 100)
```

Now all tests should pass.



## How to package your project

Let's package our project in the same virtual environment . Add necessary files to `locustenv/locust` folder and follow the packaging steps defined in this [tutorial](https://packaging.python.org/). 

NOTE: You can use `pip install` instead of `python pip install` because you are already inside active venv.



# Teardown

If you wish to delete your virtual environment do following: 

```
deactivate
rm -rf locustenv
```

And shutdown the demo-app which was tested by locust with CTRL+D. You can also deactivate and delete `myenv` virtual environment if you wish.
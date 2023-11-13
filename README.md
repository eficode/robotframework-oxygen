# Oxygen

Oxygen is a [Robot Framework](https://robotframework.org/) tool that empowers the user to convert the results of any testing tool or framework to [Robot Framework's reporting](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#screenshots). This consolidates all test reporting together regardless of tools used.

Oxygen has built-in support for three testing frameworks: [JUnit](https://junit.org/junit5/), [Gatling](https://gatling.io/), and [Zed Attack Proxy (ZAP)](https://www.zaproxy.org/).

Oxygen is designed to be extensible. Users can create their own *handlers* for other testing framework or tools to transform their reporting into the Robot Framework's `log.html` and `report.html`.

# Table of Contents
1. [Installation](#installation)
1. [Keyword documentation](#keyword-documentation)
1. [Usage](#usage)
1. [Developing Oxygen](#developing-oxygen)
1. [License](#license)
1. [Acknowledgements](#acknowledgments)

# Installation

To install Oxygen, run the following:
```
$ pip install robotframework-oxygen
```

## Pre-requisites

- Oxygen is supported on Windows, Linux and MacOS
- [Python 3.10](http://python.org) or above
- [pip](https://pypi.python.org/pypi/pip) for easy installation
- [Robot Framework](http://robotframework.org)
- [additional dependencies](requirements.txt)

To check the Python version on the command line, run:
```
$ python --version
```

# Keyword documentation

[Keyword Documentation](http://eficode.github.io/robotframework-oxygen/)

# Usage

## Example: Robot Framework running other test tools

Main usage scenario for Oxygen is the ability to write acceptance test cases that run your tests in other test tools and integrate the resulting test report as part of Robot Framework's. This means you are able to run all of your testing from Robot Framework and thus having all test reporting consolidated together.

After installing Oxygen, it can be used in the Robot Framework suite to write test cases. For example, to build acceptance tests that run different sets of JUnit tests:

``` RobotFramework
*** Settings ***
Library    oxygen.OxygenLibrary

*** Test cases ***

JUnit unit tests should pass
    [Tags]    testset-1
    Run JUnit    path/to/mydir/results.xml    java -jar junit.jar --reports-dir=path/to/mydir

JUnit integration tests should pass
    [Tags]    testset-2
    Run JUnit    path/to/anotherdir/results.xml    java -jar junit.jar --reports-dir=path/to/anotherdir
```

Then, run the suite by providing Oxygen as [a listener](http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#listener-interface):

```
$ robot --listener oxygen.listener my_tests.robot
```

Opening the Robot Framework `log.html` and `report.html`, you should see that test case `JUnit unt tests should pass` has been replaced by Oxygen with test cases matching with what is in the `path/to/mydir/results.xml` JUnit report file. Similarly, test case `JUnit integration tests should pass` has been replaced with results from `path/to/anotherdir/results.xml`; each JUnit test case with its relevant information has a counterpart in the `log.html`. Each JUnit test case is also tagged with the tags from the original Robot Framework test case.

The example above, for the brevity, shows incomplete commands to run JUnit tool from command line. Please refer to [keyword documentation](#keyword-documentation) for more detailed documentation about keyword's arguments, as well as documentation for [Gatling](https://gatling.io/) and [ZAP](https://www.zaproxy.org/) related keywords. And, of course, refer to the particular tool documentation as well.

## Using from command line

In case where you want to run your other testing tools separately, but yet combine results into unified Robot Framework `log.html` and `report.html`, you can use Oxygen's command line interface to convert single result file to single corresponding Robot Framework `output.xml`:

```
$ python -m oxygen oxygen.junit my_junit_results.xml
```

As a convention, the resulting Robot Framework xml file will be named by adding a suffix to the end. In the example above, the resulting Robot Framework xml file would be named `my_junit_results_robot_output.xml`.

**Note** that resulting xml file will also be created at the same location as the original result file. Therefore, when original result files are in another directory:

```
$ python -m oxygen oxygen.gatling path/to/results.log
```

Then `results_robot_output.xml` will be created under `path/to/`.

## Extending Oxygen: writing your own handler

### [Read the developer guide on how to write your own handler](DEVGUIDE.md)

You might also want to look at [specification for handler results](handler_result_specification.md)

### Configuring your handler to Oxygen

Oxygen knows about different handlers based on the [`config.yml`](https://github.com/eficode/robotframework-oxygen/blob/master/config.yml) file. This configuration file can be interacted with through Oxygen's command line.

The configuration has the following parts:
```yml
oxygen.junit:           # Python module. Oxygen will use this key to try to import the handler
  handler: JUnitHandler # Class that Oxygen will initiate after the handler is imported
  keyword: run_junit    # Keyword that should be used to run the other test tool
  tags:                 # List of tags that by default should be added to the test cases converted with this handler
    - oxygen-junit
oxygen.zap:
  handler: ZAProxyHandler
  keyword: run_zap
  tags: oxygen-zap
  accepted_risk_level: 2         # Handlers can have their own command line arguments
  required_confidence_level: 1   # See https://github.com/eficode/robotframework-oxygen/blob/master/DEVGUIDE.md for more information
```

#### `--add-config`

This argument is used to add new handler configuration to Oxygen:

```bash
$ python -m oxygen --add-config path/to/your_handler_config.yml
```

This file is read and appended to the Oxygen's `config.yml`. Based on the key, Oxygen will try to import you handler.

### `--reset-config`

This argument is used to return Oxygen's `config.yml` back to the state it was when the tool was installed:

```bash
$ python -m oxygen --reset-config
```

The command **does not** verify the operation from the user, so be careful.

### `--print-config`

This argument prints the current configuration of Oxygen:
```bash
$ python -m oxygen --print-config
Using config file: /path/to/oxygen/src/oxygen/config.yml
oxygen.gatling:
  handler: GatlingHandler
  keyword: run_gatling
  tags: oxygen-gatling
oxygen.junit:
  handler: JUnitHandler
  keyword: run_junit
  tags:
  - oxygen-junit
oxygen.zap:
  accepted_risk_level: 2
  handler: ZAProxyHandler
  keyword: run_zap
  required_confidence_level: 1
  tags: oxygen-zap

$
```
Because you can add the configuration to the same handler multiple times, note that only the last entry is in effect.

## `utils` module

In [utils module](https://github.com/eficode/robotframework-oxygen/blob/master/src/oxygen/utils.py), you will find assortment of functionalities that you might want to leverage when writing your own handler.

### `run_command_line()`

Most of the time, handlers want to run the other test tool through command line. For this, `utils` provides `run_command_line()` that wraps Python's [`subprocess`](https://docs.python.org/3/library/subprocess.html) module for more easier to use when writing your handler.

`run_command_line()` takes following arguments:
- `cmd`: the command to be executed in a subprocess
- `check_return_code`: if set to `True`, will raise an exception if the `cmd` fails in the subprocess. **Note** that this fails the keyword and, thus, the execution of the test case is stopped. If you want to enable test case to continue even after `run_command_line()` has failed, you should disable it by setting `False`. It is often a good idea to allow user using your handler's keyword to decide how they want the command line execution to affect the test case
- `env`: a dictionary of environment variables that should be passed to the subprocess. By default, `run_command_line()` inherits the environment from the current Python process as well as from modifications done by the Robot Framework command line arguments (ie. `--pythonpath`)

# Developing Oxygen

Clone the Oxygen repository to the environment where you want to the run the tool.

Oxygen requires a set of dependencies to be installed. Dependencies are listed in the `requirements.txt` file:
```
$ pip install -r requirements.txt
```

Oxygen uses task runner tool [`invoke`](http://www.pyinvoke.org/) to run tests, build the project, etc.

Please refer to the available tasks for the project:
```
$ invoke --list
```

and the task file [`tasks.py`](https://github.com/eficode/robotframework-oxygen/blob/master/tasks.py).


# License

Details of project licensing can be found in the [LICENSE](LICENSE) file in the project repository.

# Acknowledgments

Oxygen tool was developed by Eficode Oy as part of [Testomat project](https://www.testomatproject.eu/) with funding by [Business Finland](https://www.businessfinland.fi/).

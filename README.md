# Oxygen

Oxygen is a [Robot Framework](https://robotframework.org/) tool that empowers the user to convert the results of any testing tool or framework to the [Robot Framework's test results](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#created-outputs). This consolidates all test reporting together regardless of tool.

Oxygen has built-in parsers for three testing frameworks: [JUnit](https://junit.org/junit5/), [Gatling](https://gatling.io/), and [Zed Attack Proxy (ZAP)](https://www.zaproxy.org/).

Oxygen is designed to be extensible. Users can create their own parsers for other testing framework or tools to transform their reporting into the Robot Framework's `log.html` and `report.html`.

# Table of Contents
1. [Installation](#installation)
1. [Keyword documentation](#keyword-documentation)
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
- [Python 3.7](http://python.org) or above
- [pip](https://pypi.python.org/pypi/pip) for easy installation
- [Robot Framework](http://robotframework.org)
- [additional dependencies](requirements.txt)

To check the Python version on the command line, run:
```
$ python --version
```

# Keyword documentation

[Keyword Documentation](http://eficode.github.io/robotframework-oxygen/doc/OxygenLibrary.html)

# Usage

## Example: Robot Framework running other test tools

Main usage scenario for Oxygen is the ability to write Robot Framework test cases that run your tests in other test tools and integrate the resulting test report results as part of Robot Framework's. This means you are able to run all of your testing from Robot Framework and thus having all test reporting consolidated together.

After installing Oxygen, it can be used in the Robot Framework suite to write test cases. For example, to build acceptance tests that run different sets of JUnit tests:

``` RobotFramework
*** Settings ***
Library    oxygen.OxygenLibrary

*** Test cases ***

JUnit unit tests should pass
    Run JUnit    path/to/mydir/results.xml    java    -jar   junit.jar   --reports-dir=path/to/mydir

JUnit integration tests should pass
    Run JUnit    path/to/anotherdir/results.xml    java    -jar    junit.jar    --reports-dir=path/to/anotherdir
```

Then, run the suite by providing Oxygen as [a listener](http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#listener-interface):

```
$ robot --listener oxygen.Oxygen my_tests.robot
```

Opening the Robot Framework `log.html` and `report.html`, you should see that test case `JUnit unt tests should pass` has been replaced by Oxygen with test cases matching with what is in the `path/to/mydir/results.xml` JUnit report file. Similarly, test case `JUnit integration tests should pass` has been replaced with results from `path/to/anotherdir/results.xml`; each JUnit test case with its relevant information has a counterpart in the `log.html`.

The example above, for the brevity, shows incomplete commands to run JUnit tool from command line. Please refer to [keyword documentation](#keyword-documentation) for more detailed documentation about keyword's arguments, as well as documentation for [Gatling](https://gatling.io/) and [ZAP](https://www.zaproxy.org/) related keywords. And, of course, refer to the particular tool documentation as well.

## Using from command line

In case where you want to run your other testing tools separately, but yet combine results into unified Robot Framework `log.html` and `report.html`, you can use Oxygen's command line interface to convert single result file to single corresponding Robot Framework `output.xml`:

```
$ python -m oxygen oxygen.junit my_junit_results.xml
```

As a convention, the resulting Robot Framework xml file will be named by adding a suffix to the end. In the example above, the resulting Robot Framework xml file would be named `my_junit_results.xml`.

**Note** that resulting xml file will also be created at the same location as the original result file. Therefore, when original result files are in another directory:

```
$ python -m oxygen oxygen.gatling path/to/results.log
```

Then `results_robot_output.xml` will be created under `path/to/`.

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

and the task file [`tasks.py`](tasks.py).

# License

Details of project licensing can be found in the [LICENSE](LICENSE) file in the project repository.

# Acknowledgments

Oxygen tool  was developed by Eficode Oy as part of [Testomat project](https://www.testomatproject.eu/) with funding by [Business Finland](https://www.businessfinland.fi/).

# Oxygen

Oxygen is a [Robot Framework](https://robotframework.org/) tool that empowers the user to convert the results of any testing tool or framework to [Robot Framework's reporting](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#created-outputs). This consolidates all test reporting together regardless of tools used.

Oxygen has built-in parsers for three testing frameworks: [JUnit](https://junit.org/junit5/), [Gatling](https://gatling.io/), and [Zed Attack Proxy (ZAP)](https://www.zaproxy.org/).

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
- [additional dependencies](requirements.txt) if you are developing Oxygen itself.

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

[Read the developer guide on how to write your own handler](DEVGUIDE.md)

# Developing Oxygen with Nix

Nix is being used in this project for building development environments with capability of running bulk tests across multiple python versions and multiple Robot Framework versions.

## Requirements

- Nix (https://nixos.org/download.html#nix-quick-install)

## Development environment

This opens bash shell in current terminal window, with latest python 3.9 and Robot Framework 3.2.2.
```
$ nix-shell --argstr python python39 --argstr rfVersion 3.2.2
```
Now you can run the tests, for example:
```
$ invoke test --in-nix
$ invoke utest --in-nix
$ invoke atest
```

To exit the environment/shell type `<Ctrl+d>` or:
```
$ exit
```

## Bulk tests

This command tests all currently supported combinations of Python and Robot Framework.
```
$ nix-build test.nix
```
It should run for few minutes, and if all tests pass, the output will be:
```
Overall tests state: ok
```

# License

Details of project licensing can be found in the [LICENSE](LICENSE) file in the project repository.

# Acknowledgments

Oxygen tool was developed by Eficode Oy as part of [Testomat project](https://www.testomatproject.eu/) with funding by [Business Finland](https://www.businessfinland.fi/).

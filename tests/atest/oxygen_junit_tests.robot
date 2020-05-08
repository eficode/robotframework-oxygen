*** Settings ***
Library    oxygen.OxygenLibrary
Library    OperatingSystem

*** Variables ***
${JUNIT XML FILE}=    ${EXECDIR}/green-junit.xml
${GREEN}=    green    # override from command line if your `green` is not globally in PATH

*** Test Cases ***
Oxygen's unit tests should pass
    [Documentation]    Tests in test_oxygen_cli that run things in subprocesses
    ...                *SHOULD* fail; Since `Run JUnit` runs things in
    ...                subprocess itself, this is essentially running
    ...                subprocesses within subprocesses all the way down.
    ...
    ...                We can also inspect errors are reported correctly.
    Remove file     ${JUNIT XML FILE}
    File should not exist    ${JUNIT XML FILE}
    Run JUnit     ${JUNIT XML FILE}
    ...           ${GREEN} -j ${JUNIT XML FILE} ${EXECDIR}
    ...           PYTHONPATH=${EXECDIR}/src

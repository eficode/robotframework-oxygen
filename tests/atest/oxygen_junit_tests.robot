*** Settings ***
Library    oxygen.OxygenLibrary
Library    OperatingSystem

*** Variables ***
${JUNIT XML FILE}=    ${EXECDIR}${/}green-junit.xml

*** Test Cases ***
Oxygen's unit tests should pass
    [Documentation]    Tests in test_oxygen_cli that run things in subprocesses
    ...                *SHOULD* fail; Since `Run JUnit` runs things in
    ...                subprocess itself, this is essentially running
    ...                subprocesses within subprocesses all the way down.
    ...
    ...                We can also inspect errors are reported correctly.
    [Tags]    oxygen-own-junit
    Remove file     ${JUNIT XML FILE}
    File should not exist    ${JUNIT XML FILE}
    ${pytest}=   Get command    pytest
    Run JUnit     ${JUNIT XML FILE}
    ...           ${pytest} --junit-xml\=${JUNIT XML FILE} ${EXECDIR}
    File should exist    ${JUNIT XML FILE}

*** Keywords ***
Get command
    [Arguments]   ${program}
    ${locate}=    Set variable if    '${:}' == ';'    where    which
    Run keyword and return    Run    ${locate} ${program}

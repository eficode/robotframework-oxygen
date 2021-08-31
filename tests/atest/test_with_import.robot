*** Settings ***
Library    oxygen.OxygenLibrary
Library    OperatingSystem

*** Variables ***
${JUNIT XML FILE}=    ${CURDIR}${/}..${/}resources${/}junit-single-testsuite.xml

*** Test Cases ***
Oxygen's unit test with dynamic import
    Import Library    oxygen.OxygenLibrary
    Run JUnit     ${JUNIT XML FILE}
    ...           echo Run JUnit Dynamically Imported

Oxygen's unit test with global import
    Run JUnit     ${JUNIT XML FILE}
    ...           echo Run JUnit Globally Imported

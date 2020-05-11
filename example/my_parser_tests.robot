*** Settings ***
Library    oxygen.OxygenLibrary

*** Test Cases ***
My parser's tests should succeed
    Run my tests    ${CURDIR}/results.json

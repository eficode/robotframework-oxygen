*** Settings ***
Library     oxygen.OxygenLibrary
Metadata    RF suite    This metadata comes from the suite file itself

*** Test Cases ***
Metadata returned by handler should be visible
    [Documentation]    This test is replaced with fix results that have metadata in them
    Run Metadata Dummy Handler    doesentmatter


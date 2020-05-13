*** Settings ***
Library   oxygen.OxygenLibrary

*** Variables ***
${RESOURCES}    ${CURDIR}/../resources

*** Test Cases ***
My First Test
  [Tags]    JUNIT_ROBOT_TAG
  Log   Junit Setup Here 1
  Log   Junit Setup Here 2
  run_junit
    ...   ${RESOURCES}/junit.xml
    ...   echo JUNIT_TEST_STRING
  Log   Junit Teardown Here 1
  Log   Junit Teardown Here 2

My First Test Director's Cut
  [Tags]    JUNIT_ROBOT_TAG
  Sleep   2
  Log   Junit Setup Here 2
  run junit
    ...   ${RESOURCES}/big.xml
    ...   echo JUNIT_TEST_STRING_BIG
  Log   Junit Teardown Here 1
  Log   Junit Teardown Here 2

My Second Test
  [Tags]    GATLING_ROBOT_TAG
  Log   Gatling Setup Here 1
  Log   Gatling Setup Here 2
  run_gatling
    ...   ${RESOURCES}/gatling-example-simulation.log
    ...   echo GATLING TEST STRING
  Log   Gatling Teardown Here 2

My Third Test
  [Tags]    ZAP_ROBOT_TAG
  Log   ZAP Setup Here 1
  Log   ZAP Setup Here 2
  run_zap
    ...   ${RESOURCES}/zap/zap.xml.lol
    ...   echo ZAP TEST STRING 2
  Log   ZAP Teardown Here 1
  Log   ZAP Teardown Here 2

My Three Point Fifth Test
  [Tags]    ZAP_ROBOT_TAG
  Log   ZAP Setup Here 1
  Log   ZAP Setup Here 2
  run_zap
    ...   ${RESOURCES}/zap/zap_pp.json
    ...   echo ZAP TEST STRING 3
  Log   ZAP Teardown Here 1
  Log   ZAP Teardown Here 2

My Fourth Test
  [Tags]    NO_OXYGEN_HERE
  Log   Just a normal test

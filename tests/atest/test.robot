*** Settings ***
Library   oxygen.OxygenLibrary

*** Test Cases ***
My First Test
  [Tags]    JUNIT_ROBOT_TAG
  Log   Junit Setup Here 1
  Log   Junit Setup Here 2
  run_junit
    ...   ${CURDIR}/junit.xml
    ...   echo
    ...   JUNIT_TEST_STRING
  Log   Junit Teardown Here 1
  Log   Junit Teardown Here 2

My First Test Director's Cut
  [Tags]    JUNIT_ROBOT_TAG
  Log   Junit Setup Here 1
  Log   Junit Setup Here 2
  run_junit
    ...   ${CURDIR}/big.xml
    ...   echo
    ...   JUNIT_TEST_STRING_BIG
  Log   Junit Teardown Here 1
  Log   Junit Teardown Here 2

My Second Test
  [Tags]    GATLING_ROBOT_TAG
  Log   Gatling Setup Here 1
  Log   Gatling Setup Here 2
  run_gatling
    ...   ${CURDIR}/gatling-example-simulation.log
    ...   echo
    ...   GATLING TEST STRING
  Log   Gatling Teardown Here 2

#My Third Test
#  [Tags]    ZAP_ROBOT_TAG
#  Log   ZAP Setup Here 1
#  Log   ZAP Setup Here 2
#  run_zap
#  Log   ZAP Teardown Here 1
#  Log   ZAP Teardown Here 2

My Fourth Test
  [Tags]    NO_OXYGEN_HERE
  Log   Just a normal test

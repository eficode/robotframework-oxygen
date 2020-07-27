Notes: Its best if we write down what the pre-requiste knowlegde needed before getting this done. 
        Also if we take create a yotube tutorial on going through the devloper opxtion of oxgygen it would be super nice. 
        


- [ ]  How to run a locust sample program which was mentioned in what is our goal
Ans: locust -f <filename.py> 
reference: https://docs.locust.io/en/stable/running-locust-distributed.html#example

- [ ] More claridfication on the output csv files example should be given. It should be stated explicitly that it is an example formate not the result of the example file stated. 

- [ ] Emphasis the generality in "Our goal is to write an handler, which is able to execute the locust tests inside 
Robot Framework and provide the test results in user-friendly format in the Robot Framework log files."

so that the other testing tools code can be done independently

- [ ] locustenv/locusthandler/resources csv for the requests.csv seems confusing. We need to explicitly mention to cpy paste.


!!!. Failed to run the test using - python -m unittest tests/test_locust.py because of import error - wrote 'Basehandler' instead of 'BaseHandler'

- [ ] "and all 3 tests should pass." ccould be complemented with 

"""
...
----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK
"""

- [ ] Could have an index for all the sections.

- [ ] Following the devguide the user would be in inside the locusthandler directory, if the user 
    runs the python code for  Configuring LocustHandler to Oxygen from the locusthandler directory it will not work with    
    " import locusthandler.locusthandler" but works with " import locusthandler"

    Fix: Either mention to to back to the root directory in locustenv else use the command " import locusthandler"

    Purpose of doing this step also needs to be mentioned

- [ ] Running the  code $ python -m oxygen --version to test the oxygen configuration Following the devguide the user will be way inside the directories if using vim. 
    command needs to be run from the root directory to be successful.

- [ ] where should i install the demo app - is it inside the locustenv or all together different environment? 

- [ ] "Running Locust with LocustHandler in Robot test" it would be nicer if we could add the link to creation of the locust file. 

- [ ] Link to robot file writing could be handy just before test.robot file. 

change later!! I think we neeed robot framework package to be installed to run test.robot

- [ ] "f the test case fails, check first tha" is not checked as it already worked for me

- [ ] It would be nicer to suggest where in locusthandler.py to add the code for "returns the failure_percentage to locustenv/locusthandler/locusthandler.py" ( more clarity to be made in adding to the locusthandler.py)

- [ ] Specify to run the robot test from the root directory to aviod. Error -

"
[ ERROR ] Parsing 'locusthandler/test.robot' failed: File or directory to execute does not exist.
"

- [ ]  Running robot test after adding failure failure_percentage fails. Is it how it is supposed to be ?? If yes we need to metion that in the dev guide. If
    Success by default is understood, but if failure is what is expected, then if need to be mentioned explicitly.
    It shows successful in the command line, but the report and log shows failure.

- [ ] It will be best if we use the git UI design to show what changes was made in the functions defintions to the test_locust.py file.
    test_failure_percentage_max_amount_is_one_hundred
    test_pass_is_true_when_failure_request_percentage_is_below_default_value

- [ ] "Which will create you a locustenv/dist folder."  
    'dist' folder was not created after runnnig the code.

    pip install wheel
    python setup.py bdist_wheel

    Obselete - this error happened becasue I did not add revlevant files for packaging as defined in the tutorial. 

- [ ] Emphasis on the python packaging tutorial is to be given. May be a few sentences than a link. (readers might loss the flow in here.)

- [ ]  Major challenge on where to run the commmand 
        "import locusthandler.locusthandler" after installing the package in the 2nd virtual environment "packagenv"

        I got the import working only after running the command inside the locustenv directory. Is this how it should be? 
        Yes or No, either way we should add more clarification here to make readers life easier.
        I assume its not the right way there is an error because i was not able to run the robot test in the packagenv it exited with error "No keyword with name 'Run Locust' found."
# Devguide Refinement Checklist

- [x] List out the pre-requisites to understand the devguide.
- [ ] Tutorial Video for the developer guide 
- [x] Emphasis on the goal of the developer guide. 
- [x] One or Two lines on the locust tool and the link to the locust website to be given for further exploration.
- [x] Clarification in locustfile about the code snippet being an example of how locustfile and its output looks like and no coding required by the developer at this time when following the devguide.
- [ ] Mention a code snippet on how to run a locustfile.(Use the one from the robot file)
- [x] Find out and mention why do we need to add `resources.csv` is needed. Mention to copy paste the code to the csv file.
- [x] Add link to read more about python virtual environments.
- [x] Mention oxygen also installs robotframework package because, robot is fetched while installing oxygen lib.
- [ ] Consider re-ordering where to introduce the locustfile. (It could be done later when we write the code for locustfile.)
- [x] Emphasis (by making it bold) on running commmand line from the right directory every time we run a code. It is easy to miss and lose flow from developer guide.
- [x] Tree directory structure could be a nice way to exlpain where to run the code every time. 
- [x] Where do I install the demo app - do it where ever you want. It doesn't matter. But it is important explicitly mention a directory so that user don't lose flow of concepts of gets stuck. 
- [ ] In section - "Running Locust with LocustHandler in Robot test", if this is where we finally decide to introduce locust after re-ordering, provide a link it to the locust environment.
- [x] Provide link to robot-framework user guide while introducing the robot file for the first time in the document. 
- [ ] "If the test case fails, " - create a link to the new issue in the git. On how to toggle the debugging mode on/off. This also needed later in the devguide. 
- [x] Clarify the edits in the `locusthandler.py file`. 
- [x] Emphasis (by making it bold) on running commmand line from the right directory every time we run a code. It is easy to miss and lose flow from developer guide.
- [x] encourage/guide users to check the log and report.html files every time a robot code has been executed.
- [ ] if possible use the UI of the git for the changes to be made in the code so that the user is not confused and "let's update" bold words. 
- [x] Link to the python packaging website needs to be updated. 
- [ ] Describe the folders creates in locustenv when python packaging is executed. Also mention to clear it when trying to re-create package in case of error in packaging - build files pile up and fetch older packages if not cleared.
- [ ] mention the importance of folder structure for packaging. check if the users has all the required files include `__init__.py`. 
- [ ] Use tree structure for checking the folder structure.
- [ ] Mention the main file to be edited is python file - `setup.py` and add the rest of the code for other packages to be installed as pre-requiste at the end of `setup.py`.
- [ ] Bring locust file and robot file to packagenv.
- [ ] remind to remove /dist /build and/**egg.info fodler in case we fail to build the package in the first go.
- [ ] mention the use of "if the test case fails, check first that Oxygen's config.yml is correctly configured from the previous section. You can set variable check_return_code to "True" in order to get more specific logging:" -- at running the robot code in the package env -it for debugging purpose whenever the robot test failsd

- [ ] "We notice that two fail because we changed the name of test suite. Let's update the assert statements of the failing tests:" -- where to update

- [ ] "And we are done!" suggest the user to run again --- python -m unittest tests/test_locust.py


- [ ] Keep and eye on the robot test in the package environment as we the locustfile.py path id different from the locustenv - ${CURDIR}/locustfile.py needs to be replaced with "locustfile.py" only - find an explanation for it
- [ ] Improve the introduction.
- [ ] introduce the term locusthandler in #start developing section.


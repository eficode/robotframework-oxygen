import json

from oxygen import BaseHandler


class MyParser(BaseHandler):
    '''
    MyParser is an example how to extend Oxygen by writing your own handler
    '''
    RESULTS = {'tests': [
        {'name': 'My test 1', 'passed': True, 'msg': ''},
        {'name': 'My Test 2', 'passed': False, 'msg': 'Error text D:'}]
    }

    def run_my_tests(self, result_file):
        with open(result_file, 'w') as f:
            json.dump(self.RESULTS, f)
        return result_file

    def parse_results(self, result_file):
        with open(result_file, 'r') as f:
            results = json.load(f)
        return {
            'name': result_file,
            'tags': [],
            'setup': None,
            'teardown': None,
            'suites': [],
            'tests': [{
                'name': test['name'],
                'tags': [],
                'setup': None,
                'teardown': None,
                'keywords': [{
                    'name': test['name'] + ' result',
                    'pass': test['passed'],
                    'elapsed': 0.0,
                    'tags': [],
                    'messages': [test['msg']],
                    'teardown': None,
                    'keywords': []
                }]
            } for test in results['tests']]
        }

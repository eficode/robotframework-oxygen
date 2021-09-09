from oxygen import BaseHandler


class MyDummyHandler(BaseHandler):
    '''
    A test handler for passing tuple if parse_results accepts one parameter
    '''

    def run_my_dummy_handler(self, result_file):
        return result_file, 'foo'

    def parse_results(self, result_file):
        return {
            'name': result_file
        }

from oxygen import BaseHandler


class MyDummyHandler(BaseHandler):
    '''
    A test handler that throws mismatch argument exception if single argument
    is passed with multiple accepted
    '''

    def run_my_dummy_handler(self, result_file):
        return result_file

    def parse_results(self, result_file, foo='foo'):
        return {
            'name': result_file,
            'foo': foo
        }

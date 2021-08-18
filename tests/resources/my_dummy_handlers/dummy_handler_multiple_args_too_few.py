from oxygen import BaseHandler


class MyDummyHandler(BaseHandler):
    '''
    A test handler that throws mismatch argument exception because
    parse_results expects too many arguments
    '''

    def run_my_dummy_handler(self, result_file):
        return result_file, 'foo'

    def parse_results(self, result_file, foo, bar):
        return {
            'name': result_file,
            'foo': foo,
            'bar': bar
        }

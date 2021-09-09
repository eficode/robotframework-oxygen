from oxygen import BaseHandler


class MyDummyHandler(BaseHandler):
    '''
    A test handler for unfolding parse_results arguments
    if it has multiple parameters
    '''

    def run_my_dummy_handler(self, result_file):
        return result_file, 'foo'

    def parse_results(self, result_file, foo):
        return {
            'name': result_file,
            'foo': foo
        }

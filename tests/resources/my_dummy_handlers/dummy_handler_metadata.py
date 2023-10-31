from oxygen import BaseHandler

class MyDummyMetadataHandler(BaseHandler):
    def run_metadata_dummy_handler(self, result_file):
        return result_file

    def parse_results(self, result_file):
        return {
            'name': 'Minimal Suite',
            'metadata': {
                'Main-level metadata': 'This should come *from handler*'
            },
            'suites': [{
                'name': 'Minimal Subsuite',
                'metadata': { 'Sub-level metadata': '_Inner_ metadata' },
                'tests': [{
                    'name': 'Minimal TC',
                    'keywords': [{ 'name': 'someKeyword', 'pass': True }]
                }]
            }]
        }

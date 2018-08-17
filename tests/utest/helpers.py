from tempfile import mkstemp

from yaml import load

TEST_CONFIG = '''
oxygen.junit:
  handler: JUnitHandler
  keyword: run_junit
  tags:
    - JUNIT
    - EXTRA_JUNIT_CASE
oxygen.gatling:
  handler: GatlingHandler
  keyword: run_gatling
  tags: GATLING
oxygen.zap:
  handler: ZAProxyHandler
  keyword: run_zap
  tags: ZAP
  accepted_risk_level: 2
  required_confidence_level: 1
'''


def get_config():
    return load(TEST_CONFIG)

def get_config_as_file():
    _, filepath = mkstemp()
    with open(filepath, 'w') as f:
        f.write(TEST_CONFIG)
    return filepath


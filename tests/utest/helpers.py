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

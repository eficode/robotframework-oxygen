TestSuite:

{
  'name': <string>,
  'tags': [
    <string>,
  ],
  'setup': <keyword>,
  'teardown': <keyword>,
  'suites': [
    <testsuite>,
  ],
  'tests': [
    '<testcase>',
  ],
}


TestCase:

{
  'name': <string>,
  'tags': [
    <string>,
  ],
  'setup': <keyword>,
  'teardown': <keyword>,
  'keywords': [
    <keyword>,
  ],
}


Keyword:

{
  'name': <string>,
  'pass': <bool>,
  'elapsed': <float>, // milliseconds
  'tags': [
    <string>,
  ],
  'messages': [
    <string>,
  ],
  'teardown': <keyword>,
  'keywords': [
    <keyword>,
  ],
}

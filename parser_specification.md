TestSuite:

{
  'name': <string>,
  'start': <int>, // timestamp
  'finish': <int>, // timestamp
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
  'start': <int>, // timestamp
  'finish': <int>, // timestamp
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
  'start': <int>, // timestamp
  'finish': <int>, // timestamp
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

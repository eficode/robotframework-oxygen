# Oxygen handler result specification
```
{
  "$defs": {
    "OxygenKeywordDict": {
      "properties": {
        "pass": {
          "title": "Pass",
          "type": "boolean"
        },
        "name": {
          "title": "Name",
          "type": "string"
        },
        "elapsed": {
          "title": "Elapsed",
          "type": "number"
        },
        "tags": {
          "items": {
            "type": "string"
          },
          "title": "Tags",
          "type": "array"
        },
        "messages": {
          "items": {
            "type": "string"
          },
          "title": "Messages",
          "type": "array"
        },
        "teardown": {
          "$ref": "#/$defs/OxygenKeywordDict"
        },
        "keywords": {
          "items": {
            "$ref": "#/$defs/OxygenKeywordDict"
          },
          "title": "Keywords",
          "type": "array"
        }
      },
      "required": [
        "pass",
        "name"
      ],
      "title": "OxygenKeywordDict",
      "type": "object"
    },
    "OxygenSuiteDict": {
      "properties": {
        "name": {
          "title": "Name",
          "type": "string"
        },
        "tags": {
          "items": {
            "type": "string"
          },
          "title": "Tags",
          "type": "array"
        },
        "setup": {
          "$ref": "#/$defs/OxygenKeywordDict"
        },
        "teardown": {
          "$ref": "#/$defs/OxygenKeywordDict"
        },
        "metadata": {
          "additionalProperties": {
            "type": "string"
          },
          "title": "Metadata",
          "type": "object"
        },
        "suites": {
          "items": {
            "$ref": "#/$defs/OxygenSuiteDict"
          },
          "title": "Suites",
          "type": "array"
        },
        "tests": {
          "items": {
            "$ref": "#/$defs/OxygenTestCaseDict"
          },
          "title": "Tests",
          "type": "array"
        }
      },
      "required": [
        "name"
      ],
      "title": "OxygenSuiteDict",
      "type": "object"
    },
    "OxygenTestCaseDict": {
      "properties": {
        "name": {
          "title": "Name",
          "type": "string"
        },
        "keywords": {
          "items": {
            "$ref": "#/$defs/OxygenKeywordDict"
          },
          "title": "Keywords",
          "type": "array"
        },
        "tags": {
          "items": {
            "type": "string"
          },
          "title": "Tags",
          "type": "array"
        },
        "setup": {
          "$ref": "#/$defs/OxygenKeywordDict"
        },
        "teardown": {
          "$ref": "#/$defs/OxygenKeywordDict"
        }
      },
      "required": [
        "name",
        "keywords"
      ],
      "title": "OxygenTestCaseDict",
      "type": "object"
    }
  },
  "allOf": [
    {
      "$ref": "#/$defs/OxygenSuiteDict"
    }
  ]
}
```
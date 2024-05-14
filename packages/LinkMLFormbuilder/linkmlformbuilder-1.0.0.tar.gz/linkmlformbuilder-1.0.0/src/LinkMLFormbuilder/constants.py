NAME = "name"
DEFAULT = "default"
CWD = "cwd"
HTML_EXT = ".html"
DEFAULT_RANGE = "default_range"
SLOTS = "slots"
RANGE = "range"
CLASSES = "classes"
ATTRIBUTES = "attributes"
REQUIRED = "required"
IS_A = "is_a"
MIXINS = "mixins"
VALUES_FROM = "values_from"
ENUMS = "enums"
PERMISSIBLE_VALUES = "permissible_values"
ENUM_RANGE = "enum_range"
SEPARATOR = " / "
ALIASES = "aliases"
STRUCTURED_ALIASES = "structured_aliases"
LOCAL_NAMES = "local_names"
TITLE = "title"
DESCRIPTION = "description"
ALT_DESCRIPTIONS = "alt_descriptions"
MULTIVALUED = "multivalued"
MAXIMUM_CARDINALITY = "maximum_cardinality"
SINGULAR_NAME = "singular_name"
MINIMUM_CARDINALITY = "minimum_cardinality"
MINIMUM_VALUE = "minimum_value"
MAXIMUM_VALUE = "maximum_value"

HTML_START = '''<!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8'>
    <meta http-equiv='X-UA-Compatible' content='IE=edge'>
    <title>LinkML JSON schema form builder</title>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.4.1/dist/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
</head>
<style>
'''
HTML_START_PART2 = '''
</style>
<body>
'''
HTML_START_HTML_ONLY = '''<!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8'>
    <meta http-equiv='X-UA-Compatible' content='IE=edge'>
    <title>LinkML JSON schema form builder</title>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.4.1/dist/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
</head>
<style>
    .form-text {
        font-style: italic;
        width: -webkit-fill-available;
    }

    p :not(.form-description){
        margin-bottom: 0px !important;
    }

    .form-description {
        margin-top: 0px !important;
        margin-bottom: 20px;
    }

    body {
        margin-left: 10px !important;
    }

    label {
        font-weight: normal !important;
    }

    .input-group {
        width: -webkit-fill-available !important;
        display: table !important;
    }

    .mb-3 {
        margin-bottom: 1rem !important;
    }

    .input-group-text {
        padding: .5rem .75rem;
        font-weight: 400;
        line-height: 1.5;
        color: #212529;
        text-align: center;
        white-space: nowrap;
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 0.375rem;
        float: left;
        min-height: 34px;
        white-space: pre-wrap;
    }

    .width20 {
        width: 20%
    }

    .form-control {
        width: 80% !important;
        height: 100%;
    }

    .input-group {
        position: relative;
        display: flex;
        flex-wrap: wrap;
        align-items: stretch;
        width: 100%;
    }

    .hideField {
        display: none !important;
    }

    .form-check {
        width: fit-content;
        display: inline-block;
        margin-right: 5px;
    }

    .values-from {
        font-weight: bold;
        margin-right: 5px;
    }

    .values-from-dynamic {
        font-weight: bold;
        margin-right: 5px;
        float: left;
        width: calc(20% - 5px);
    }

    h2 {
        width: 100vw;
    }

    .answer-options {
        padding-left: 0.667px;
    }

    details {
        border: 1px solid #dee2e6;
        border-radius: 0.375rem;
        padding: 0.5em 0.5em 0;
        width: fit-content;
        margin-bottom: 0.5rem;
    }
    
    summary {
        font-weight: bold;
        margin: -0.5em -0.5em 0;
        padding: 0.5em;
    }
    
    details[open] {
        padding: 0.5em;
    }
    
    details[open] summary {
        border-bottom: 1px solid #dee2e6;
        margin-bottom: 0.5em;
    }
</style>
<body>
'''
HTML_END = '''</body>
</html>'''
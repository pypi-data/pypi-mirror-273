import argparse
import yaml
from LinkMLFormbuilder import utils
# import utils
import os
import pdfkit
from LinkMLFormbuilder import slot_code_generators
# import slot_code_generators
from shutil import which
import pkg_resources
from LinkMLFormbuilder import constants
# import constants
import warnings

def retrieveFileContent(yamlfile):
    try:
        stream = open(os.path.abspath(yamlfile), "r")
        return yaml.safe_load(stream)
    except yaml.YAMLError:
        print("File could not be parsed")
        exit(1)
    except Exception:
        print("Could not retrieve file content, please make sure the path is correct")
        exit(1)

def getSlotFormCode(slotCode, content, default_range, subclasses, level, key):
    if (slotCode is None): return ""
    # if (constants.NAME not in slotCode): raise TypeError("Missing field: name")
    desc = utils.extractDescription(slotCode)
    required = constants.REQUIRED if (constants.REQUIRED in slotCode and slotCode.get(constants.REQUIRED) == True) else ""
    propertyName = slotCode.get(constants.NAME)
    if (propertyName == None): propertyName = key
    title = utils.extractSlotName(slotCode, key)
    
    if (constants.VALUES_FROM in slotCode or (constants.RANGE in slotCode and constants.ENUMS in content and slotCode.get(constants.RANGE) in content.get(constants.ENUMS))):
        return slot_code_generators.getEnumSlotCode(slotCode, content, desc, required, propertyName, title)
    elif (constants.ENUM_RANGE in slotCode): # inlined enum
        return slot_code_generators.getInlineEnumSlotCode(slotCode, desc, required, propertyName, title)
    elif (constants.RANGE in slotCode):
        if (slotCode.get(constants.RANGE) in content.get(constants.CLASSES)):
            return getClassFormCode(content.get(constants.CLASSES).get(slotCode.get(constants.RANGE)), content, default_range, subclasses, level + 1, key) # the range is a class itself and should be treated as such
        elif (slotCode.get(constants.RANGE) == "integer" or slotCode.get(constants.RANGE) == "float"):
            return slot_code_generators.getNumberSlotCode(slotCode, desc, required, propertyName, title)
        elif (slotCode.get(constants.RANGE) == "string"): #assume textarea
            return slot_code_generators.getTextareaSlotCode(desc, required, propertyName, title, slotCode, html_only)
        elif (slotCode.get(constants.RANGE) == "boolean"):
            return slot_code_generators.getBooleanSlotCode(desc, required, propertyName, title)
        else: # this is a basic pdf, so datetime should not be a datetime field, but a textfield
            return slot_code_generators.getStringSlotCode(desc, required, propertyName, title, slotCode)
    else: # rely on default range
        if (default_range is not None):
            if (default_range == "integer" or default_range == "float"):
                return slot_code_generators.getNumberSlotCode(slotCode, desc, required, propertyName, title)
            elif (default_range == "string"): #assume textarea
                return slot_code_generators.getTextareaSlotCode(desc, required, propertyName, title, slotCode, html_only)
            elif (default_range == "boolean"):
                return slot_code_generators.getBooleanSlotCode(desc, required, propertyName, title)
            else: # this is a basic pdf, so datetime should not be a datetime field, but a textfield
                return slot_code_generators.getStringSlotCode(desc, required, propertyName, title, slotCode)
        else:
            raise TypeError("Invalid LinkML. There should either be a explicitly defined range for slot {slot}, or a default_range.".format(slot=utils.extractName(slotCode, key)))

def getClassFormCode(classCode, content, default_range, subclasses, level, key):
    title = utils.extractName(classCode, key)
    code = '''<h{level}>{title}</h{level}>\n'''.format(level = level + 1, title = title)
    global html_only
    if(html_only == True):
        code += "<details><summary style=\"display:list-item\">Form description</summary>" + utils.capitalizeLabel(utils.extractDescription(classCode)) + "</details>"
    else:
        code += "<p class='form-description'>Form description: " + utils.capitalizeLabel(utils.extractDescription(classCode)) + "</p>\n"
    if (constants.IS_A in classCode): # process superclass first
        superClassName = classCode.get(constants.IS_A)
        superClassCode = content.get(constants.CLASSES).get(superClassName)
        for slot in superClassCode.get(constants.SLOTS):
            if (slot not in classCode.get("slot_usage")): # this slot is not further specified in the class itself
                slotCode = content.get(constants.SLOTS).get(slot)
                code += getSlotFormCode(slotCode, content, default_range, subclasses, level, slot)
    if (constants.MIXINS in classCode): # then process mixins
        for key in classCode.get(constants.MIXINS):
            mixinCode = content.get(constants.CLASSES).get(key)
            for slot in mixinCode.get(constants.SLOTS):
                if (slot not in classCode.get("slot_usage")): # this slot is not further specified in the class itself
                    slotCode = content.get(constants.SLOTS).get(slot)
                    code += getSlotFormCode(slotCode, content, default_range, subclasses, level, slot)
    
    if (constants.SLOTS in classCode):
        gen = (slot for slot in classCode.get(constants.SLOTS) if (content.get(constants.SLOTS).get(slot).get(constants.RANGE) not in subclasses and content.get(constants.SLOTS).get(slot) is not None))
        for slot in gen: #process slots of this class
            slotCode = content.get(constants.SLOTS).get(slot)
            code += getSlotFormCode(slotCode, content, default_range, subclasses, level, slot)
    if (constants.ATTRIBUTES in classCode): #inline slots
        for slot in classCode.get(constants.ATTRIBUTES):
            slotCode = classCode.get(constants.ATTRIBUTES).get(slot)
            code += getSlotFormCode(slotCode, content, default_range, subclasses, level, slot)
    if (constants.SLOTS in classCode):
        gen2 = (slot for slot in classCode.get(constants.SLOTS) if (content.get(constants.SLOTS).get(slot).get(constants.RANGE) in subclasses and content.get(constants.SLOTS).get(slot) is not None))
        for slot in gen2: #process slots of this class where the range is a subclass
            slotCode = content.get(constants.SLOTS).get(slot)
            code += getSlotFormCode(slotCode, content, default_range, subclasses, level, slot)
    return code


def buildForm(content, html_only_in, output_directory, name, testEnv = False):
    global html_only
    html_only = html_only_in #extra storage for test purposes
    if (constants.NAME not in content and name == constants.DEFAULT): 
        warnings.warn("WARNING: The model metadata does not contain a 'name' field. Please make sure your model is valid")
    NAME = name if (name != constants.DEFAULT) else (content.get(constants.NAME) if constants.NAME in content else "formDefault")
    OUTPUT_DIR = os.getcwd() if (output_directory == constants.CWD) else os.path.abspath(output_directory)
    HTML_PATH = os.path.join(OUTPUT_DIR, NAME + constants.HTML_EXT)
    
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        if (html_only == True):
            f.write(constants.HTML_START_HTML_ONLY)
        else:
            f.write(constants.HTML_START)
            f.write(pkg_resources.resource_string(__name__, "bootstrap.css").decode('utf-8'))
            f.write("\n")
            f.write(pkg_resources.resource_string(__name__, "styles.css").decode('utf-8'))
            f.write(constants.HTML_START_PART2)
        title = utils.extractName(content, "default")
        f.write("<h1>" + title + "</h1>\n")
        default_range = content.get(constants.DEFAULT_RANGE) if (constants.DEFAULT_RANGE in content) else None
        classes = []
        superClasses = []
        subClasses = [] # all classes that are technically containers/subclasses
        if (constants.SLOTS in content):
            for key in content.get(constants.SLOTS):
                slotCode = content.get(constants.SLOTS).get(key)
                if (slotCode is not None and constants.RANGE in slotCode and slotCode.get(constants.RANGE) in content.get(constants.CLASSES)):
                    subClasses.append(slotCode.get(constants.RANGE))

        for key in content.get(constants.CLASSES):
            classCode = content.get(constants.CLASSES).get(key)       
            if (constants.IS_A in classCode):
                superClasses.append(classCode.get(constants.IS_A))
            if ("mixin" in classCode and classCode.get("mixin") == True): # it is a mixin
                superClasses.append(key)
            if (constants.MIXINS in classCode): # it inherits from other classes which should not be shown separately in forms
                for mixin in classCode.get(constants.MIXINS):
                    superClasses.append(mixin)
            if (constants.ATTRIBUTES in classCode):
                for attribute in classCode.get(constants.ATTRIBUTES):
                    slotCode = classCode.get(constants.ATTRIBUTES).get(attribute)
                    if (slotCode is not None and constants.RANGE in slotCode and slotCode.get(constants.RANGE) in content.get(constants.CLASSES)):
                        subClasses.append(slotCode.get(constants.RANGE))

            if (key not in superClasses and key not in subClasses):
                classes.append(key)
        for key in classes:
            classCode = content.get(constants.CLASSES).get(key)
            if ("abstract" not in classCode or classCode.get("abstract") == False): # if the class is abstract, it should not be in the form
                f.write(getClassFormCode(classCode, content, default_range, subClasses, 1, key))
        f.write(constants.HTML_END)
        f.close()
        if (not html_only):
            options = { 
            'margin-bottom': '1cm', 
            'footer-right': '[page] of [topage]',
            }
            pdfkit.from_file(HTML_PATH, os.path.join(OUTPUT_DIR, NAME + ".pdf"), options=options)
        if (testEnv):
            f = open(HTML_PATH, "r", encoding="utf-8")
            html_result = f.read()
            f.close()
            return html_result

def cli():
    if (which("wkhtmltopdf") is None):
        #install somehow, for now: error
        raise ImportError("wkhtmltopdf is not installed, please install from: https://wkhtmltopdf.org/downloads.html")
        exit(1)
    
    parser = argparse.ArgumentParser("linkmlformbuilder")
    parser.add_argument("yamlfile", help="The LinkML yaml file for which a form should be built")
    parser.add_argument("-html", "--html_only", dest="html_only", action="store_true", help="This flag is used when the user only wants an HTML file returned, there will be no PDF export", default=False)
    parser.add_argument("-dir", "--output_directory", dest="output_directory", help="Specify an output directory, the current working directory is used when this value not provided or the flag is missing", nargs="?", default=constants.CWD, const=constants.CWD)
    parser.add_argument("--name", help="Specify an alternative file name, do not specify a file extension. By default, the filename of the yamlfile is used for the HTML and optionally PDF files", nargs="?", default=constants.DEFAULT, const=constants.DEFAULT)
    args = parser.parse_args()
    global html_only
    html_only = args.html_only
    buildForm(retrieveFileContent(args.yamlfile), html_only, args.output_directory, args.name)

if __name__ == "__main__":
    cli()

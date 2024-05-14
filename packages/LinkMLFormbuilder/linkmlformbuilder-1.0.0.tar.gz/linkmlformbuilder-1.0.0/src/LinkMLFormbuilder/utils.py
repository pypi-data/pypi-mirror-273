import re
from LinkMLFormbuilder import constants
# import constants
import warnings

def extractAliases(sourceCode):
    name = ""
    if (constants.ALIASES in sourceCode or constants.STRUCTURED_ALIASES in sourceCode or constants.LOCAL_NAMES in sourceCode):
        name += " ("
        if (constants.ALIASES in sourceCode):
            for alias in sourceCode.get(constants.ALIASES):
                name += alias + constants.SEPARATOR
        if (constants.STRUCTURED_ALIASES in sourceCode):
            structured_aliases = sourceCode.get(constants.STRUCTURED_ALIASES)
            for structured_alias in structured_aliases:
                if (constants.TITLE in structured_alias):
                    name += structured_alias.get(constants.TITLE) + constants.SEPARATOR
                else:
                    name += structured_alias.get("literal_form") + constants.SEPARATOR
        if (constants.LOCAL_NAMES in sourceCode):
            for local_name in sourceCode.get(constants.LOCAL_NAMES):
                name += local_name.get("local_name_value") + constants.SEPARATOR
        name = name[:-3] + ")"
    return name

def extractName(classCode, key):
    if (constants.NAME not in classCode): 
        warnings.warn("WARNING: missing field name")
        return key
    return (classCode.get(constants.TITLE) if (constants.TITLE in classCode) else classCode.get(constants.NAME)) + extractAliases(classCode)

def extractDescription(itemCode):
    description = ""
    if (constants.DESCRIPTION in itemCode):
        description = normalize_description(itemCode.get(constants.DESCRIPTION))
    if (constants.ALT_DESCRIPTIONS in itemCode):
        description += " ("
        for alt_description in itemCode.get(constants.ALT_DESCRIPTIONS):
            description += normalize_description(alt_description.get(constants.DESCRIPTION)) + constants.SEPARATOR
        description = description[:-3] + ")"
    return description

def extractSlotName(slotCode, slot):
    name = ""
    if (((constants.MULTIVALUED in slotCode and slotCode.get(constants.MULTIVALUED) == False) or (constants.MAXIMUM_CARDINALITY in slotCode and slotCode.get(constants.MAXIMUM_CARDINALITY) == 1)) and constants.SINGULAR_NAME in slotCode):
        name = slotCode.get(constants.SINGULAR_NAME) # cardinality is either 0..1 or 1..1
    else:
        name += extractName(slotCode, slot)
    return name

def normalize_description(desc): # remove html tags <p><div>, remove anything in <i> and <img>
    p = re.compile(r'<.*?>')
    return p.sub('', desc).strip()

def capitalizeLabel(label):
    if (len(label) == 0): return label
    return label[0].upper() + label[1:]

def isMultivalued(slotCode):
    multivalued = True if ((constants.MULTIVALUED in slotCode and slotCode.get(constants.MULTIVALUED) == True) or (constants.MAXIMUM_CARDINALITY in slotCode and slotCode.get(constants.MAXIMUM_CARDINALITY) > 1)) else False
    return multivalued

def getMinCardinality(slotCode):
    if (constants.MINIMUM_CARDINALITY in slotCode): return slotCode.get(constants.MINIMUM_CARDINALITY)
    elif (constants.MULTIVALUED in slotCode): return 1
    elif (constants.REQUIRED in slotCode and slotCode.get(constants.REQUIRED) == True): return 1
    return 0

def getMaxCardinality(slotCode):
    if (constants.MAXIMUM_CARDINALITY in slotCode): return slotCode.get(constants.MAXIMUM_CARDINALITY)
    elif (constants.MULTIVALUED not in slotCode): return 1
    elif (constants.MULTIVALUED in slotCode and slotCode.get(constants.MULTIVALUED) == True): return 2 # no max cardinality specified
    else: return 1

def getRangeDeclaration(slotCode):
    rangeDeclaration = ""
    if (constants.MINIMUM_VALUE in slotCode and constants.MAXIMUM_VALUE in slotCode):
      rangeDeclaration = "The value for this field should be between {min} and {max}".format(min = slotCode.get(constants.MINIMUM_VALUE), max = slotCode.get(constants.MAXIMUM_VALUE))
    elif (constants.MINIMUM_VALUE in slotCode):
      rangeDeclaration = "The value for this field should be equal to or greater than {min}".format(min = slotCode.get(constants.MINIMUM_VALUE))
    elif (constants.MAXIMUM_VALUE in slotCode):
       rangeDeclaration = "The value for this field should be equal to or smaller than {max}".format(max = slotCode.get(constants.MAXIMUM_VALUE))
    return rangeDeclaration

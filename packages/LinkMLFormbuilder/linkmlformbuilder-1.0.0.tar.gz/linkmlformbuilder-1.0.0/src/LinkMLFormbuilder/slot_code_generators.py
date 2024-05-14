from LinkMLFormbuilder import constants, utils
# import utils
# import constants

def getNumberSlotCode(slotCode, desc, required, propertyName, title):
    rangeDeclaration = utils.getRangeDeclaration(slotCode)
    multivalued = utils.isMultivalued(slotCode)
    minCardinality = utils.getMinCardinality(slotCode)
    maxCardinality = utils.getMaxCardinality(slotCode)   
    cardinalityStatement = ""
    
    code = '''<div class="mb-3">
    <div class="input-group">
      <span class="input-group-text width20" id="{propertyName}-addon">{title}</span>
      <input type="number" class="form-control" id="{propertyName}" name="{propertyName}" aria-describedby="{propertyName}-addon {propertyName}-description" {required}>
    </div>'''.format(propertyName = propertyName, required = required, desc = utils.capitalizeLabel(desc), title = utils.capitalizeLabel(title), rangeDeclaration = rangeDeclaration)

    if (multivalued):
        for i in range(maxCardinality-1):
            code += '''<div class="input-group">
        <span class="input-group-text width20 hideField" id="{propertyName}-addon">{title}</span>
        <input type="number" class="form-control" id="{propertyName}{n}" name="{propertyName}{n}" aria-describedby="{propertyName}-addon {propertyName}-description">
        </div>'''.format(propertyName = propertyName, required = required, title = utils.capitalizeLabel(title), n = i+2)
        cardinalityStatement = ''' This field requires at least {minCardinality} value(s)'''.format(minCardinality = minCardinality)

    code += '''
    <div class="form-text" id="{propertyName}-description">{desc} {rangeDeclaration}{cardinalityStatement}</div>
  </div>\n'''.format(propertyName = propertyName, required = required, desc = utils.capitalizeLabel(desc), title = utils.capitalizeLabel(title), rangeDeclaration = rangeDeclaration, cardinalityStatement = cardinalityStatement)
    return code

def getBooleanSlotCode(desc, required, propertyName, title):
    code = '''<div class="mb-3">
            <div class="input-group">\n'''
    code += '''<span class="input-group-text">{slotName}</span>\n'''.format(slotName = utils.capitalizeLabel(title))
    code += '''<input type="text" class="form-control hideField">\n</div>\n'''
    code += '''<div class="form-text" id="{propertyName}-description">{desc}</div>\n'''.format(propertyName = propertyName, desc = utils.capitalizeLabel(desc))
    code += "<div class='answer-options'>\n"
    code += '''<div class="form-check">
                  <input class="form-check-input" type="radio" name="{enumName}" id="{item}" value="{item}" {required}>
                  <label class="form-check-label" for="{item}">{item}</label></div>\n'''.format(enumName = propertyName, item = "True", required = required)
    code += '''<div class="form-check">
                  <input class="form-check-input" type="radio" name="{enumName}" id="{item}" value="{item}" {required}>
                  <label class="form-check-label" for="{item}">{item}</label></div>\n'''.format(enumName = propertyName, item = "False", required = required)
    code += "</div>\n</div>\n"     
    return code

def getEnumSlotCode(slotCode, content, desc, required, propertyName, title):
    multivalued = utils.isMultivalued(slotCode)
    
    code = '''<div class="mb-3">
            <div class="input-group">\n'''
    code += '''<span class="input-group-text">{slotName}</span>\n'''.format(slotName = utils.capitalizeLabel(title))
    code += '''<input type="text" class="form-control hideField">\n</div>\n'''
    code += '''<div class="form-text" id="{propertyName}-description">{desc}</div>\n'''.format(propertyName = propertyName, desc = utils.capitalizeLabel(desc))
    enumList = []
    if (constants.VALUES_FROM in slotCode):
       for enum in slotCode.get(constants.VALUES_FROM): enumList.append(enum)
    if (constants.RANGE in slotCode and constants.RANGE in content.get(constants.ENUMS)): enumList.append(slotCode.get(constants.RANGE))
    
    for enum in enumList:
      if (enum not in content.get(constants.ENUMS)):
          return getTextareaSlotCode(desc, required, propertyName, title, slotCode, True)
      enumCode = content.get(constants.ENUMS).get(enum)
      enumName = utils.extractName(enumCode, "")
      if (constants.PERMISSIBLE_VALUES in enumCode):
        code += getPermissibleValuesCode(enumCode.get(constants.PERMISSIBLE_VALUES), enumName, multivalued, required)
      else:
        code += '''<div class='answer-options'>\n<span class='values-from-dynamic'>{enumName}:</span>\n<textarea rows="6" class="form-control" id="{propertyName}" name="{propertyName}"></textarea></div>'''.format(enumName = utils.capitalizeLabel(enumName), propertyName = enumCode.get(constants.NAME))
    code += "</div>\n"        
    return code

def getPermissibleValuesCode(permissible_values, enumName, multivalued, required):
    code = "<div class='answer-options'>\n<span class='values-from'>" + utils.capitalizeLabel(enumName) + ":</span>\n"
    for value in permissible_values:
      if (not multivalued):
        code += '''<div class="form-check">
            <input class="form-check-input" type="radio" name="{enumName}" id="{itemNoSpace}" value="{itemNoSpace}" {required}>
            <label class="form-check-label" for="{itemNoSpace}">{itemCap}</label></div>\n'''.format(enumName = enumName.replace(" ", "_"), required = required, itemNoSpace = value.replace(" ", "_"), itemCap = utils.capitalizeLabel(value))
      else:
            code += '''<div class="form-check">
            <input class="form-check-input" type="checkbox" name="{enumName}" id="{itemNoSpace}" value="{itemNoSpace}" {required}>
            <label class="form-check-label" for="{itemNoSpace}">{itemCap}</label></div>\n'''.format(enumName = enumName.replace(" ", "_"), required = required, itemNoSpace = value.replace(" ", "_"), itemCap = utils.capitalizeLabel(value))
    return code + "</div>\n"

def getInlineEnumSlotCode(slotCode, desc, required, propertyName, title):
    multivalued = utils.isMultivalued(slotCode)

    if (constants.ENUM_RANGE not in slotCode or (constants.PERMISSIBLE_VALUES not in slotCode.get(constants.ENUM_RANGE) and "reachable_from" not in slotCode.get(constants.ENUM_RANGE))):
        return getTextareaSlotCode(desc, required, propertyName, title, slotCode, True)

    code = '''<div class="mb-3">
            <div class="input-group">\n'''
    code += '''<span class="input-group-text">{slotName}</span>\n'''.format(slotName = utils.capitalizeLabel(title))
    code += '''<input type="text" class="form-control hideField">\n</div>\n'''
    code += '''<div class="form-text" id="{propertyName}-description">{desc}</div>\n'''.format(propertyName = propertyName, desc = utils.capitalizeLabel(desc))
    enumCode = slotCode.get(constants.ENUM_RANGE)
    enumName = utils.extractName(slotCode, "") + " valueset" #inlined enums don't have names and titles, so it's generated from the slot itself
    if (constants.PERMISSIBLE_VALUES in enumCode):
        code += getPermissibleValuesCode(enumCode.get(constants.PERMISSIBLE_VALUES), enumName, multivalued, required)
    else:
      code += '''<div class='answer-options'>\n<span class='values-from-dynamic'>{enumName}:</span>\n<textarea rows="6" class="form-control" id="{enumNameNoSpace}" name="{enumNameNoSpace}"></textarea>\n</div>\n'''.format(enumName = utils.capitalizeLabel(enumName), propertyName = enumCode.get(constants.NAME), enumNameNoSpace = enumName.replace(" ", "_"))
    code += "</div>\n"     
    return code

def getStringSlotCode(desc, required, propertyName, title, slotCode):
    multivalued = utils.isMultivalued(slotCode)
    minCardinality = utils.getMinCardinality(slotCode)
    maxCardinality = utils.getMaxCardinality(slotCode)   
    cardinalityStatement = ""

    code =  '''<div class="mb-3">
    <div class="input-group">
      <span class="input-group-text width20" id="{propertyName}-addon">{title}</span>
      <input type="text" class="form-control" id="{propertyName}" name="{propertyName}" aria-describedby="{propertyName}-addon {propertyName}-description" {required}>
    </div>
    '''.format(propertyName = propertyName, required = required, title = utils.capitalizeLabel(title))
    if (multivalued):
        for i in range(maxCardinality-1):
            code += '''<div class="input-group">
      <span class="input-group-text width20 hideField" id="{propertyName}-addon">{title}</span>
      <input type="text" class="form-control" id="{propertyName}{n}" name="{propertyName}{n}" aria-describedby="{propertyName}-addon {propertyName}-description">
    </div>'''.format(propertyName = propertyName, required = required, title = utils.capitalizeLabel(title), n = i+2)
        cardinalityStatement = ''' This field requires at least {minCardinality} value(s)'''.format(minCardinality = minCardinality)


    code += '''<div class="form-text" id="{propertyName}-description">{desc}{cardinalityStatement}</div>
  </div>\n'''.format(propertyName = propertyName, desc = utils.capitalizeLabel(desc), cardinalityStatement = cardinalityStatement)
    return code

def getTextareaSlotCode(desc, required, propertyName, title, slotCode, html_only):
    multivalued = utils.isMultivalued(slotCode)
    minCardinality = utils.getMinCardinality(slotCode)
    maxCardinality = utils.getMaxCardinality(slotCode)   
    cardinalityStatement = ""
    rows = 2 if html_only else 6

    code = '''<div class="mb-3">
    <div class="input-group">
      <span class="input-group-text width20" id="{propertyName}-addon">{title}</span>
      <textarea rows="{rows}" class="form-control" id="{propertyName}" name="{propertyName}" aria-describedby="{propertyName}-addon {propertyName}-description" {required}></textarea>
    </div>'''.format(propertyName = propertyName, required = required, desc = utils.capitalizeLabel(desc), title = utils.capitalizeLabel(title), rows=rows)

    if (multivalued):
        for i in range(maxCardinality-1):
            code += '''<div class="input-group">
      <span class="input-group-text width20 hideField" id="{propertyName}-addon">{title}</span>
      <textarea rows="{rows}" class="form-control" id="{propertyName}{n}" name="{propertyName}{n}" aria-describedby="{propertyName}-addon {propertyName}-description"></textarea>
    </div>'''.format(propertyName = propertyName, required = required, title = utils.capitalizeLabel(title), n = i+2, rows=rows)
        cardinalityStatement = ''' This field requires at least {minCardinality} value(s)'''.format(minCardinality = minCardinality)


    code += '''<div class="form-text" id="{propertyName}-description">{desc}{cardinalityStatement}</div>
  </div>\n'''.format(propertyName = propertyName, required = required, desc = utils.capitalizeLabel(desc), title = utils.capitalizeLabel(title), cardinalityStatement = cardinalityStatement)
    return code

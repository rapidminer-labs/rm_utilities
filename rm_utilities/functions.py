import pandas as pd
from enum import Enum

nominal_value_list = ['nominal', 'polynominal', 'binominal']
numerical_value_list = ['numeric', 'integer', 'real']


class Datatypes(Enum):
    nominal = 1
    polynominal = 2
    binominal = 3
    numeric = 4
    integer = 5
    real = 6


def get_label(df, metadata):
    """Get the label of the ExampleSet.

    Returns
    -------
    label : pandas data frame
    label_name : String
    """
    label_name = None
    for name, data in metadata.items():
        column_type, column_role = data
        if column_role == "label":
            label_name = name
    if label_name is None:
        raise Exception("The data set needs an attribute of type label. It was not provided.")

    return df[label_name], label_name


def get_regular(df, metadata):
    regular_attributes = []
    for name, data in metadata.items():
        column_type, column_role = data
        if column_role is None:
            regular_attributes.append(name)
    if len(regular_attributes) is 0:
        raise Exception("The data was supposed to have regular attributes, but got none?")

    regular_attributes = sorted(regular_attributes)

    return df[regular_attributes], regular_attributes


def get_special(df, metadata):
    special_attributes = []
    for name, data in metadata.items():
        column_type, column_role = data
        if column_role is not None:
            special_attributes.append(name)
    return df[special_attributes], special_attributes


def get_type(attributeName, metadata):
    return metadata[attributeName][0]


def is_nominal(attributeName, metadata):
    rm_type = metadata[attributeName][0]

    if rm_type in nominal_value_list:
        return True
    return False


def is_binominal(attributeName, metadata, df=None):
    """Returns true if the attribute is binominal.
    If df is not defined this is done using metadata.
    If df is set the data is checked for the type.
    This is helpful because a polynominal or nominal
    attribute can have only 2 classes and thus be bi-nominal.

    Returns
    -------
    label : pandas data frame
    label_name : String
    """
    if df is None:
        rm_type = metadata[attributeName][0]
        if rm_type is "binominal":
            return True
        return False
    else:
        count = df[attributeName].nunique()
        if (count == 2):
            return True
        else:
            return False


def is_numerical(attributeName, metadata):
    rm_type = metadata[attributeName][0]
    if rm_type in numerical_value_list:
        return True
    return False


def set_role(df, attribute_name, role):
    # TODO
    # Roles need to be unique. We don't check this!
    if attribute_name not in df.rm_metadata:
        df.rm_metadata[attribute_name] = ("attribute", role)
    else:
        df.rm_metadata[attribute_name] = (df.rm_metadata[attribute_name][0], role)

    return df

def set_type(df, attribute_name, type):
    #(df.rm_metadata[attribute_name][0], role)
    #df.rm_metadata[attributeName][0] = str(type.name)
    if attribute_name not in df.rm_metadata:
        df.rm_metadata[attribute_name] = (type.name, "regular")
    else:
        df.rm_metadata[attribute_name] = (type.name, df.rm_metadata[attribute_name][1])


def set_roles(df, role_dict):
    for name, role in role_dict.items():
        set_role(df, name, role)
    return df


def process_params(params):
    for i in params.index:
        print(params['type'][i])
        if (params['type'][i] == 'ParameterTypeInt'):
            params['value'][i] = int(params['value'][i])
        elif (params['type'][i] == 'ParameterTypeString'):
            params['value'][i] = __process_parameter_string__(params['value'][i])
        elif (params['type'][i] == 'ParameterTypeDouble'):
            params['value'][i] = float(params['value'][i])
        elif (params['type'][i] == 'ParameterTypeBoolean'):
            params['value'][i] = __process_parameter_string__(params['value'][i])
        elif (params['type'][i] == 'ParameterTypeStringCategory'):
            params['value'][i] = __process_parameter_string__(params['value'][i])
        elif (params['type'][i] == 'ParameterTypeCategory'):
            params['value'][i] = __process_parameter_string__(params['value'][i])

    params_dict = dict(zip(params.key, params.value))
    # replace string None with KeyWord None
    # for key,value in params_dict.items():
    #	if value == 'None':
    #		params_dict[key] = None
    return params_dict


def __process_parameter_string__(strvalue):
    if (strvalue == 'None'):
        strvalue = None
    if strvalue == "True":
        return True
    if strvalue == "False":
        return False
    return strvalue


# def check_capabilities(metadata, capabilities):
#     for availableCapability in get_available_capabilities():
#         if availableCapability not in capabilities:
#             # we need to check
#             if availableCapability == "POLYNOMINAL_ATTRIBUTES":
#                 for name, data in metadata.items():
#                     column_type, column_role = data
#                     if (column_type == "nominal" or column_type == "polynominal"):
#                         raise Exception(
#                             "This operator does not support polynominal data, but got polynominal attribute")
#
#
# def get_available_capabilities():
#     capabilites = []
#     capabilites.append("POLYNOMINAL_ATTRIBUTES")
#     capabilites.append("BINOMINAL_ATTRIBUTES")
#     capabilites.append("WEIGHTED_EXAMPLES")
#     capabilites.append("MISSING_VALUES")
#     capabilites.append("NO_LABEL")
#     capabilites.append("POLYNOMINAL_LABEL")
#     capabilites.append("ONE_CLASS_LABEL")
#     return capabilites


def metadata_to_string(metadata, html=True):
    result_string = "Training header:"
    if html is True:
        result_string += "<br/>"
    for name, data in metadata.items():
        column_type, column_role = data
        if column_role is None:
            column_role = "regular"
        result_string += name + " " + column_role + " " + column_type
        if html is True:
            result_string += "<br/>"
    return result_string

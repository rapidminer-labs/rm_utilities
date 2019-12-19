import pandas as pd


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
    return df[regular_attributes], regular_attributes


def get_special(df, metadata):
    special_attributes = []
    for name, data in metadata.items():
        column_type, column_role = data
        if column_role is not None:
            special_attributes.append(name)
    return df[special_attributes], special_attributes


def get_type(attributeName, metadata):
    raise Exception("Not yet implemented")
    return None


def set_role(df, attribute_name, role):
    # TODO
    # Roles need to be unique. We don't check this!
    if attribute_name not in df.rm_metadata:
        df.rm_metadata[attribute_name] = ("attribute", role)
    else:
        df.rm_metadata[attribute_name] = (df.rm_metadata[attribute_name][0], role)

    return df


def check_capabilities(metadata, capabilities):
    for availableCapability in get_available_capabilities():
        if availableCapability not in capabilities:
            # we need to check
            if availableCapability == "POLYNOMINAL_ATTRIBUTES":
                for name, data in metadata.items():
                    column_type, column_role = data
                    if (column_type == "nominal" or column_type == "polynominal"):
                        raise Exception(
                            "This operator does not support polynominal data, but got polynominal attribute")


def get_available_capabilities():
    capabilites = []
    capabilites.append("POLYNOMINAL_ATTRIBUTES")
    capabilites.append("BINOMINAL_ATTRIBUTES")
    capabilites.append("WEIGHTED_EXAMPLES")
    capabilites.append("MISSING_VALUES")
    capabilites.append("NO_LABEL")
    capabilites.append("POLYNOMINAL_LABEL")
    capabilites.append("ONE_CLASS_LABEL")
    return capabilites


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

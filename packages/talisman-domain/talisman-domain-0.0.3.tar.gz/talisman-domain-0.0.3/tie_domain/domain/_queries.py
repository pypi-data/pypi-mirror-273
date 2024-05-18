common_fields = '''
    id
    name
'''


concept_value_fields = f'''
    {common_fields}
    regexp: listWhiteRegexp {{
        regexp
        context_regexp: contextRegexp
        auto_create: autoCreate
    }}
    black_regexp: listBlackRegexp {{
        regexp
        context_regexp: contextRegexp
        auto_create: autoCreate
    }}
    black_list: listBlackDictionary
    list_white_dictionary: listWhiteDictionary
    pretrained_nerc_models: pretrainedNERCModels
'''

concept_types = f'''
    listConceptType: listConceptType {{
        {concept_value_fields}
        metaType
        list_names_dictionary: listNamesDictionary
    }}
'''


concept_property_value_types = f'''
    listConceptPropertyValueType: listConceptPropertyValueType {{
        {concept_value_fields}
        value_type: valueType
        value_restriction: valueRestriction
    }}
'''

composite_property_value_types = f'''
    listCompositePropertyValueTemplate: listCompositePropertyValueTemplate {{
        {common_fields}
        componentValueTypes {{
            {common_fields}
            valueType {{
                {concept_value_fields}
                value_type: valueType
                value_restriction: valueRestriction
            }}
        }}
    }}
'''

property_link_types = f'''
    {common_fields}
    pretrained_relext_models: pretrainedRelExtModels {{
        source_annotation: sourceAnnotationType
        target_annotation: targetAnnotationType
        invert_direction: invertDirection
        relation_type: relationType
    }}
'''

link_types = f'''
    listConceptPropertyValueType: listConceptLinkType {{
        {property_link_types}
        conceptFromType {{
            id
        }}
        conceptToType {{
            id
        }}
        is_directed: isDirected
    }}
'''

property_types = f'''
    listConceptPropertyValueType: listConceptPropertyType {{
        {property_link_types}
        isIdentifying
        parentConceptType {{
            id
        }}
        parentConceptLinkType {{
            id
        }}
        valueType {{
            ... on ConceptPropertyValueType {{
                id
            }}
            ... on CompositePropertyValueTemplate {{
                id
            }}
        }}
    }}
'''

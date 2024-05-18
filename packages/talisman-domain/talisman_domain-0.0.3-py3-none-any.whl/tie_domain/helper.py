from dataclasses import replace
from functools import singledispatch
from itertools import chain
from typing import Iterator, Optional, Type

from gql import gql
from graphql import DocumentNode
from tdm import TalismanDocument, and_filter, not_filter
from tdm.abstract.datamodel import AbstractDomain, AbstractDomainType, AbstractFact, AbstractLinkFact, FactStatus
from tdm.datamodel.domain import Domain
from tdm.datamodel.facts import AtomValueFact, ComponentFact, CompositeValueFact, ConceptFact, MentionFact, MissedConceptValue, \
    PropertyFact, RelationFact, RelationPropertyFact, ValueFact

from tp_interfaces.domain import get_filters
from tp_interfaces.domain.model.types import ComponentValueType, CompositeValueType, IdentifyingPropertyType


def remove_synthetic_facts(doc: TalismanDocument) -> TalismanDocument:
    """
    Remove facts with synthetic types (account and platforms).
    @param doc: document to be cleaned
    @return: the same document without hacksh facts.
    """
    from tie_domain.domain._synthetic import TYPES
    synthetic_types = {t.id for t in TYPES}

    def _filter(f: AbstractFact) -> bool:
        if not hasattr(f, 'type_id'):
            return False
        type_id = f.type_id
        if isinstance(type_id, AbstractDomainType):
            type_id = type_id.id
        if not isinstance(type_id, str):
            raise ValueError
        return type_id in synthetic_types

    facts_to_remove = tuple(doc.get_facts(filter_=_filter))
    return doc.without_facts(facts_to_remove, cascade=True)


def cleanup_metadata(doc: TalismanDocument) -> TalismanDocument:
    """
    Remove document metadata facts with no normalized value filled (missed document metadata).
    All the metadata facts will have APPROVED status
    @param doc: document to be processed
    @return: the same document with broken metadata cleaned up
    """

    def _has_value(fact: ValueFact) -> bool:
        if isinstance(fact, AtomValueFact):
            return bool(fact.value)
        if isinstance(fact, CompositeValueFact):
            return all(_has_value(comp.target) for comp in doc.related_facts(fact, ComponentFact))
        raise ValueError

    def _approve_value(fact: ValueFact) -> Iterator[AbstractFact]:
        if isinstance(fact, AtomValueFact):
            yield replace(fact, status=FactStatus.APPROVED, value=fact.most_confident_value)
            for f in doc.related_facts(fact):
                yield replace(f, status=FactStatus.APPROVED)
        elif isinstance(fact, CompositeValueFact):
            yield replace(fact, status=FactStatus.APPROVED)
            yield from chain.from_iterable(_approve_value(component.target) for component in doc.related_facts(fact, ComponentFact))
        else:
            raise ValueError

    remove = set()
    changed = set()
    for prop in doc.related_facts(doc.id, PropertyFact):
        value = prop.target
        if not _has_value(value):
            remove.add(value)  # cascade remove with mentions and properties
            continue
        changed.update(_approve_value(value))
    return doc.without_facts(remove, cascade=True).with_facts(changed, update=True)


def replace_auto_facts(doc: TalismanDocument) -> TalismanDocument:
    """
    Change all auto facts status to new
    @param doc: document to be processed
    @return: the same document with updated facts
    """

    def fix_fact(fact: AbstractFact):
        if isinstance(fact, ConceptFact) and isinstance(fact.value, MissedConceptValue):
            return replace(fact, status=FactStatus.NEW, value=tuple())
        return replace(fact, status=FactStatus.NEW)

    return doc.with_facts(
        map(fix_fact, doc.get_facts(filter_=AbstractFact.status_filter(FactStatus.AUTO))),
        update=True
    )


def get_creation_operation(
        fact: ConceptFact, doc: TalismanDocument, doc_kb_id: str, domain: Domain, access_level: str, approved: bool = True
) -> tuple[Optional[DocumentNode], Optional[dict]]:
    """ return getOrAddConceptNew operation with not-approved facts """

    value: MissedConceptValue = fact.most_confident_value
    # now concept can be loaded only with identity property name
    identity_property_type = next(domain.related_types(fact.type_id, IdentifyingPropertyType), None)
    if identity_property_type is None:
        return None, None

    identity_prop: Optional[PropertyFact] = \
        next(doc.related_facts(fact, PropertyFact, filter_=PropertyFact.type_id_filter(identity_property_type.id)), None)
    if identity_prop is None:
        return None, None

    filters = {
        "doc_id": doc_kb_id,
        "access_level": access_level,
        "concept": {"id": fact.id, "approved": approved},
        "identity_prop": {"id": identity_prop.id, "approved": approved},
        "value_id": identity_prop.target.id,
        "filters": [{**get_filters(v.value), 'propertyTypeId': v.type_id, 'propertyType': 'concept'} for v in value.filters],
        "type_id": fact.str_type_id,
    }
    gql_node = gql('''
        mutation crete_new(
            $doc_id: ID!,
            $access_level: ID!,
            $concept: ConceptFactInput!,
            $identity_prop: ConceptPropertyFactInput!,
            $value_id: ID!,
            $filters: [PropertyFilterSettings!],
            $type_id: ID!
        ) {
            getOrAddConceptNew(
                form: {
                    documentId: $doc_id,
                    accessLevelId: $access_level,
                    conceptFact: $concept,
                    conceptPropertyFact: [$identity_prop],
                    propertyValueFact: {id: $value_id}
                }, filterSettings: {propertyFilterSettings: $filters, conceptTypeIds: [$type_id]}
            ) {
                id
            }
        }''')

    return gql_node, filters


def collect_facts_to_approve(doc: TalismanDocument, domain: AbstractDomain) -> Iterator[AbstractFact]:
    """
    Collect fact chains to be approved:
    - concept facts with most confident in-kb value
    - concept relations (both arguments should be already collected)
    - concept properties with normalized values (for all collected concept facts)
    - relation properties with normalized values (the same criteria).
    - value facts with normalized values.

    Value is considered normalized if:
    - it is AtomValueFact with non-empty value list
    - it is CompositeValueFact, and all required components are to be approved (the same criteria as for properties)

    @param doc: document to be processed
    @param domain: document domain
    @return: iterator of the facts to be approved automatically only with new and auto statuses.
    """
    return filter(lambda f: f.status in {FactStatus.AUTO, FactStatus.NEW}, _collect_facts_to_approve(doc, domain))


def _collect_facts_to_approve(doc: TalismanDocument, domain: AbstractDomain) -> Iterator[AbstractFact]:
    """
    Collect both AUTO and APPROVED facts to be sure no dependent auto fact is skipped
    """
    _concepts_filter = [
        ConceptFact.status_filter([FactStatus.NEW, FactStatus.AUTO, FactStatus.APPROVED]),  # we need new/auto/approved facts
        not_filter(ConceptFact.empty_value_filter())  # with no empty value (most confident exists)
    ]

    for concept in doc.get_facts(ConceptFact, filter_=_concepts_filter):
        yield concept  # approve concept fact with in-kb value
        yield from _collect_properties_to_approve(doc, concept, PropertyFact, domain)  # collect all the concept properties

        _relations_filter = [
            RelationFact.status_filter([FactStatus.NEW, FactStatus.AUTO, FactStatus.APPROVED]),  # we need new/auto/approved facts
            RelationFact.source_filter(AbstractFact.id_filter(concept)),  # with fixed source fact (to process each fact once)
            RelationFact.target_filter(and_filter(*_concepts_filter))  # and appropriate target fact
        ]

        for relation in doc.related_facts(concept, RelationFact, filter_=_relations_filter):
            yield relation  # approve relation fact
            yield from _collect_properties_to_approve(doc, relation, RelationPropertyFact, domain)  # collect all the relation properties


def _collect_properties_to_approve(
        doc: TalismanDocument, source: AbstractFact, type_: Type[PropertyFact | RelationPropertyFact], domain: AbstractDomain
) -> Iterator[AbstractFact]:
    """
    Collect properties and values fact to be approved. This method assumes property source is approvable.
    """
    _property_filter = [
        AbstractLinkFact.status_filter([FactStatus.NEW, FactStatus.AUTO, FactStatus.APPROVED]),  # we need new/auto/approved facts
        AbstractLinkFact.target_filter(
            AbstractFact.status_filter([FactStatus.NEW, FactStatus.AUTO, FactStatus.APPROVED]),  # with new/auto/approved value
        )
    ]

    for prop in doc.related_facts(source, type_, filter_=_property_filter):
        facts = _get_value_to_approve(prop.target, doc, domain)
        value = next(facts, None)  # check if property value is ready for approvement
        if value is None:
            continue  # if no value to be approved, don't approve whole property
        yield prop  # orig property
        yield value  # property value
        yield from facts  # all value dependent facts


@singledispatch
def _get_value_to_approve(value: ValueFact, doc: TalismanDocument, domain: AbstractDomain) -> Iterator[AbstractFact]:
    raise NotImplementedError


@_get_value_to_approve.register
def _(value: AtomValueFact, doc: TalismanDocument, domain: AbstractDomain) -> Iterator[AbstractFact]:
    if AtomValueFact.empty_value_filter()(value):
        return

    if not AbstractFact.status_filter([FactStatus.NEW, FactStatus.AUTO, FactStatus.APPROVED])(value):
        return

    yield value  # approve value
    yield from doc.related_facts(value, MentionFact, filter_=MentionFact.status_filter(FactStatus.AUTO))  # and all non-approved mentions


@_get_value_to_approve.register
def _(value: CompositeValueFact, doc: TalismanDocument, domain: AbstractDomain) -> Iterator[AbstractFact]:
    """
    composite value could be approved only with all required components.
    """
    value_type: CompositeValueType = domain.get_type(value.str_type_id)
    components: dict[ComponentValueType, ComponentFact] = {}
    for component in doc.related_facts(value, ComponentFact):  # check if each component has single value
        if component.type_id in components:
            return
        components[component.type_id] = component
    facts = [value]
    for component_type in domain.related_types(value_type, ComponentValueType):
        if component_type in components:
            component = components.pop(component_type)
            to_approve = _get_value_to_approve(component.target, doc, domain)
            value = next(to_approve, None)
            if value is not None:
                facts.extend([component, value, *to_approve])
                continue
        if component_type.isRequired:
            return  # required component is missed
    yield from facts

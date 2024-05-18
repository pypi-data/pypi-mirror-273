import enum
import logging
import os
from typing import Dict, Iterable, Type, TypeVar

from tdm.abstract.datamodel import AbstractDomainType
from tdm.datamodel.domain import Domain
from tdm.datamodel.values import DateTimeValue, DoubleValue, GeoPointValue, IntValue, LinkValue, StringValue, TimestampValue

from tie_domain.domain._queries import (composite_property_value_types, concept_property_value_types, concept_types, link_types,
                                        property_types)
from tie_domain.domain.updates_manager import AbstractDomainUpdatesManager, MANAGERS
from tie_domain.talisman_api import GQLClientConfig, TalismanAPIAdapter
from tp_interfaces.domain.hooks import DOMAIN_CHANGE_HOOKS
from tp_interfaces.domain.interfaces import AbstractDomainChangeHook, DomainProducer
from tp_interfaces.domain.model.types import AtomValueType, ComponentValueType, CompositeValueType, ConceptType, DocumentType, \
    IdentifyingPropertyType, PropertyType, RelationPropertyType, RelationType
from tp_interfaces.logging.time import log_time

logger = logging.getLogger(__name__)

_SYNTHETIC_TYPES = bool(os.getenv('SYNTHETIC_TYPES', True))


class ValueTypes(enum.Enum):
    Date = DateTimeValue
    Double = DoubleValue
    Geo = GeoPointValue
    Int = IntValue
    Timestamp = TimestampValue
    Link = LinkValue
    String = StringValue

    @classmethod
    def get(cls, key: str, default_value=None):
        if key in cls.__members__.keys():
            return cls[key].value
        return default_value


_T = TypeVar('_T', bound=AbstractDomainType)


class TalismanDomainProducer(DomainProducer):
    def __init__(
            self, adapter: TalismanAPIAdapter, updates_manager: AbstractDomainUpdatesManager,
            hooks: Iterable[AbstractDomainChangeHook] = tuple()
    ):
        super().__init__(hooks)
        self._adapter: TalismanAPIAdapter = adapter
        self._updates_manager = updates_manager

    async def __aenter__(self):
        await self._adapter.__aenter__()
        await self._updates_manager.__aenter__()
        return self

    async def __aexit__(self, *exc):
        await self._updates_manager.__aexit__(*exc)
        await self._adapter.__aexit__(*exc)

    @log_time(logger=logger)
    async def has_changed(self) -> bool:
        return await self._updates_manager.has_changed

    @log_time(logger=logger)
    async def _get_domain(self) -> Domain:
        await self._updates_manager.update()  # first we notify manager, that we reload domain

        def make_dictionary(obj) -> dict:
            ret = obj
            ret["dictionary"] = ret.get("list_names_dictionary", []) + ret.get("list_white_dictionary", [])
            return ret

        def build_type(cls: Type[_T], data: dict) -> _T:
            if not hasattr(cls, '__dataclass_fields__'):
                raise TypeError
            fields = cls.__dataclass_fields__

            return cls(**{name: field for name, field in data.items() if name in fields})

        types: dict[str, AbstractDomainType] = {}

        concepts: dict = await self._adapter.pagination_query('paginationConceptType', concept_types)
        concepts: list[dict] = concepts['paginationConceptType']['listConceptType']

        meta_to_concept = {
            'concept': ConceptType,
            'document': DocumentType
        }
        concept_types_ = {build_type(meta_to_concept[c['metaType']], c): make_dictionary(c) for c in concepts}
        types.update(map(lambda t: (t.id, t), concept_types_))

        def set_value_type(obj) -> dict:
            obj['value_type'] = ValueTypes.get(obj['value_type'], obj['value_type'])
            return obj

        values: Dict = await self._adapter.pagination_query('paginationConceptPropertyValueType', concept_property_value_types)
        values = values['paginationConceptPropertyValueType']['listConceptPropertyValueType']

        value_types = (build_type(AtomValueType, set_value_type(make_dictionary(value))) for value in values)
        types.update(map(lambda t: (t.id, t), value_types))

        composite_values: Dict = await self._adapter.pagination_query('paginationCompositePropertyValueTemplate',
                                                                      composite_property_value_types)
        composites = composite_values['paginationCompositePropertyValueTemplate']['listCompositePropertyValueTemplate']

        for composite in composites:
            c = build_type(CompositeValueType, make_dictionary(composite))
            types[c.id] = c

            for component in composite['componentValueTypes']:
                value = build_type(AtomValueType, set_value_type(make_dictionary(component['valueType'])))
                types[value.id] = value
                relation = build_type(ComponentValueType, {**component, 'source': c, 'target': value})
                types[relation.id] = relation

        def build_link_type(cls: Type[_T], obj, source, target) -> _T:
            source = types[source['id']]
            target = types[target['id']]
            obj_dict = obj
            obj_dict.update({'source': source, 'target': target})
            if obj_dict.get('isIdentifying') and obj_dict.get('name', '') == 'Название':
                obj_dict = {**concept_types_[source], **obj_dict}  # add NERC-based fields to main identifying property
            return build_type(cls, obj_dict)

        relations: Dict = await self._adapter.pagination_query('paginationConceptLinkType', link_types)
        relations = relations['paginationConceptLinkType']['listConceptPropertyValueType']

        for relation in relations:
            relation_type = build_link_type(RelationType, relation, relation['conceptFromType'], relation['conceptToType'])
            types[relation_type.id] = relation_type

        properties: Dict = await self._adapter.pagination_query('paginationConceptPropertyType', property_types)
        properties = properties['paginationConceptPropertyType']['listConceptPropertyValueType']

        for property_ in properties:
            type_ = IdentifyingPropertyType if property_['isIdentifying'] else PropertyType
            prop_type = build_link_type(type_, property_, property_['parentConceptType'], property_['valueType'])
            types[prop_type.id] = prop_type

        link_properties: Dict = await self._adapter.pagination_query('paginationConceptLinkPropertyType', property_types)
        link_properties = link_properties['paginationConceptLinkPropertyType']['listConceptPropertyValueType']

        for property_ in link_properties:
            prop_type = build_link_type(RelationPropertyType, property_, property_['parentConceptLinkType'], property_['valueType'])
            types[prop_type.id] = prop_type

        final_types = list(types.values())

        if _SYNTHETIC_TYPES:
            from ._synthetic import TYPES
            final_types.extend(TYPES)
        return Domain(final_types)

    @classmethod
    def from_config(cls, config: dict) -> 'TalismanDomainProducer':
        hooks = []
        for hook_cfg in config.get('hooks', []):
            if isinstance(hook_cfg, str):
                name, cfg = hook_cfg, {}
            elif isinstance(hook_cfg, dict):
                name, cfg = hook_cfg['name'], hook_cfg.get('config', {})
            else:
                raise ValueError
            hooks.append(DOMAIN_CHANGE_HOOKS[name].from_config(cfg))
        updates_cfg = config.get('updates', {})
        updates_manager = MANAGERS[updates_cfg.get('strategy', 'never')].from_config(updates_cfg.get('config', {}))
        return cls(TalismanAPIAdapter(GQLClientConfig(**config['adapter'])), updates_manager, hooks)

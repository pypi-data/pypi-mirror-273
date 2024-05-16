"""
Defining pydantic models for foreground types- in preparation for writing the oryx API (aka. Antelope v2 foreground)

We need:

 Fragment(Entity) <- full record
 FragmentRef(EntityRef) <- minimal (but not even a name?
 FragmentLink (for tree)
 FragmentFlow (for traversal)

and that's probably it

"""
from typing import Dict, Optional, List
from antelope.models import ResponseModel, EntityRef, Entity, FlowEntity
from antelope.xdb_tokens import ResourceSpec


UNRESOLVED_ANCHOR_TYPE = 'term'  # this is used when an anchor node's origin cannot be resolved


class MissingResource(ResponseModel):
    origin: str
    interface: str


class Anchor(ResponseModel):
    """
    An anchor is either: a terminal node designation (i.e. origin + ref) or a context, and a descent marker.
    and cached LCIA scores

    Use FlowTermination.to_anchor(term, ..) to produce
    """
    node: Optional[EntityRef] = None
    anchor_flow: Optional[EntityRef] = None
    context: Optional[List[str]] = None
    descend: bool
    score_cache: Optional[Dict[str, float]] = None

    def __str__(self):
        """
        Replicate FlowTermination

        :return:
          '---:' = fragment I/O
          '-O  ' = foreground node
          '-*  ' = process
          '-#  ' - sub-fragment (aggregate)
          '-#::' - sub-fragment (descend)
          '-B ' - terminated background
          '--C ' - cut-off background
          '--? ' - ungrounded catalog ref

        :return:
        """
        if self.node:
            if self.node.entity_type == 'process':
                return '-*  '
            elif self.node.entity_type == UNRESOLVED_ANCHOR_TYPE:
                return '--? '
            else:
                if self.descend:
                    return '-#::'
                else:
                    return '-#  '
        elif self.context:
            if self.context == ['None']:
                return '-)  '
            else:
                return '-== '
        else:
            return '---:'

    @property
    def type(self):
        if self.node:
            return 'node'
        elif self.context:
            return 'context'
        else:
            return 'cutoff'

    @property
    def unit(self):
        if self.is_null:
            return '--'
        if self.node:
            if self.node.entity_type == 'fragment':
                return '####'
            return '****'
        return '::::'

    @property
    def is_null(self):
        return not bool(self.node or self.context)

    @classmethod
    def null(cls):
        return cls(descend=True)

    def _term_flow_block(self):
        if self.anchor_flow:
            if self.anchor_flow.origin == self.node.origin:
                return self.anchor_flow.entity_id
            else:
                return {
                    'origin': self.anchor_flow.origin,
                    'externalId': self.anchor_flow.entity_id
                }

    def serialize(self):
        """
        emulates FlowTermination.serialize()
        :return:
        """
        if self.context:
            j = {
                'origin': 'foreground',
                'context': self.context[-1]
            }
        else:
            j = {
                'origin': self.node.origin,
                'externalId': self.node.entity_id
            }
        j['descend'] = self.descend
        tfb = self._term_flow_block()
        if tfb:
            j['termFlow'] = tfb
        if self.score_cache:
            j['scoreCache'] = self.score_cache
        return j

    def masquerade(self, masq):
        if self.node:
            if self.node.origin in masq:
                self.node.origin = masq[self.node.origin]
        if self.anchor_flow:
            if self.anchor_flow.origin in masq:
                self.anchor_flow.origin = masq[self.anchor_flow.origin]


class Anchors(ResponseModel):
    anchors: Dict[str, Anchor]

    @classmethod
    def from_fragment(cls, fragment):
        def _default_or(scenario):
            if scenario is None:
                return 'default'
            return str(scenario)

        return cls(anchors={_default_or(k): v.to_anchor(save_unit_scores=False) for k, v in fragment.terminations()})

    def masquerade(self, masq):
        for a in self.anchors.values():
            a.masquerade(masq)


class FragmentRef(Entity):
    """
    From EntityRef, inherits: origin, entity_id (<-external_ref), entity_type, properties
    we ensure put a "name" field because we want users to be able to see what they're getting
    """
    entity_type: str = 'fragment'
    flow: FlowEntity
    direction: str
    entity_uuid: str
    parent: Optional[str] = None

    @property
    def dirn(self):
        return {
            'Input': '-<-',
            'Output': '=>='
        }[self.direction]

    @classmethod
    def from_fragment(cls, fragment, **kwargs):
        """

        :param fragment:
        :param kwargs:
        :return:
        """
        ''' # we don't want this
        if fragment.reference_entity is None:
            dirn = comp_dir(fragment.direction)
        else:
            dirn = fragment.direction
        '''
        dirn = fragment.direction
        if fragment.parent is None:
            parent = None
        else:
            parent = fragment.parent.external_ref

        obj = cls(origin=fragment.origin, entity_id=fragment.external_ref, entity_uuid=fragment.uuid,
                  flow=FlowEntity.from_flow(fragment.flow), direction=dirn, parent=parent, properties=dict())
        obj.properties['name'] = fragment['name']

        for key, val in kwargs.items():
            try:
                obj.properties[key] = fragment[key]
            except KeyError:
                pass
        return obj

    def masquerade(self, masq):
        if self.origin in masq:
            self.origin = masq[self.origin]
        if self.flow.origin in masq:
            self.flow.origin = masq[self.flow.origin]


class FragmentEntity(Entity):
    """
    From Entity, inherits: origin, entity_id (<- external_ref), entity_type, properties
    """
    entity_type: str = 'fragment'
    flow: FlowEntity  # should be full entity or just a ref? this is a full return, it should be full
    direction: str
    parent: Optional[str]
    is_balance_flow: bool

    entity_uuid: str  # we need uuid for consistency since we are running the same LcForeground on the backend

    exchange_values: Dict[str, float]

    anchors: Dict[str, Anchor]

    @classmethod
    def from_entity(cls, fragment, save_unit_scores=False, **kwargs):
        """
        :param fragment:
        :param save_unit_scores:
        :param kwargs:
        :return:
        """
        ''' # we don't want this
        if fragment.reference_entity is None:
            dirn = comp_dir(fragment.direction)
        else:
            dirn = fragment.direction
        '''
        dirn = fragment.direction
        j = fragment.serialize(**kwargs)
        evs = j.pop('exchangeValues')
        evs['cached'] = evs.pop('0')
        evs['observed'] = evs.pop('1')
        terms = {}
        for k, v in fragment.terminations():
            if k is None:
                k = 'default'
            a = v.to_anchor(save_unit_scores=save_unit_scores)
            terms[k] = a
        return cls(origin=fragment.origin, entity_id=fragment.external_ref, properties=j.pop('tags'),
                   entity_uuid=fragment.uuid,
                   flow=FlowEntity.from_flow(fragment.flow), direction=dirn,
                   parent=j.pop('parent'), is_balance_flow=j.pop('isBalanceFlow'),
                   exchange_values=evs, anchors=terms)

    def _serialize_evs(self):
        d = dict(**self.exchange_values)
        d["0"] = d.pop('cached')
        d["1"] = d.pop('observed')
        return d

    def _serialize_terms(self):
        terms = dict()
        for k, v in self.anchors.items():
            if v is None:
                terms[k] = {}
            else:
                terms[k] = v.serialize()
        return terms

    def serialize(self):
        """
        This emulates LcFragment.serialize()
        :return:
        """
        j = {
            'entityType': self.entity_type,
            'externalId': self.entity_id,
            'entityId': self.entity_uuid,
            'parent': self.parent
        }
        if self.flow.origin == self.origin:
            j['flow'] = self.flow.entity_id
        else:
            j['flow'] = '%s/%s' % (self.flow.origin, self.flow.entity_id)
        j['direction'] = self.direction
        j['isPrivate'] = False
        j['isBalanceFlow'] = self.is_balance_flow
        j['exchangeValues'] = self._serialize_evs()
        j['terminations'] = self._serialize_terms()
        j['tags'] = dict(**self.properties)
        return j

    def masquerade(self, masq):
        # I wonder if there is a better way to do this-- surely with a decorator of some sort
        if self.origin in masq:
            self.origin = masq[self.origin]
        if self.flow.origin in masq:
            self.flow.origin = masq[self.flow.origin]
        for a in self.anchors.values():
            a.masquerade(masq)


class FragmentBranch(ResponseModel):
    """
    Used to construct a tree diagram. Reports exchange values only, can be null (if not observable), and no node weights
    (because no traversal)
    """
    parent: Optional[str]
    node: FragmentRef
    name: str
    group: str  # this is the StageName, used for aggregation.. the backend must set / user specify / modeler constrain
    magnitude: Optional[float]
    unit: str
    anchor: Optional[Anchor]
    is_cutoff: bool
    is_balance_flow: bool

    @property
    def term(self):
        if self.anchor is None:
            return Anchor.null()
        return self.anchor

    @property
    def fragment(self):
        return self.node

    @property
    def term_str(self):
        if self.anchor and self.anchor.node:
            if self.node.entity_id == self.anchor.node.entity_id:
                return '-O  '
            return str(self.anchor)
        return '---:'

    @classmethod
    def from_fragment(cls, fragment, scenario=None, observed=False, group='StageName', save_unit_scores=False):
        """

        :param fragment:
        :param scenario:
        :param observed:
        :param group:
        :param save_unit_scores: score_cache must generally not be returned unless some aggregation condition is met
        :return:
        """
        if fragment.observable(scenario):
            mag = fragment.exchange_value(scenario, observed)
        else:
            mag = None
        if fragment.is_balance:
            print(' ## Balance Flow ## %s' % fragment)
        if fragment.reference_entity is None:
            parent = None
        else:
            parent = fragment.reference_entity.external_ref
        term = fragment.termination(scenario)
        anchor = term.to_anchor(save_unit_scores=save_unit_scores)
        if anchor.is_null and len(list(fragment.child_flows)) == 0:
            cutoff = True
        else:
            cutoff = False
        return cls(parent=parent, node=FragmentRef.from_fragment(fragment), name=term.name,
                   group=fragment.get(group, ''),
                   magnitude=mag, unit=fragment.flow.unit, is_balance_flow=fragment.is_balance,
                   anchor=anchor, is_cutoff=cutoff)

    def masquerade(self, masq):
        self.node.masquerade(masq)
        if self.anchor:
            self.anchor.masquerade(masq)


class FragmentFlow(FragmentBranch):
    """
    A FragmentFlow is a record of a link in a traversal. Current controversy: when a flow magnitude or anchor is
    determined by a scenario specification, the FragmentFlow needs to report that.

    Also: whether foreground nodes (anchor = self) actually have anchors (decision: no, the 'foreground is self'
    designation is actually a hack and is redundant. the relevant trait is whether it has child flows, which can be
    known by the constructor)

    hmm except all FragmentFlows have anchors. I think we need to preserve the anchor-is-self, and simply test for it
    when doing operations.

    """
    magnitude: float
    flow_conversion: float
    scenario: Optional[str]
    node_weight: float
    anchor_scenario: Optional[str]
    is_conserved: bool
    subfragments: List = []

    def __str__(self):
        """
        Replicate the FragmentFlow behavior
                return '%.5s  %10.3g [%6s] %s %s' % (self.fragment.uuid, self.magnitude, self.fragment.direction,
                                             self.term, self.name)

        :return:
        """
        if self.anchor is None:
            anc = '---:'
        else:
            anc = str(self.anchor)
            if self.anchor.node:
                if self.anchor.node.entity_id == self.node.entity_id:
                    anc = '-O  '

        return '%.5s  %10.3g [%6s] %s %s' % (self.node.entity_id, self.magnitude, self.node.direction,
                                             anc, self.name)

    @classmethod
    def from_fragment_flow(cls, ff, group=None, save_unit_scores=False):
        """
        The ff is a FragmentFlow generated during a traversal (or tree crawl)
        :param ff:
        :param group:
        :param save_unit_scores: score_cache must generally not be returned unless some aggregation condition is met
        :return:
        """
        if ff.fragment.reference_entity is None:
            parent = None
        else:
            parent = ff.fragment.reference_entity.external_ref
        scen, a_scen = ff.match_scenarios
        if scen in (1, '1', True):
            scen = 'observed'
        if group is None:
            group = 'StageName'
        node = FragmentRef.from_fragment(ff.fragment)
        anchor = ff.term.to_anchor(save_unit_scores=save_unit_scores)
        ff_m = cls(parent=parent, node=node, name=ff.name,
                   group=ff.fragment.get(group, ''),
                   magnitude=ff.magnitude, scenario=scen, unit=ff.fragment.flow.unit, node_weight=ff.node_weight,
                   flow_conversion=ff.flow_conversion,
                   is_balance_flow=ff.fragment.is_balance,
                   is_cutoff=anchor.is_null,
                   is_conserved=ff.is_conserved,
                   anchor=anchor, anchor_scenario=a_scen)
        if anchor.descend:
            ff_m.subfragments = [FragmentFlow.from_fragment_flow(f, group=group, save_unit_scores=save_unit_scores)
                                 for f in ff.subfragments]
        return ff_m

    def masquerade(self, masq):
        self.node.masquerade(masq)
        if self.anchor:
            self.anchor.masquerade(masq)
        for sf in self.subfragments:
            sf.masquerade(masq)


"""
Foreground serialization

1- foreground serialization has shown to be sufficient to reproduce models
2- thus, formalize the serialization


"""


class MicroCf(ResponseModel):
    ref_quantity: str
    value: Dict[str, float]  # locale, CF


class Compartment(ResponseModel):
    name: str
    parent: Optional[str] = None
    sense: Optional[str] = None
    synonyms: List[str]


class Flowable(ResponseModel):
    name: str
    synonyms: List[str]


class TermManager(ResponseModel):
    Characterizations: Dict[str, Dict[str, Dict[str, MicroCf]]]  # query qty, flowable, compartment
    Compartments: List[Compartment]
    Flowables: List[Flowable]

    @classmethod
    def null(cls):
        return cls(Characterizations=dict(), Compartments=[], Flowables=[])


'''
class LcTermination(ResponseModel):
    """
    these became anchors
    """
    externalId: str
    origin: str
    direction: Optional[str]
    termFlow: Optional[str]
    descend: Optional[str]
    context: Optional[str]
'''


class LcModel(ResponseModel):
    fragments: List[FragmentEntity]

    @classmethod
    def from_reference_fragment(cls, fragment, save_unit_scores=False):
        """
        Replicates the save_fragments method of the LcForeground provider
        for packing prior to transmission over HTTP
        """
        def _recurse_frags(f):
            _r = [f]
            for _x in f.child_flows:  # child flows are already ordered
                _r.extend(_recurse_frags(_x))
            return _r

        fragments = [FragmentEntity.from_entity(k, save_unit_scores=save_unit_scores) for k in _recurse_frags(fragment)]
        return cls(fragments=fragments)

    def serialize(self):
        """
        Replicates the LcFragment.serialize() operation
        for unpacking and storing upon receipt over HTTP
        :return:
        """
        return {
            'fragments': [
                k.serialize() for k in self.fragments
            ]
        }


class ForegroundMetadata(ResponseModel):
    version_major: int
    version_minor: int
    dataSource: str
    release_notes: Optional[str] = None
    description: Optional[str] = 'none'
    author: str = 'nobody'


class ForegroundRelease(ResponseModel):
    major: bool = False
    notes: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None


class LcForeground(ResponseModel):

    catalogNames: Dict[str, List[str]]  #
    dataSource: str  #
    dataSourceType: str  #
    flows: List[Dict]  # these should be removed
    initArgs: Dict  #
    quantities: List[Dict]  #
    termManager: Optional[TermManager]  #
    models: List[LcModel]
    resources: List[ResourceSpec]

    @classmethod
    def from_foreground_archive(cls, ar, save_unit_scores=False):
        """
        A simple function to construct a serialized foreground for transmission to an oryx server
        :param ar: an LcForeground archive
        :return: an LcForeground model
        """
        j = ar.serialize(characterizations=True, values=True)
        ms = [LcModel.from_reference_fragment(f, save_unit_scores=save_unit_scores) for f in ar.fragments()]
        rs = []
        return cls(resources=rs, models=ms, **j)

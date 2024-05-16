"""
Client for the oryx Foreground server

This is to be the same as the XdbServer, just with different methods defined
"""
from typing import List

from antelope import UnknownOrigin
from antelope_core.providers.xdb_client import XdbClient, _ref
from antelope_core.providers.xdb_client.xdb_entities import XdbEntity
from antelope_core.implementations import BasicImplementation
from antelope.models import OriginCount, LciaResult as LciaResultModel, EntityRef, FlowEntity

from ..interfaces import AntelopeForegroundInterface
from ..refs.fragment_ref import FragmentRef, ParentFragment

from ..models import (LcForeground, FragmentFlow, FragmentRef as FragmentRefModel, MissingResource,
                      FragmentBranch, FragmentEntity, Anchor)

from requests.exceptions import HTTPError


class MalformedOryxEntity(Exception):
    """
    something is wrong with the entity model
    """
    pass


class OryxEntity(XdbEntity):
    @property
    def uuid(self):
        if hasattr(self._model, 'entity_uuid'):
            return self._model.entity_uuid
        return None

    def make_ref(self, query):
        if self._ref is not None:
            return self._ref

        if self.entity_type == 'fragment':
            """
            This is complicated because there are a couple different possibilities for the model type.
            If the model is a FragmentEntity, then it contains a 'flow' attribute which is actually a FlowEntity,
            but if the model is a FragmentRef, then its flow and direction are stored along with other 
            entity properties, and they will not be converted into pydantic types but kept as dicts
            
            we also need to handle parents, with reference fragments (having None parents) being replaced in the API
            layer with 404 errors and thereby getting caught and replaced with ParentFragment exceptions... 
            
            and also UUIDs which arrive from Entity models as properties and from FragmentRef models as entity_uuid
            attributes
            """
            args = {k: v for k, v in self._model.properties.items()}
            f = args.pop('flow', None)
            d = args.pop('direction', None)
            parent = args.pop('parent', ParentFragment) or ParentFragment
            if hasattr(self._model, 'flow'):
                the_origin = self._model.flow.origin
                the_id = self._model.flow.entity_id
                direction = self._model.direction
                args['uuid'] = self._model.entity_uuid
            else:
                if f is None:
                    print(self._model.model_dump_json(indent=2))
                    raise MalformedOryxEntity(self.link)
                the_origin = f['origin']
                the_id = f['entity_id']
                direction = d

            if hasattr(self._model, 'parent'):
                parent = self._model.parent or ParentFragment

            try:
                flow = query.cascade(the_origin).get(the_id)  # get locally
            except UnknownOrigin:
                flow = query.get(the_id, origin=the_origin)  # get remotely

            if self.origin != query.origin:
                args['masquerade'] = self.origin

            ref = FragmentRef(self.external_ref, query,
                              flow=flow, direction=direction, parent=parent, **args)

            if hasattr(self._model, 'anchors'):
                ref.anchors(**self._model.anchors)

            self._ref = ref
            return ref

        return super(OryxEntity, self).make_ref(query)


class OryxClient(XdbClient):

    _base_type = OryxEntity

    def __init__(self, *args, catalog=None, **kwargs):
        """
        Not sure we need the catalog yet, but LcResource gives it to us, so let's hold on to it
        :param args:
        :param catalog:
        :param kwargs:
        """
        self._catalog = catalog
        super(OryxClient, self).__init__(*args, **kwargs)

    @property
    def query(self):
        return self._catalog.query(self.ref)

    def make_interface(self, iface):
        if iface == 'foreground':
            return OryxFgImplementation(self)
        return super(OryxClient, self).make_interface(iface)

    def _model_to_entity(self, model):
        if model.entity_type == 'fragment':
            ''' check for flow spec '''
            if hasattr(model, 'flow'):
                self.get_or_make(model.flow)
            else:
                if hasattr(model, 'properties') and 'flow' in model.properties:
                    self.get_or_make(FlowEntity(**model.properties['flow']))
                else:
                    model = self._requester.origin_get_one(FragmentEntity, model.origin, 'fragments',
                                                           model.entity_id)
                    self.get_or_make(model.flow)

        ent = super(OryxClient, self)._model_to_entity(model)
        if ent.uuid is not None:
            self._entities[ent.uuid] = ent
        return ent


class OryxFgImplementation(BasicImplementation, AntelopeForegroundInterface):
    """
    We don't need to REimplement anything in XdbClient because oryx server should behave the same to the same routes
    (but that means we need to reimplement everything in OryxServer)
    """
    def _o(self, obj=None):
        """
        Key difference between the Xdb implementation is: the xdb implementation is strongly tied to its origin,
        but the foreground can refer to entities with various origins.

        To handle this, we *masquerade* the query (to the primary origin) with the entity's authentic origin (just as
        we do with local.qdb). this happens automatically in entity.make_ref() when the query origin doesn't match the
        entity origin

        then in our requester we unset_origin() and issue origin, ref explicitly.

        _o is the mechanism for this.

        Implies that client code is expected to supply a true entity and not a string ref-- this is potentially a
        problem

        returns either the object's origin, if it is an object, or the archive's ref

        :param obj:
        :return:
        """
        if hasattr(obj, 'origin'):
            return obj.origin
        return self._archive.ref

    @property
    def delayed(self):
        return self._archive.delayed

    @property
    def unresolved(self):
        return self._archive.unresolved

    def get(self, external_ref, **kwargs):
        print('I have a theory this tranche of code never gets run %s' % external_ref)
        return self._archive.query.get(external_ref, **kwargs)

    # foreground resource operations-- non-masqueraded
    def fragments(self, **kwargs):
        llargs = {k.lower(): v for k, v in kwargs.items()}
        return [self._archive.get_or_make(k) for k in self._archive.r.get_many(FragmentRefModel, 'fragments', **llargs)]

    def post_foreground(self, fg, save_unit_scores=False):
        pydantic_fg = LcForeground.from_foreground_archive(fg.archive, save_unit_scores=save_unit_scores)
        return self._archive.r.post_return_one(pydantic_fg.dict(), OriginCount, 'post_foreground')

    def post_entity_refs(self, entities, **kwargs):
        post_ents = [p if isinstance(p, EntityRef) else EntityRef.from_entity(p) for p in entities]
        return self._archive.r.post_return_one([p.model_dump() for p in post_ents], OriginCount, 'entity_refs')

    def save(self):
        return self._archive.r.post_return_one(None, bool, 'save_foreground')

    def restore(self):
        return self._archive.r.post_return_one(None, bool, 'restore_foreground')

    def missing(self):
        return self._archive.r.origin_get_many(MissingResource, 'missing')  # no origin required

    # Entity operations- masqueraded
    def get_reference(self, key):
        try:
            # !TODO! key will always be an external_ref so _o(key) will fail
            parent = self._archive.r.origin_get_one(FragmentRefModel, self._o(key), _ref(key), 'reference')
        except HTTPError as e:
            if e.args[0] == 400:
                raise ParentFragment
            raise e
        return self._archive.get_or_make(parent)

    def get_fragment(self, fragment):
        """
        detailed version of a fragment
        :param fragment:
        :return:
        """
        return self._archive.r.origin_get_one(FragmentEntity, self._o(fragment), 'fragments', _ref(fragment))

    def child_flows(self, fragment, **kwargs):
        return [self._archive.get_or_make(k) for k in self._archive.r.origin_get_many(FragmentRefModel,
                                                                                      self._o(fragment),
                                                                                      'fragments', _ref(fragment),
                                                                                      'child_flows')]

    def top(self, fragment, **kwargs):
        return self._archive.get_or_make(self._archive.r.origin_get_one(FragmentRefModel,
                                                                        self._o(fragment), _ref(fragment), 'top'))

    def anchors(self, fragment, **kwargs):
        a = self._archive.r.origin_get_one(dict, self._o(fragment), 'fragments', _ref(fragment), 'anchors')
        return {k: Anchor(**v) for k, v in a.items()}

    def scenarios(self, fragment, **kwargs):
        return self._archive.r.origin_get_many(str, self._o(fragment), _ref(fragment),
                                               'scenarios', **kwargs)

    def _get_or_make_fragment_flows(self, ffs):
        """
        whoo-ee we love danger
        :param ffs:
        :return:
        """
        for ff in ffs:
            subfrags = [FragmentFlow(**f) for f in ff.subfragments]
            self._get_or_make_fragment_flows(subfrags)
            self._archive.get_or_make(ff.node)

    def traverse(self, fragment, scenario=None, **kwargs):
        ffs = self._archive.r.origin_get_many(FragmentFlow, self._o(fragment), _ref(fragment),
                                              'traverse', scenario=scenario, **kwargs)

        self._get_or_make_fragment_flows(ffs)

        return ffs

    def activity(self, fragment, scenario=None, **kwargs):
        return self._archive.r.origin_get_many(FragmentFlow, self._o(fragment), _ref(fragment),
                                               'activity', scenario=scenario, **kwargs)

    def tree(self, fragment, scenario=None, **kwargs):
        return self._archive.r.origin_get_many(FragmentBranch, self._o(fragment), _ref(fragment),
                                               'tree', scenario=scenario, **kwargs)

    def fragment_lcia(self, fragment, quantity_ref, scenario=None, mode=None, **kwargs):
        if mode == 'detailed':
            return self.detailed_lcia(fragment,quantity_ref, scenario=scenario, **kwargs)
        elif mode == 'flat':
            return self.flat_lcia(fragment, quantity_ref, scenario=scenario, **kwargs)
        elif mode == 'stage':
            return self.stage_lcia(fragment, quantity_ref, scenario=scenario, **kwargs)
        elif mode == 'anchor':
            return self.anchor_lcia(fragment, quantity_ref, scenario=scenario, **kwargs)
        return self._archive.r.origin_get_many(LciaResultModel, self._o(fragment), 'fragments', _ref(fragment),
                                               'fragment_lcia',
                                               _ref(quantity_ref), scenario=scenario, **kwargs)

    def detailed_lcia(self, fragment, quantity_ref, scenario=None, **kwargs):
        return self._archive.r.origin_get_many(LciaResultModel, self._o(fragment), 'fragments', _ref(fragment),
                                               'detailed_lcia',
                                               _ref(quantity_ref), scenario=scenario, **kwargs)

    def flat_lcia(self, fragment, quantity_ref, scenario=None, **kwargs):
        return self._archive.r.origin_get_many(LciaResultModel, self._o(fragment), 'fragments', _ref(fragment),
                                               'lcia',
                                               _ref(quantity_ref), scenario=scenario, **kwargs)

    def stage_lcia(self, fragment, quantity_ref, scenario=None, **kwargs):
        return self._archive.r.origin_get_many(LciaResultModel, self._o(fragment), 'fragments', _ref(fragment),
                                               'stage_lcia',
                                               _ref(quantity_ref), scenario=scenario, **kwargs)

    def anchor_lcia(self, fragment, quantity_ref, scenario=None, **kwargs):
        return self._archive.r.origin_get_many(LciaResultModel, self._o(fragment), 'fragments', _ref(fragment),
                                               'anchor_lcia',
                                               _ref(quantity_ref), scenario=scenario, **kwargs)

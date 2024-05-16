from antelope import UnknownOrigin
from antelope_core.archives import InterfaceError
from antelope_core.catalog import LcCatalog
from .foreground_query import ForegroundQuery, ForegroundNotSafe, MissingResource

from itertools import chain
import shutil
import os
import re
import tempfile


foreground_origin_regexp = re.compile('^[A-Za-z0-9_-]+(\.[A-Za-z0-9_-]+)*$')
savefile_regexp = re.compile('^([A-Za-z0-9_-]+(\.[A-Za-z0-9_-]+)*)\.(\d+)\.(\d+)\.zip$')


class BackReference(Exception):
    """
    trying to instantiate a foreground that's currently being loaded
    """
    pass


class NoSuchForeground(Exception):
    """
    foregrounds must be explicitly created
    """
    pass


class OriginDependencies(object):
    """
    This class stores records of references made from one origin (host) to another (dependency), detected
    whenever an LcForeground
    """
    def __init__(self):
        self._deps = set()  #

    @property
    def all(self):
        for d in sorted(self._deps):
            yield d

    def add_dependency(self, host, dependency):
        self._deps.add((str(host), str(dependency)))

    def dependencies(self, host):
        for h, d in sorted(self._deps):
            if h == host:
                yield d

    def recursive_dependencies(self, *hosts):
        """
        we want all the downstream dependencies but without repeating or entering an endless loop
        :param hosts:
        :return:
        """
        hosts_seen = set()
        deps_seen = set()
        queue = list(hosts)
        while len(queue) > 0:  # this sort of construction always gives me a thrill
            h = queue.pop(0)
            if h in hosts_seen:
                continue
            hosts_seen.add(h)
            for d in self.dependencies(h):
                queue.append(d)
                if d not in deps_seen:
                    deps_seen.add(d)
                    yield d

    def referents(self, dependency):
        for h, d in sorted(self._deps):
            if d == dependency:
                yield h


class ForegroundCatalog(LcCatalog):
    """
    Adds the ability to create (and manage?) foreground resources

    Maintains two different lists of resources that have been encountered but not yet resolved:

     _fg_queue is a set of foregrounds (that may reference one another)- they can be added to the queue
      when referenced, and their queries will resolve once the queue is processed, which will happen within
      a single query evaluation

     _missing_o is a set of (origin, interface) 2-tuples that have been requested but are not found. They must
      be removed from the set when a resource is added to fulfill them.
    """

    '''
    ForegroundCatalog
    '''
    def __init__(self, *args, **kwargs):
        self._fg_queue = set()  # fgs we are *currently* opening
        self._missing_o = set()  # references we have encountered that we cannot resolve
        self._dependencies = OriginDependencies()
        super(ForegroundCatalog, self).__init__(*args, **kwargs)

    @property
    def dependencies(self):
        for d in self._dependencies.all:
            yield d

    def _check_missing_o(self, res):
        for iface in res.interfaces:
            key = (res.origin, iface)
            if key in self._missing_o:
                self._missing_o.remove(key)

    def new_resource(self, reference, source, ds_type, store=True, **kwargs):
        res = super(ForegroundCatalog, self).new_resource(reference, source, ds_type, store=store, **kwargs)
        self._check_missing_o(res)
        return res

    def add_resource(self, resource, **kwargs):
        super(ForegroundCatalog, self).add_resource(resource, **kwargs)
        self._check_missing_o(resource)

    def is_in_queue(self, home):
        """
        This tells us whether the foreground named in home is actively being instantiated
        :param home:
        :return:
        """
        return home in self._fg_queue

    def is_missing(self, origin, interface):
        """
        This tells us whether the named origin, interface tuple is in our list of missing references
        :param origin:
        :param interface:
        :return:
        """
        return origin, interface in self._missing_o

    @property
    def missing_resources(self):
        for k in self._missing_o:
            yield k

    '''
    def delete_foreground(self, ref):
        """
        
        :param ref: 
        :return: 
        """
        """
        Creates or activates a foreground as a sub-folder within the catalog's root directory.  Returns a
        Foreground interface.
        :param path: either an absolute path or a subdirectory path relative to the catalog root
        :param ref: semantic reference (optional)
        :param quiet: passed to fg archive
        :param reset: [False] if True, clear the archive and create it from scratch, before returning the interface
        :param delete: [False] if True, delete the existing tree completely and irreversibly. actually just rename
        the directory to whatever-DELETED; but if this gets overwritten, there's no going back.  Overrides reset.
        :return:
        if localpath:
            if os.path.exists(localpath):
                del_path = localpath + '-DELETED'
                if os.path.exists(del_path):
                    rmtree(del_path)
                os.rename(abs_path, del_path)
        dels = [k for k in self._resolver.resolve(ref, interfaces='foreground')]
        """
        dels = [k for k in self._resolver.resolve(ref, interfaces='foreground')]
        for k in dels:
            self.delete_resource(k, delete_source=True, delete_cache=True)
    '''

    def gen_interfaces(self, origin, itype=None, strict=False, ):
        """
        Override parent method to also create local backgrounds
        :param origin:
        :param itype:
        :param strict:
        :return:
        """
        if origin in self.foregrounds:
            for res in self._sorted_resources(origin, itype, strict):
                '''
                self._fg_queue.add(origin)
                res.check(self)
                self._fg_queue.remove(origin)
                '''
                try:
                    self._check_foreground(res)
                    yield res.make_interface(itype)
                except InterfaceError:
                    continue

        elif (origin, itype) in self._missing_o:
            raise MissingResource(origin, itype)

        else:
            try:
                for k in super(ForegroundCatalog, self).gen_interfaces(origin, itype=itype, strict=strict):
                    yield k
            except (UnknownOrigin, InterfaceError):
                self._missing_o.add((origin, itype))
                raise MissingResource(origin, itype)

    @property
    def test(self):
        return bool(self._test)

    def create_foreground(self, ref, path=None, quiet=True):
        """
        Creates foreground resource and returns an interface to that resource.
        By default creates in a subdirectory of the catalog root with the ref as the folder
        :param ref:
        :param path:
        :param quiet:
        :return:
        """
        assert bool(foreground_origin_regexp.match(ref)), "Foreground reference not valid: %s" % ref
        if self._test:
            local_path = ref
        else:
            if path is None:
                path = os.path.join(self._rootdir, ref)  # should really sanitize this somehow
                # localpath = ref
            else:
                if os.path.isabs(path):
                    pass
                    # localpath = None
                else:
                    # localpath = path
                    path = os.path.join(self._rootdir, path)

            abs_path = os.path.abspath(path)
            local_path = self._localize_source(abs_path)

        res = self.new_resource(ref, local_path, 'LcForeground',
                                interfaces=['basic', 'index', 'foreground', 'quantity'],
                                quiet=quiet)

        return self._check_foreground(res)

    def foreground(self, ref, reset=False):
        """
        activates a foreground resource and returns a query interface to that resource.
        :param ref:
        :param reset: re-load the foreground from the saved files
        :return:
        """
        if ref in self._fg_queue:
            raise BackReference(ref)

        try:
            res = next(self._resolver.resolve(ref, interfaces='foreground'))
        except (UnknownOrigin, StopIteration):
            raise NoSuchForeground(ref)

        if reset:
            self.purge_resource_archive(res)

        return self._check_foreground(res)

    def _get_target_abspath(self, target_dir=None):
        if target_dir is None:
            target_dir = self.root
        else:
            target_dir = os.path.abspath(target_dir)
            if not os.path.isdir(target_dir):
                raise NotADirectoryError(target_dir)
        return target_dir

    def _saved_versions(self, foreground, target_dir=None):
        """
        Generates a list of versioned foreground savefiles for the named foreground, as produced by write_versioned_fg,
        in REVERSE ORDER (most recent first), sorted by the numeric values of the major and minor version numbers.

        This routine hard-codes the filename convention of (foreground origin).(major version).(minor version).zip
        and conventional usage assumes all files can be found in the catalog's root directory
        :param foreground:
        :param target_dir: specify where to look for saved versions (default cat.root)
        :return:
        """
        def _make_sortable(filename):
            """
            here we have to take something that says "my.origin.[majorversion].[minorversion]" and make it so that
            [majorversion].10 appears after [majorversion].1 IN GENERAL

            so we pad using %d.%04d and we prohibit more than 9,999 minor versions

            :param filename:
            :return:
            """
            g = savefile_regexp.match(filename).groups()
            return float('%d.%04d' % (int(g[-2]), int(g[-1])))

        candidates = [file for file in sorted(os.listdir(self._get_target_abspath(target_dir))) if
                      bool(savefile_regexp.match(file)) and savefile_regexp.match(file).groups()[0] == foreground]

        for save in sorted(candidates, key=lambda x: _make_sortable(x), reverse=True):
            yield save

    @staticmethod
    def _restore_foreground_zip_to(source_file, target):
        print('Unpacking lastsave %s to %s' % (source_file, target))
        os.makedirs(target)
        shutil.unpack_archive(source_file, extract_dir=target)

    def restore_foreground_by_version(self, foreground, major_version, minor_version=0, target_dir=None, force=False):
        target_dir = self._get_target_abspath(target_dir)
        ref = '%s.%d.%d' % (foreground, major_version, minor_version)
        file = os.path.join(target_dir, '%s.zip' % ref)
        try:
            res = self.get_resource(ref)
            target = res.source
        except UnknownOrigin:
            target = os.path.join(target_dir, ref)
        if os.path.exists(file):
            if os.path.exists(target):
                if force:
                    if os.path.isdir(target_dir):
                        shutil.rmtree(target)
                    else:
                        os.remove(target)
                else:
                    raise FileExistsError(target)
            self._restore_foreground_zip_to(file, target)
            return self.create_foreground(ref, path=target)
        else:
            raise FileNotFoundError(file)

    def _check_foreground(self, res):
        """
        finish foreground activation + return QUERY interface
        If the foreground source directory doesn't exist, BUT at least one versioned save file DOES exist, the highest-
        versioned save file is expanded and renamed to the foreground source directory.
        :param res:
        :return:
        """
        ref = res.origin

        abs_source = self.abs_path(res.source)

        if not os.path.exists(abs_source):
            try:
                lastsave = next(self._saved_versions(ref))
                savedir, ext = os.path.splitext(lastsave)
                assert ext == '.zip'
                assert savedir.startswith(ref)

                source_file = os.path.join(self._rootdir, lastsave)

                self._restore_foreground_zip_to(source_file, abs_source)

            except StopIteration:
                # no save files
                pass

        self._fg_queue.add(ref)
        res.check(self)
        self._fg_queue.remove(ref)

        if ref not in self._queries:
            self._seed_fg_query(ref)

        return self._queries[ref]

    def flush_backreference(self, origin):
        if origin in self._fg_queue:
            self._fg_queue.remove(origin)

    @property
    def foregrounds(self):
        f = set()
        for k in self.interfaces:
            org, inf = k.split(':')
            if inf == 'foreground' and org not in f:
                yield org
                f.add(org)

    def write_versioned_fg(self, foreground, target_dir=None, force=False):
        target_dir = self._get_target_abspath(target_dir)

        ar = self.get_archive(foreground)
        new_ref = '.'.join([foreground, str(ar.metadata.version_major), str(ar.metadata.version_minor)])
        new_path = os.path.join(target_dir, new_ref)

        if force:
            if os.path.isdir(new_path):
                shutil.rmtree(new_path)
        else:
            fname = new_path + '.zip'
            if os.path.exists(fname):
                raise FileExistsError(fname)
            if os.path.isdir(new_path):
                raise IsADirectoryError(new_path)

        shutil.copytree(ar.source, new_path)
        zipfile = shutil.make_archive(new_path, format='zip', root_dir=new_path)
        shutil.rmtree(new_path)
        return zipfile

    '''
    def assign_new_origin(self, old_org, new_org):
        """
        This only works for certain types of archives. Foregrounds, in particular. but it is hard to say what else.
        What needs to happen here is:
         - first we retrieve the archive for the ref (ALL archives?)
         - then we call set_origin() on the archive
         - then we save the archive
         - then we rename the resource file
         = actually we just rewrite the resource file, since the filename and JSON key have to match
         = since we can't update resource origins, it's easiest to just blow them away and reload them
         = but to save time we should transfer the archives from the old resource to the new resource
         = anyway, it's not clear when we would want to enable this operation in the first place.
         * so for now we leave it
        :param old_org:
        :param new_org:
        :return:
        """
        pass

    def configure_resource(self, reference, config, *args):
        """
        We must propagate configurations to internal, derived resources. This also begs for testing.
        :param reference:
        :param config:
        :param args:
        :return:
        """
        # TODO: testing??
        for res in self._resolver.resolve(reference, strict=False):
            abs_src = self.abs_path(res.source)
            if res.add_config(config, *args):
                if res.internal:
                    if os.path.dirname(abs_src) == self._index_dir:
                        print('Saving updated index %s' % abs_src)
                        res.archive.write_to_file(abs_src, gzip=True,
                                                  exchanges=False, characterizations=False, values=False)
                else:
                    print('Saving resource configuration for %s' % res.origin)
                    res.save(self)

            else:
                if res.internal:
                    print('Deleting unconfigurable internal resource for %s\nsource: %s' % (res.origin, abs_src))
                    self.delete_resource(res, delete_source=True)
                else:
                    print('Unable to apply configuration to resource for %s\nsource: %s' % (res.origin, res.source))

    def delete_foreground(self, foreground, really=False):
        res = self.get_resource(foreground, 'foreground')
        self.delete_resource(res)
        abs_src = self.abs_path(res.source)
        if really:
            shutil.rmtree(abs_src)
        else:
            del_path = abs_src + '-DELETED'
            if os.path.exists(del_path):
                shutil.rmtree(del_path)

            os.rename(abs_src, del_path)
    '''

    def _seed_fg_query(self, origin, **kwargs):
        self._queries[origin] = ForegroundQuery(origin, catalog=self, **kwargs)

    def query(self, origin, strict=False, refresh=False, **kwargs):
        if origin in self.foregrounds:
            if origin not in self._queries:
                # we haven't loaded this fg yet, so
                raise ForegroundNotSafe(origin)
            if origin in self._fg_queue:
                raise BackReference(origin)
            if refresh or (origin not in self._queries):
                self._seed_fg_query(origin, **kwargs)
            return self._queries[origin]

        return super(ForegroundCatalog, self).query(origin, strict=strict, refresh=refresh, **kwargs)

    def internal_ref(self, fg_ref, origin, external_ref):
        """
        for use by an LcForeground provider to obtain a reference to an entity from a separate origin
        :param fg_ref: referring foreground ref
        :param origin:
        :param external_ref:
        :return:
        """
        self._dependencies.add_dependency(fg_ref, origin)
        try:
            return self.query(origin).get(external_ref)
        except UnknownOrigin:
            self._missing_o.add((origin, 'basic'))
            raise MissingResource(origin, 'basic')
        # don't catch EntityNotFound

    '''
    Parameterization
    Observing fragments requires the catalog because observations can come from different resources.
    '''

    def apply_observation(self, scenario, fragment, obs, default_fg=None):
        """

        :param scenario:
        :param fragment:
        :param obs:
        :param default_fg:
        :return:
        """
        if isinstance(obs, str):
            term = default_fg.find_term(obs)
            fragment.observe(scenario=scenario, termination=term)
        elif isinstance(obs, tuple):
            origin, ref = obs
            term = self.query(origin).get(ref)
            fragment.observe(scenario=scenario, termination=term)
        else:
            fragment.observe(obs, scenario=scenario)

    def apply_ad_hoc_parameter(self, adhoc_scenario, param_spec, factor, default_fg=None, mult=True):
        """
        Apply an ad hoc parameterization to a uniquely specified child fragment.  User must specify:
         - the name or external ref of the parent fragment
         - the external ref of the child flow

        User may optionally specify:
         - the foreground that contains the fragment [default_fg must be provided]
         - the observed scenario that should be altered [default is base case]

        The routine will find the unique child flow, retrieve its observed exchange value, multiply it by the factor,
        and enter a new observation under the adhoc_scenario.

        If 'mult=False' is supplied, then the parameter is applied as-is, without multiplication (in this case, any
        reference scenario specification is ignored)

        :param adhoc_scenario: the scenario under which the ad hoc parameter will be observed
        :param param_spec: A tuple having 2, 3, or 4 elements:
         2-element: (fragment_ref, flow_ref) using default_fg, default (observed) reference scenario
         3-element: (origin, fragment_ref, flow_ref) using default scenario [if origin is found in cat.foregrounds]
         3-element: (fragment_ref, flow_ref, scenario) using default_fg [if origin is not found in cat.foregrounds]
         4-element: (origin, fragment_ref, flow_ref, reference_scenario)
        :param factor: The value by which to multiply the base exchange value
        :param default_fg: used when origin is not specified; not required if origin is provided
        :param mult: If True (default), the factor is multiplicative and applied to the adhoc_scenario (future:
        applied to fragment multiplicative root param). if false, is applied directly to the adhoc_scenario.
        :return:
        """
        if len(param_spec) == 2:  # (fragment, child_flow)
            fg = default_fg
            frag, child = param_spec
            sc = None
        elif len(param_spec) == 3:  # (origin, fragment, child_flow)
            if param_spec[0] in self.foregrounds:
                org, frag, child = param_spec
                fg = self.foreground(org)
                sc = None
            else:
                fg = default_fg
                frag, child, sc = param_spec
        elif len(param_spec) == 4:
            org, frag, child, sc = param_spec
            fg = self.foreground(org)
        else:
            print('%s: skipping unrecognized ad hoc parameter %s' % (adhoc_scenario, param_spec))
            return
        if fg is None:
            print('%s: unknown or unspecified foreground for ad hoc param %s' % (adhoc_scenario, param_spec))
            return
        tgt = fg[frag]
        if tgt is None:
            print('%s: Unable to retrieve fragment %s' % (adhoc_scenario, param_spec))
            return
        flow = fg.get_local(child)
        cfs = list(tgt.children_with_flow(flow))
        if len(cfs) == 1:
            cf = cfs[0]
            if mult:
                base_value = cf.exchange_value(scenario=sc, observed=True)
                try:
                    value = base_value * factor
                    fg.observe(cf, value, scenario=adhoc_scenario)
                except TypeError:  # if 'factor' is not a float, it's interpreted as a termination
                    self.apply_observation(adhoc_scenario, cf, factor, default_fg=default_fg)
            else:
                self.apply_observation(adhoc_scenario, cf, factor, default_fg=default_fg)
        elif len(cfs) == 0:
            print('%s: no child flow found %s' % (adhoc_scenario, param_spec))
        else:
            print('%s: too many (%d) child flows found %s' % (adhoc_scenario, len(cfs), child))
            print('Or, actually, maybe the thing to do is to paramaterize ALL of them!')

    def set_scenario_knobs(self, scenarios, *foregrounds):
        """
        Apply parameter values to a set of "knobs" (fragment names) to define scenarios.
        Note: if "knob name" is a tuple, interpret it as an ad hoc parameterization, specifying the parent fragment,
        the child to parameterize, and the optional scenario case to be altered.  Ad hoc parameters are multiplicative,
        meaning they are applied to the existing value and not interpreted as absolute values.  This means they
        cannot be used to parameterize zero-valued cases.
        ([origin], parent fragment, child flow, [scenario])
        :param scenarios: (dict of dicts) mapping of scenario names to {knob name: value} mappings - a scenario will
         be created for each key, with the corresponding knobs set to spec.  Use 'scenario': True to add scenario
         flags
        :param foregrounds: use to specify where to draw named knobs from.  First one listed is the default.
        If all knobs are specified 'ad hoc', no foregrounds are required
        :return: None
        """
        if scenarios is None or len(scenarios) == 0:
            return
        # this is ALL OF THEM
        knobs = {k.external_ref: k for k in chain(*(z.knobs() for z in foregrounds))
                 if not k.external_ref.startswith('__')}

        if foregrounds:
            default_fg = foregrounds[0]
        else:
            default_fg = None

        for k, vd in scenarios.items():

            if vd is None:
                continue

            for i, v in vd.items():
                if v is True:
                    # valid setting at runtime; nothing to do here
                    continue
                if i in knobs:
                    self.apply_observation(k, knobs[i], v, default_fg=default_fg)
                elif isinstance(i, tuple):
                    self.apply_ad_hoc_parameter(k, i, v, default_fg=default_fg)
                else:
                    print('%s: Skipping unknown scenario key %s=%g' % (k, i, v))


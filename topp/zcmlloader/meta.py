from ConfigParser import NoSectionError
from ConfigParser import ConfigParser
from zope.configuration import xmlconfig
import pkg_resources as pkr
from zope.interface import Interface
from zope.schema import BytesLine
from zope.schema import TextLine
import os


class IOpencoreConfigFile(Interface):
    """a config file to load up"""
    file = BytesLine(
        title=u'Configuration file name',
        description=u'Name of a configuration file to be loaded',
        required=True)

class IOpencoreEntryPoints(Interface):
    """an entry point group to load up"""
    group = TextLine(
        title=u'Entry point group name',
        description=u'Name of an entry point group to be loaded',
        required=True)

class IIncludes(Interface):
    zcmlgroup = TextLine(
        title=u"ZCML Group",
        description=u"File group to be loaded",
        required=True,
        default=u'configure.zcml'
        )


class IIncludeOverrides(Interface):
    zcmlgroup = TextLine(
        title=u"ZCML Group",
        description=u"File group to be loaded",
        required=True,
        default=u'overrides.zcml'
        )


_opencore_config = None

def load_opencore_config(_context, file=None):
    global _opencore_config
        
    if file is None:
        # do default?
        pass
    cp = ConfigParser()
    cp.read(file)
    _opencore_config = cp

def load_entry_points(_content, group=None):
    global _opencore_config

    if group is None:
        # do default?
        pass

    for ep in pkr.iter_entry_points(group):
        dist = ep.dist
        dist_name = dist.project_name
        module = ep.load()
        import types
        if not isinstance(module, types.ModuleType):
            continue
        path = module.__path__[0]
        if not path.endswith(os.sep):
            path = path + os.sep
        _opencore_config.set(ep.name, dist_name, path)

def load(_context, zcmlgroup='configure.zcml', override=False):
    global _opencore_config
    include = xmlconfig.include
    if override:
        include = xmlconfig.includeOverrides
    cp = _opencore_config
    try:
        items = cp.items(zcmlgroup)
    except NoSectionError:
        print "no section: %s" %zcmlgroup
        return

    for dist, filename in items:
        req = pkr.Requirement.parse(dist)
        if filename.endswith(os.sep):
            filename = os.path.join(filename, zcmlgroup)
        include(_context, filename)

def load_overrides(_context, zcmlgroup='overrides.zcml'):
    load(_context, zcmlgroup, override=True)
    
def get_opencore_config(self):
    return _opencore_config

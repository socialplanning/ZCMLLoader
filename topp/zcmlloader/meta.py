from ConfigParser import NoSectionError
from ConfigParser import ConfigParser
from zope.configuration import xmlconfig
import pkg_resources as pkr
from zope.interface import Interface
from zope.schema import BytesLine
from zope.schema import TextLine
from zope.dottedname.resolve import resolve
import os


class IConfigFile(Interface):
    """a config file to load up"""
    file = BytesLine(
        title=u'Configuration file name',
        description=u'Name of a configuration file to be loaded',
        required=True)

class IEntryPoints(Interface):
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


_config = None

def load_config(_context, file=None):
    global _config
    if file is None:
        # do default?
        pass
    cp = ConfigParser()
    cp.read(file)
    _config = cp

def load_entry_points(_content, group=None):
    global _config

    if group is None:
        # do default?
        pass

    for ep in pkr.iter_entry_points(group):
        dist = ep.dist
        dist_name = dist.project_name
        filename = ep.load()
        _config.set(ep.name, dist_name, filename)

def load(_context, zcmlgroup='configure.zcml', override=False):
    global _config
    include = xmlconfig.include
    if override:
        include = xmlconfig.includeOverrides
    cp = _config

    try:
        items = cp.items(zcmlgroup)
    except NoSectionError:
        print "no section: %s" %zcmlgroup
        return

    for dist, dotted_package in items:
        req = pkr.Requirement.parse(dist)
        module_path = os.path.join(*dotted_package.split('.'))
        filename = os.path.join(module_path, zcmlgroup)
        filename = pkr.resource_filename(req, filename)
        dep_package = resolve(dotted_package)
        include(_context, file=filename, package=dep_package)

def load_overrides(_context, zcmlgroup='overrides.zcml'):
    load(_context, zcmlgroup, override=True)
    
def get_config(self):
    return _config

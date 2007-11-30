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

def load_entry_points(_content, group):
    global _opencore_config
    for ep in pkr.iter_entry_points(group):
        zcmlmap = ep.load()
        for section in ('meta.zcml', 'configure.zcml', 'overrides.zcml'):
            _opencore_config.set(section, ep.distname, zcmlmap[section])

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
        if not filename.endswith('/'):
            filename = pkr.resource_filename(req, filename)
        else:
            filename = pkr.resource_filename(req, zcmlgroup)
        include(_context, filename)

def load_overrides(_context, zcmlgroup='overrides.zcml'):
    load(_context, zcmlgroup, override=True)
    
def get_opencore_config(self):
    return _opencore_config

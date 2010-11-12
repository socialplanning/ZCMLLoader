from ConfigParser import NoSectionError
from ConfigParser import ConfigParser
from zope.configuration import xmlconfig
import pkg_resources as pkr
from zope.interface import Interface
from zope.schema import BytesLine
from zope.schema import TextLine
from zope.dottedname.resolve import resolve
import os

class IEntryPoints(Interface):
    """an entry point group to load up"""
    group = TextLine(
        title=u'Entry point group name',
        description=u'Name of an entry point group to be loaded',
        required=True)

class IIncludes(Interface):
    target = TextLine(
        title=u"target",
        description=u"Plugin set to be loaded",
        required=True,
        )

class IIncludeOverrides(Interface):
    zcmlgroup = TextLine(
        title=u"ZCML Group",
        description=u"File group to be loaded",
        required=True,
        default=u'overrides.zcml'
        )

def load(_context, target):
    include = xmlconfig.include

    for ep in pkr.iter_entry_points('topp.zcmlloader'):
        if ep.name != target:
            continue
        dotted_name = ep.module_name

        for zcmlgroup in ('configure.zcml', 'meta.zcml'):
            filename = pkr.resource_filename(dotted_name, zcmlgroup)
            if not os.path.isfile(filename): continue
            dep_package = ep.load()
            if zcmlgroup == 'overrides.zcml':
                include = xcmlconfig.includeOverrides
            xmlconfig.include(_context, file=filename, package=dep_package)
            print 'Found configuration file %s: <include package="%s" file="%s" />' % (filename, dotted_name, zcmlgroup)

        for zcmlgroup in ('overrides.zcml',):
            filename = pkr.resource_filename(dotted_name, zcmlgroup)
            if not os.path.isfile(filename): continue
            dep_package = ep.load()
            xmlconfig.includeOverrides(_context, file=filename, package=dep_package)
            print 'Found configuration file %s: <includeOverrides package="%s" file="%s" />' % (filename, dotted_name, zcmlgroup)
    

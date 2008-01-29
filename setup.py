from setuptools import setup, find_packages

version = '0.1'

setup(name='ZCMLLoader',
      version=version,
      description="utils for loading zcml from entry points",
      long_description="""\
""",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Whit Morriss, Ethan Jucovy',
      author_email='whit@openplans.org',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['topp'],
      include_package_data=True,
      zip_safe=False,
      dependency_links=[
        'https://svn.openplans.org/svn/snowsprint/z3c.autoinclude/trunk#egg=z3c.autoinclude-dev',
        ],
      install_requires=[
          'setuptools',
          'zope.dottedname'
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      [distutils.commands]
      zinstall = topp.utils.setup_command:zinstall
      """,
      )

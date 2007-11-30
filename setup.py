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
      author='whit',
      author_email='whit@openplans.org',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['topp'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      [distutils.commands]
      zinstall = topp.utils.setup_command:zinstall
      """,
      )

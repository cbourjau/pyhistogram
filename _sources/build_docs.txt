Building the documentation
==========================

Building the documentation requires sphinx together with napoleon to be installed.

If new modules or methods were added one needs to rebuild the source files with
from the docs directory by running
::

   $ sphinx-apidoc -f -o source/ ../pyhistogram/ ../pyhistogram/tests

Than, the html files can be recreated by running 
::

   make html

in the docs directory again. The html file will be created in ../../pyhistogram-docs/html from where it can easily be pushed to the github-pages.

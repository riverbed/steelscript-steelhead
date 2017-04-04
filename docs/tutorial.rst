.. py:currentmodule:: steelscript.steelhead.core

SteelScript SteelHead Tutorial
================================

This tutorial will walk through the main components of the SteelScript
interfaces for Riverbed SteelHead Appliance.  It is assumed that
you have a basic understanding of the Python programming language.

The tutorial has been organized so you can follow it sequentially.
Throughout the examples, you will be expected to fill in details
specific to your environment.  These will be called out using a dollar
sign ``$<name>`` -- for example ``$host`` indicates you should fill in
the host name or IP address of a SteelHead appliance.

Whenever you see ``>>>``, this indicates an interactive session using
the Python shell.  The command that you are expected to type follows
the ``>>>``.  The result of the command follows.  Any lines with a
``#`` are just comments to describe what is happening.  In many cases
the exact output will depend on your environment, so it may not match
precisely what you see in this tutorial.

Background
----------

Riverbed SteelHead is the industry’s #1 optimization solution for
accelerated delivery of all applications across the hybrid enterprise.
SteelHead also provides better visibility into application and network
performance and the end user experience plus control through an
application-aware approach to hybrid networking and path selection based
on centralized, business intent-based policies for what you want to
achieve – as a business.  SteelScript for SteelHead offers a set of interfaces
to control and work with a SteelHead appliance.

Operation Overview
------------------

Interacting with a SteelHead appliance via a python script involves two steps.
The first step is to obtain a SteelHead object.  The second step is to send
command to the appliance via the existing SteelHead object.  Below we will
describe both steps in details.

Obtaining a SteelHead Object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As with any Python code, the first step is to import the module(s) we
intend to use. The SteelScript code for working with SteelHead appliances
resides in a module called :py:mod:`steelscript.steelhead.core.steelhead`.
The main class in this module is :py:class:`SteelHead <steelhead.SteelHead>`.
This object represents a connection to a SteelHead appliance.

To start, start python from the shell or command line:

.. code-block:: bash

   $ python
   Python 2.7.3 (default, Apr 19 2012, 00:55:09)
   [GCC 4.2.1 (Based on Apple Inc. build 5658) (LLVM build 2335.15.00)] on darwin
   Type "help", "copyright", "credits" or "license" for more information.
   >>>

Once in the python shell, let's create a SteelHead object:

.. code-block:: python

   >>> from steelscript.steelhead.core import steelhead
   >>> from steelscript.common.service import UserAuth
   >>> auth = UserAuth(username=$username, password=$password)
   >>> sh = steelhead.SteelHead(host=$host, auth=auth)

At first the module of :py:mod:`steelscript.steelhead.core.steelhead` and
:py:mod:`steelscript.common.service` are imported. Two classes were used,
including :py:class:`UserAuth <steelscript.common.service.UserAuth>` and
:py:class:`SteelHead <steelhead.SteelHead>`. The object ``auth`` is created
by instantiating the :py:class:`UserAuth <steelscript.common.service.UserAuth>`
class with username and password to access an SteelHead appliance. Afterwards,
a SteelHead object is created by instantiating the SteelHead class with
the hostname or IP address of the SteelHead appliance and the existing
authentication object. Note that the arguments ``$username`` and ``$password`` 
need to be replaced with the actual username and password, and the argument
``$host`` need to be replaced with the hostname or IP address of the SteelHead
appliance. 

As soon as the :py:class:`SteelHead <steelhead.SteelHead>` object is created, a connection is
established to the appliance, and the authentication credentials are
validated.  If the username and password are not correct, you will
immediately see an exception.

Sending commands
^^^^^^^^^^^^^^^^

As soon as a SteelHead object is available, commands can be sent to the SteelHead
appliance via two kinds of interfaces: Command Line Interface (CLI) and Application Program
Interface (API).  CLI is mainly used if the end user just wants to view the
output as it returns well formatted string. In contrast, API returns python data objects and
therefore can be used for further data analysis and processing.

See below for a detailed description for both interfaces are presented using concrete examples.
Note that ``sh`` will be used to reference the existing SteelHead object, which is the
basis for all communication with the SteelHead appliance. 

CLI Interface
"""""""""""""

We can get some basic version information as follows.

.. code-block:: python

   >>> print sh.cli.exec_command("show version")
   Product name:      rbt_sh
   Product release:   8.5.2
   Build ID:          #39
   Build date:        2013-12-20 10:10:02
   Build arch:        i386
   Built by:          mockbuild@bannow-worker4

   Uptime:            153d 10h 8m 29s

   Product model:     250
   System memory:     2063 MB used / 974 MB free / 3038 MB total
   Number of CPUs:    1
   CPU load averages: 0.23 / 0.15 / 0.10

As shown above, a CLI object is obtained by referencing the ``cli`` attribute
of ``sh``. Afterwards, a method ``exec_command`` can be called via the existing CLI
object. Note that the string argument is the actual CLI command that is run as if it
were executed on the SteelHead appliance.

When one logs into a SteelHead appliance, he/she will be in one of three modes
on a shell terminal, including basic mode, enable mode and configure mode. The CLI
interface from the SteelHead object defaults to enable mode. In order to enter into
configure mode, the user need to either use a "mode" parameter or change the default
mode to configure mode. The first method applies to scenarios when one just needs to
run no more than a few commands in configure mode, as shown below:

.. code-block:: python

   >>> from steelscript.cmdline.cli import CLIMode
   >>> sh.cli.exec_command("show version", mode=CLIMode.CONFIG)

In contrast, if the user wants to engage in a fair amount of interactions with SteelHead
appliance in configure mode, it is recommended to change the default to configure mode, as
shown below:

.. code-block:: python

   >>> from steelscript.cmdline.cli import CLIMode
   >>> sh.cli.default_mode = CLIMode.CONFIG
   >>> sh.cli.exec_command("show version")

API Interface
"""""""""""""

If the user wants to obtain python data objects via the SteelHead object ``sh``
instead of just viewing the output, he/she should use the API interface.
The key components of the API interface are the Model and Action class.
Model class is used if the desired data is a property of a SteelHead appliance,
which can usually be derived by executing just one command.
On the other hand, the Action class is intended to include higher-level methods,
deriving data by taking some extra processing in addition to just one command.
For instance, to obtain the version information of a SteelHead appliance should
be using the Model class as follows:

.. code-block:: python

   >>> from pprint import pprint
   >>> from steelscript.common.interaction.model import Model
   >>> model = Model.get(sh, feature='common')
   >>> pprint(model.show_version())
   {u'build arch': u'i386',
    u'build id': u'#39',
    u'built by': u'mockbuild@bannow-worker4',
    u'number of cpus': 1,
    u'product model': u'250',
    u'product name': u'rbt_sh',
    u'product release': u'8.5.2'}

In contrast, to get the product information of the SteelHead requires further processing
of the output of the version information above, thus the Action class should be used
as follows:

.. code-block:: python

   >>> from pprint import pprint
   >>> from steelscript.common.interaction.action import Action
   >>> action = Action.get(sh, feature='common')
   >>> pprint(action.get_product_info())
   {u'model': u'250', u'name': u'SteelHead', u'release': u'8.5.2'}

From the above two examples, we can summarize on the procedure of using API to
obtain data from a SteelHead.  First of all, the Model or Action class is imported.
Secondly, the Model or Action object is created by passing the SteelHead object ``sh``
and a feature string "common" to the get class method associated with either Model or Action class.
The last and most important step is to call a method associated with the derived Model
or Action object according to the specific data that is desired.
There are a total of 5 features available: 'common', 'networking', 'optimization', 'flows' and 'stats'.
Each feature is bound to a model and action object with a set of associated methods.
Methods supported by each feature can be found at :doc:`steelhead`.
Note that both of the above-mentioned examples yield data as a python dictionary instead
of a well-formatted string.


Before moving on, exit the python interactive shell:

.. code-block:: python

   >>> [Ctrl-D]
   $

Extending the Example
---------------------

As a last item to help get started with your own scripts, we will post a new
script below, then walk through the key sections in the example script.

.. code-block:: python

   #!/usr/bin/env python

   import steelscript.steelhead.core.steelhead as steelhead

   from steelscript.common.service import UserAuth
   from steelscript.common.app import Application

   class ShowVersionApp(Application):

       def add_positional_args(self):
           self.add_positional_arg('host', 'SteelHead hostname or IP address')

       def add_options(self, parser):
           super(ShowVersionApp, self).add_options(parser)

           parser.add_option('-u', '--username', help="Username to connect with")
           parser.add_option('-p', '--password', help="Password to use")

       def validate_args(self):
           super(ShowVersionApp, self).validate_args()

           if not self.options.username:
               self.parser.error("User Name needs to be specified")

           if not self.options.password:
               self.parser.error("Password needs to be specified")

       def main(self):
           auth = UserAuth(username=self.options.username,
                           password=self.options.password)
           sh = steelhead.SteelHead(host=self.options.host, auth=auth)

           print sh.cli.exec_command("show version")

    
   ShowVersionApp().run()

Let us break down the script. First we need to import some items:

.. code-block:: bash

   #!/usr/bin/env python

   import steelscript.steelhead.core.steelhead as steelhead

   from steelscript.common.app import Application

That bit at the top is called a shebang, it tells the system that it should
execute this script using the program after the '#!'. Besides steelhead module,
we are also importing the Application class, which is used to help parse arguments
and simplify the api call to run the application.

.. code-block:: bash

   class ShowVersionApp(Application):

       def add_options(self, parser):
           super(ShowVersionApp, self).add_options(parser)
           parser.add_option('-H', '--host',
                             help='hostname or IP address')
           parser.add_option('-u', '--username', help="Username to connect with")
           parser.add_option('-p', '--password', help="Password to use")

       def validate_args(self):
           super(ShowVersionApp, self).validate_args()

           if not self.options.host:
               self.parser.error("Host name needs to be specified")

           if not self.options.username:
               self.parser.error("User Name needs to be specified")

           if not self.options.password:
               self.parser.error("Password needs to be specified")

This section begins the definition of a new class, which inherits from the
class Application.  This is some of the magic of object-oriented programming,
a lot of functionality is defined as part of Application, and we get all
of that for *free*, just by inheriting from it.  In fact, we go beyond that,
and *extend* its functionality by defining the function ``add_options`` and
``validate_args``.  Here, we add options to pass in a host name, a user name and
a password, and then if the format of the passed-in arguments in the command
is wrong, a help message will be printed out. 

.. code-block:: bash

       def main(self):
           auth = UserAuth(username=self.options.username,
                           password=self.options.password)
           sh = steelhead.SteelHead(host=self.options.host, auth=auth)

           print (sh.cli.exec_command("show version"))

    
   ShowVersionApp().run()

This is the main part of the script, and it is using the CLI interface. One
can easily modify it to use any API interface to fetch data from a SteelHead appliance.
The last line calls the run function as defined in the Application class,
which executes the main function defined in the ShowVersionApp class.

Now let us try to run the script. Copy the code into a new file ``show_version_example.py``,
make it executable and run it from command line. Note that ``host``, ``username``, ``password``
are now all items to be passed to the command, shown as below.

.. code-block:: bash

   $ chmod +x show_version_example.py
   $ show_version_example.py $host -u $username -p $password
   Product name:      rbt_sh
   Product release:   8.5.2
   Build ID:          #39
   Build date:        2013-12-20 10:10:02
   Build arch:        i386
   Built by:          mockbuild@bannow-worker4

   Uptime:            153d 10h 8m 29s

   Product model:     250
   System memory:     2063 MB used / 974 MB free / 3038 MB total
   Number of CPUs:    1
   CPU load averages: 0.23 / 0.15 / 0.10


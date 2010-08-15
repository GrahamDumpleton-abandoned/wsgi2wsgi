# COPYRIGHT 2010 GRAHAM DUMPLETON

import sys
import os
import imp
import cStringIO

from adapter import Adapter

class Script(object):

    def __init__(self, filename):
        self._filename = filename

    def __call__(self, environ, start_response):

        # Load the target WSGI script file into a dummy module.

        module = imp.new_module('__wsgi__')
        module.__file__ = self._filename
        execfile(self._filename, module.__dict__)
        sys.modules['__wsgi__'] = module

        # Lookup and execute the WSGI application.

        application = getattr(module, 'application')

        return application(environ, start_response)


def main():

    # Keep a reference to the original stdin. We then replace
    # stdin with an empty stream. This is to protect against
    # code from accessing sys.stdin directly and consuming the
    # request content.

    stdin = sys.stdin

    sys.stdin = cStringIO.StringIO('')

    # Keep a reference to the original stdout. We then replace
    # stdout with stderr. This is to protect against code that
    # wants to use 'print' to output debugging. If stdout wasn't
    # protected, then anything output using 'print' would end up
    # being sent as part of the response itself and interfere
    # with the operation of the CGI protocol.

    stdout = sys.stdout

    sys.stdout = sys.stderr

    # Use the original stderr as is for errors.

    stderr = sys.stderr

    # Use a copy of the process environment as we want to
    # populate it with additional WSGI specific variables and
    # don't want to be polluting the process environment
    # variables with those as they would then be inherited by
    # sub processes.

    environ = dict(os.environ.items())

    # Target WSGI script file is dictated by value of the
    # variable SCRIPT_FILENAME in CGI environment.

    filename = environ['SCRIPT_FILENAME']

    # Create adapter for the WSGI application contained in
    # the WSGI script file.

    application = Script(filename)

    # Create CGI/WSGI bridge wrapping the 'application' entry
    # point in the target WSGI script file along with the
    # current request context. We only use the object once and
    # then the process exits, so doesn't matter it isn't
    # reusable or thread safe.

    adapter = Adapter(application, environ, stdin, stdout, stderr)

    # Execute the application.

    adapter.handle_request()


if __name__ == '__main__':
    main()

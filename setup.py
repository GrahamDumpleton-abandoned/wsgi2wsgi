from distutils import core

packages = [
    "wsgi2wsgi",
    "wsgi2wsgi.adapters",
    "wsgi2wsgi.adapters.cgi2wsgi",
]

core.setup(
    name = "wsgi2wsgi",
    version = "1.0",
    packages = packages,
    license = "Apache 2.0 Licence",
    description = "WSGI deployment toolkit.",
    author = "Graham Dumpleton",
    author_email = "Graham.Dumpleton@gmail.com",
    maintainer = "Graham Dumpleton",
    maintainer_email = "Graham.Dumpleton@gmail.com",
    url = "http://blog.dscpl.com.au",
)

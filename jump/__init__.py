import pkg_resources

from jump import libtracer


VERSION = "0.9"
lib_dir = pkg_resources.resource_filename('jump', 'lib')
template_dir = pkg_resources.resource_filename('jump', 'templates')

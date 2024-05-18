from collections import namedtuple

InstallablePlugin = namedtuple('InstallablePlugin', ('target_object', 'namespace', 'implementation_class'))
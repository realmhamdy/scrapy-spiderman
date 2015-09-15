import sys
import imp
import os
from os import walk as walk_dir
from django.conf import settings


def find_spiders():
    # return paths to all spiders' settings modules
    settings_paths = []
    imported_settings = sys.modules.pop("settings", None)
    for spiders_dir in settings.SPIDER_DIRS:
        for (root, dirshere, fileshere) in walk_dir(spiders_dir):
            try:
                fp, pathname, description = imp.find_module("settings", [root + os.sep])
            except ImportError:
                continue
            if fp is not None:
                try:
                    spider_settings = imp.load_module("settings", fp, pathname, description)
                    if hasattr(spider_settings, "SPIDER_MODULES"):
                        settings_paths.append(os.path.dirname(pathname))
                    sys.modules.pop("settings")
                except ImportError:
                    pass
                finally:
                    fp.close()
    if imported_settings is not None:
        # is this how you re-import a module?
        sys.modules["settings"] = imported_settings
    return settings_paths

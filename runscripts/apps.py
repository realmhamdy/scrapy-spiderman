import os
import os.path as pth
from django.apps import AppConfig, apps


class RSAppConfig(AppConfig):

    name = "runscripts"
    verbose_name = "Run Scripts"

    searched = False
    found_scripts = []

    def ready(self):
        if not self.searched:
            # find scripts here in app folders
            for app_config in apps.get_app_configs():
                app_path = app_config.path
                possible_scripts_path = pth.join(app_path, "scripts")
                if pth.exists(possible_scripts_path) and pth.isdir(possible_scripts_path):
                    # any files in the scripts directory will be considered scripts
                    # TODO: provide a setting to exclude certain script extensions
                    app_scripts = os.listdir(possible_scripts_path)
                    for script_name in app_scripts:
                        self.found_scripts.append(pth.join(possible_scripts_path, script_name))
        self.searched = True

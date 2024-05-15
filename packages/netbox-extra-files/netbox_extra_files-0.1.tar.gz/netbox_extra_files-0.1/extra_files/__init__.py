from extras.plugins import PluginConfig

class ExtraFilesConfig(PluginConfig):
    name = 'extra_files'
    verbose_name = 'Netbox Extra Files'
    description = 'Store files together with your netbox objects'
    version = '0.1'
    author = 'Eric Lindsjö'
    author_email = 'eric@emj.se'
    base_url = 'extra-files'
    required_settings = []
    default_settings = {}


config = ExtraFilesConfig

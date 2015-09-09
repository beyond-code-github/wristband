from django.conf import settings

from wristband.providers.config import ProvidersConfig

if settings.PROVIDER_CONFIG == 'providers.yaml':
    providers_config = ProvidersConfig.load_from_file(settings.PROVIDER_CONFIG)
else:
    providers_config = ProvidersConfig.load_from_env(settings.PROVIDER_CONFIG)

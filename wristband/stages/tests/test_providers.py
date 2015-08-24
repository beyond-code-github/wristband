from wristband.stages.providers import EnvVarStagesDataProvider


def get_env_var_stages_data_provider(settings):
    settings.STAGES = 'qa,staging,test'

    provider_under_test = EnvVarStagesDataProvider()

    assert provider_under_test._get_raw_data() == ['qa', 'staging', 'test']
    assert provider_under_test._get_list_data() == [
                                                        {'name': 'qa'},
                                                        {'name': 'staging'},
                                                        {'name': 'test'},
                                                    ]

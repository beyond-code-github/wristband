from wristband.stages.providers import EnvVarStagesDataProvider


def test_get_env_var_stages_data_provider(settings):
    settings.STAGES = 'foo,bar,test'

    provider_under_test = EnvVarStagesDataProvider()

    assert provider_under_test._get_raw_data() == ['foo', 'bar', 'test']
    assert provider_under_test._get_list_data() == [
                                                        {'name': 'foo'},
                                                        {'name': 'bar'},
                                                        {'name': 'test'},
                                                    ]

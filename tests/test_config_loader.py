from trace_invest.config.loader import load_config


def test_config_loads_successfully():
    config = load_config()
    assert "system" in config
    assert "universe" in config
    assert "risk" in config
    assert "data_sources" in config


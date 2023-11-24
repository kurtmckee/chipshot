import pytest


@pytest.mark.parametrize("top_level_key", ("extension", "style"))
def test_defaults_key_order_first_level(default_config, top_level_key):
    """Guarantee the default config has sorted keys."""

    previous_name = ""
    for name in default_config[top_level_key]:
        assert name > previous_name, f"'{name}' is not sorted in '{top_level_key}'"
        previous_name = name

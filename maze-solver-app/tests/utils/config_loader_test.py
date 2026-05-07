import pytest
from src.utils.config_loader import get_config



def test_config_loading():
    '''Verify that configuration is a dictionary and has required keys'''
    config = get_config()
    assert isinstance(config, dict)
    assert 'window' in config
    assert 'main_screen' in config # TO-DO other screens
    assert 'colors' in config
    assert 'fonts' in config

def test_config_loading():
    '''Verify that configuration is a dictionary and has required keys'''
    config = get_config()
    assert isinstance(config, dict)
    assert 'window' in config
    assert 'main_screen' in config # TO-DO other screens
    assert 'colors' in config
    assert 'fonts' in config

def test_colors_are_valid_rgb():
    '''Check if colors are lists of 3 integers between 0 and 255'''
    config = get_config()
    for color_name, value in config['colors'].items():
        assert len(value) == 3
        assert all(0 <= c <= 255 for c in value)

def test_screens_have_all_variables():
    '''Check if every screen have all required variables'''
    config = get_config()
    assert 'has_return' in config['main_screen']
    assert 'title' in config['main_screen']
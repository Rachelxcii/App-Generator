import pytest
from src.utils.config_loader import get_config


@pytest.fixture(scope='module')
def loaded_config():
    '''
    Loads the real config.json for all tests in this module.
    Scope 'module' ensures the file is read only once for this script.
    '''
    return get_config()


class BaseConfigTest:

    @pytest.fixture(autouse=True)
    def setup_class_data(self, loaded_config):
        self.config = loaded_config


class TestGeneralConfig(BaseConfigTest):

    def test_config_is_dict(self):
        '''Verify that configuration is a dictionary'''
        msg = 'Config should be a dictionary.'
        assert isinstance(self.config, dict), msg

    def test_mandatory_sections_exist(self):
        '''Verify that configuration has mandatory sections'''
        sections = ['window', 'colors', 'fonts']
        for section in sections:
            msg = f'Missing critical section: {section} in configuration file.'
            assert section in self.config, msg


class TestColors(BaseConfigTest):

    def test_colors_are_valid_rgb(self):
        '''
        Check every color has RGB format: [Red, Green, Blue].
        Should be a list of 3 integers between 0 and 255.
        For example: white is [255, 255, 255].
        '''
        colors = self.config['colors']
        for color_name, value in colors.items():
            msg_1 = f'Color "{color_name}" should be a list'
            msg_2 = f' of 3 integers'
            msg_3 = f' between 0 and 255'
            msg_end = f'.'
            assert isinstance(value, list), msg_1+msg_end
            assert len(value) == 3, msg_1+msg_2+msg_end
            assert all(isinstance(c, int) for c in value), msg_1+msg_2+msg_end
            assert all(0 <= c <= 255 for c in value), msg_1+msg_2+msg_3+msg_end


class TestScreens(BaseConfigTest):

    def test_one_or_more_screen_sections_exist(self):
        '''Verify that configuration has one or screen section'''
        screens = [key for key in self.config if key.endswith('screen')]
        msg = 'No screen found or incorrect name format, should end in "_screen".'
        assert len(screens) > 0, msg

    def test_screens_have_all_variables(self):
        '''Check if every screen have all required variables'''
        screens = [key for key in self.config if key.endswith('screen')]
        keys = ['has_return', 'title']
        for screen in screens:
            for key in keys:
                msg = f'Screen "{screen}" has not "{key}" key.'
                assert key in self.config[screen], msg

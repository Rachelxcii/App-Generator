import pytest
from src.utils.config_loader import get_config


@pytest.fixture(scope='module')
def loaded_config():
    '''
    Loads the real config.json for all tests in this module.
    Scope 'module' ensures the file is read only once for this script.
    '''
    try:
        return get_config()
    except (FileNotFoundError, ValueError) as e:
        return None


class BaseConfigTest:

    @pytest.fixture(autouse=True)
    def setup_class_data(self, loaded_config):
        self.config = loaded_config


class TestGeneralConfig(BaseConfigTest):

    def test_get_config_execution(self):
        '''Verify that get_config() executed successfully and returned data'''
        msg = (
            "CRITICAL: get_config() failed. "
            "Check if 'config.json' exists and is valid JSON."
        )
        assert self.config is not None, msg

    def test_config_is_dict(self):
        '''Verify configuration is a dictionary'''
        msg = 'Config should be a dictionary.'
        assert isinstance(self.config, dict), msg

    def test_mandatory_sections_exist(self):
        '''Verify configuration has mandatory sections'''
        sections = ['window', 'colors', 'fonts']
        for section in sections:
            msg = f'Missing critical section: {section} in configuration file.'
            assert section in self.config, msg


class TestWindow(BaseConfigTest):

    @pytest.fixture(autouse=True)
    def setup_window(self):
        '''Inherits self.config and prepares the specific section'''
        self.window = self.config.get('window', {}) if self.config else {}

    def test_window_is_dictionary(self):
        '''Verify window section is a dictionary'''
        msg = 'The "window" section should be a dictionary.'
        assert isinstance(self.window, dict), msg

    def test_mandatory_keys_in_window(self):
        '''Verify window section has mandatory variables'''
        variables = ['width', 'height', 'fps']
        for var in variables:
            msg = f'Missing critical variable: {var} in window config.'
            assert var in self.window


class TestColors(BaseConfigTest):

    @pytest.fixture(autouse=True)
    def setup_colors(self):
        '''Inherits self.config and prepares the specific section'''
        self.colors = self.config.get('colors', {}) if self.config else {}

    def test_colors_is_dictionary(self):
        '''Verify colors section is a dictionary'''
        msg = 'The "colors" section should be a dictionary.'
        assert isinstance(self.colors, dict), msg

    def test_colors_are_valid_rgb(self):
        '''
        Check every color has RGB format: [Red, Green, Blue].
        Should be a list of 3 integers between 0 and 255.
        For example: white is [255, 255, 255].
        '''
        for color_name, value in self.colors.items():
            msg_1 = f'Color "{color_name}" should be a list'
            msg_2 = f' of 3 integers'
            msg_3 = f' between 0 and 255'
            msg_end = f'.'
            assert isinstance(value, list), msg_1+msg_end
            assert len(value) == 3, msg_1+msg_2+msg_end
            assert all(isinstance(c, int) for c in value), msg_1+msg_2+msg_end
            assert all(0 <= c <= 255 for c in value), msg_1+msg_2+msg_3+msg_end


class TestFonts(BaseConfigTest):

    @pytest.fixture(autouse=True)
    def setup_fonts(self):
        '''Inherits self.config and prepares the specific section'''
        self.fonts = self.config.get('fonts', {}) if self.config else {}

    def test_fonts_is_dictionary(self):
        '''Verify fonts section is a dictionary'''
        msg = 'The "fonts" section should be a dictionary.'
        assert isinstance(self.fonts, dict), msg

    def test_mandatory_keys_in_every_font(self):
        '''Check every font has: "file" and "size"'''
        keys = ['file', 'size']
        for font in self.fonts:
            for key in keys:
                msg = f'Font "{font}" has not "{key}" key.'
                assert key in self.config[font], msg


class TestScreens(BaseConfigTest):

    @pytest.fixture(autouse=True)
    def setup_window(self):
        '''Inherits self.config and prepares the specific section'''
        self.screens = [key for key in self.config if key.endswith('screen')]

    def test_one_or_more_screen_sections_exist(self):
        '''Verify that configuration has one or screen section'''
        msg = (
            'No screen found or incorrect name format, '
            'should end in "_screen".'
            )
        assert len(self.screens) > 0, msg

    def test_every_screen_is_dictionary(self):
        '''Verify fonts section is a dictionary'''
        for screen in self.screens:
            msg = f'The {screen} section should be a dictionary.'
            assert isinstance(screen, dict), msg

    def test_mandatory_keys_in_every_screen(self):
        '''Check if every screen have all required variables'''
        keys = ['has_return', 'title']
        for screen in self.screens:
            for key in keys:
                msg = f'Screen "{screen}" has not "{key}" key.'
                assert key in self.config[screen], msg

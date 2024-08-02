import unittest
from unittest.mock import patch, MagicMock
from character.character import Character
from connexion import Connexion
from errors.exceptions import *
import requests

class TestCharacter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.patcher = patch('connexion.Connexion.get')
        cls.mock_get = cls.patcher.start()

        cls.mock_response = MagicMock()
        cls.mock_response.json.return_value = {
            'data': {
                'hp': 100,
                'level': 10,
                'gold': 50,
                'xp': 200,
                'max_xp': 300,
                'cooldown': 5,
                'x': 10,
                'y': 20
            }
        }
        cls.mock_get.return_value = cls.mock_response.json.return_value

    @classmethod
    def tearDownClass(cls):
        cls.patcher.stop()

    def test_get_data_success(self):
        char = Character('test_char')
        char.get_data()

        self.assertEqual(char.hp, 100)
        self.assertEqual(char.lvl, 10)
        self.assertEqual(char.gold, 50)
        self.assertEqual(char.current_xp, 200)
        self.assertEqual(char.next_lvl_xp, 300)
        self.assertEqual(char.cooldown, 5)
        self.assertEqual(char.pos_x, 10)
        self.assertEqual(char.pos_y, 20)

    @patch('connexion.Connexion')
    def test_get_data_failed(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_get.side_effect = mock_response.raise_for_status

        char = Character('test_char_not_found')

        with self.assertRaises(CharacterNotFoundError) as context:
            char.get_data()

        self.assertEqual(str(context.exception), "Character 'test_char_not_found' not found.")

    @patch('character.Character.wait_for_cd')
    def test_wait_for_cd(self, mock_wait_for_cd):
        char = Character('test_char')

        char.wait_for_cd()
        self.assertEqual(char.cooldown, 5)
        mock_wait_for_cd.assert_called_once()

    @patch('connexion.Connexion.post')
    def test_move(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'x': 0,
            'y': 3
        }

        mock_post.return_value = mock_response.json.return_value

        char = Character('test_char')
        char.move(0, 4)

        mock_post.assert_called_once_with(
            'my/test_char/action/move',
            {'x': 0, 'y': 4}
        )
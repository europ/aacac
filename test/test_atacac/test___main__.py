from unittest import mock

import click
import pytest  # pylint: disable=import-error

from atacac import __main__


class TestCommandsLoader:

    def test_list_commands(self):
        CL = __main__.CommandsLoader()

        assert CL.list_commands(click.Context) == [
            "backup",
            "differentiate",
            "restore",
            "synchronize",
            "upload",
            "validate"
        ]

    @pytest.mark.parametrize(
        "name",
        [
            pytest.param("backup", id="'backup'"),
            pytest.param("differentiate", id="'differentiate'"),
            pytest.param("restore", id="'restore'"),
            pytest.param("synchronize", id="'synchronize'"),
            pytest.param("upload", id="'upload'"),
            pytest.param("validate", id="'validate'"),
        ]
    )
    @mock.patch("atacac.__main__.importlib")
    def test_get_command(self, mock_importlib, name):

        class mock_module:
            def main(self):
                pass

        mock_importlib.import_module.return_value = mock_module

        CL = __main__.CommandsLoader()
        assert mock_module.main == CL.get_command(click.Context, name)

        mock_importlib.import_module.assert_called_with(f"atacac.{name}")

import io
from unittest.mock import call, patch

import pytest

from gcm.commands.base import (
    PACKAGE_NAME,
    Command,
    ensure_desired_env_line,
    get_package_env_path,
)

DUMMY_ENV = """# foo
bar
# foo
# baz
"""


@pytest.mark.parametrize(
    'exists,is_file',
    (
        (True, True),
        (True, False),
        (False, None),
    ),
)
@patch('gcm.commands.base.PACKAGE_ENV_PATH')
def test_get_package_env_path(mock, exists, is_file):
    mock.exists.return_value = exists
    mock.is_file.return_value = is_file

    new_path = object()
    truediv = mock.__truediv__
    truediv.return_value = new_path

    path = get_package_env_path()

    mock.exists.assert_called_once_with()

    if exists:
        mock.mkdir.assert_not_called()
        mock.is_file.assert_called_once_with()
    else:
        mock.mkdir.assert_called_once_with()
        mock.is_file.assert_not_called()

    if is_file:
        truediv.assert_not_called()
        assert path is mock
    else:
        truediv.assert_called_once_with('ccache')
        assert path is new_path


@pytest.mark.parametrize(
    'desired,undesired,expected',
    (
        ('foo\n', '# foo\n', 'foo\nbar\n# baz\n'),
        ('bar\n', '# bar\n', '# foo\nbar\n# foo\n# baz\n'),
        ('baz\n', '# baz\n', '# foo\nbar\n# foo\nbaz\n'),
        ('new\n', '# new\n', '# foo\nbar\n# foo\n# baz\nnew\n'),
        ('# foo\n', 'foo\n', '# foo\nbar\n# foo\n# baz\n'),
        ('# bar\n', 'bar\n', '# foo\n# bar\n# foo\n# baz\n'),
        ('# baz\n', 'baz\n', '# foo\nbar\n# foo\n# baz\n'),
        ('# new\n', 'new\n', '# foo\nbar\n# foo\n# baz\n# new\n'),
    ),
)
@patch('gcm.commands.base.get_package_env_path')
def test_ensure_desired_env_line(
    get_package_env_path, desired, undesired, expected
):
    env = io.StringIO(DUMMY_ENV)
    path = get_package_env_path.return_value
    path.open.return_value.__enter__.return_value = env

    ensure_desired_env_line(desired, undesired)

    path.touch.assert_called_once()
    path.open.assert_called_once_with('r+')
    assert env.getvalue() == expected


def test_command_callback_not_implemented():
    with pytest.raises(NotImplementedError):
        Command.callback('app-misc/foo')


class DummyCommand(Command):
    """Do nothing."""

    INVOKE_MESSAGE = f'Doing nothing with {PACKAGE_NAME}'

    callback_is_called = False

    def callback(self, package):
        self.callback_is_called = True
        assert package == 'app-misc/foo'


@patch('click.echo')
def test_command_invoke(echo):
    command = DummyCommand()

    with pytest.raises(SystemExit):
        command(['foo'])

    assert command.callback_is_called
    assert echo.call_args_list == [
        call('Doing nothing with \x1b[32m\x1b[1mapp-misc/foo\x1b[0m'),
        call('\x1b[32mDone :-)\x1b[0m'),
    ]

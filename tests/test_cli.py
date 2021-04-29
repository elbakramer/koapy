import re

from click.testing import CliRunner

from koapy import cli


def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli.cli)
    assert result.exit_code == 0
    assert "Usage" in result.output
    help_result = runner.invoke(cli.cli, ["--help"])
    assert help_result.exit_code == 0
    assert (
        re.search(r"-h, --help[ ]* Show this message and exit.", help_result.output)
        is not None
    )
    assert "serve" in help_result.output

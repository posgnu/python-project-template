"""Unit tests for main module."""

import pytest
from typer.testing import CliRunner

from src.main import app


@pytest.fixture
def runner():
    """Create a CLI runner for testing."""
    return CliRunner()


class TestMainCLI:
    """Test cases for the main CLI application."""

    def test_hello_default(self, runner):
        """Test hello command with default argument."""
        result = runner.invoke(app, ["hello"])
        assert result.exit_code == 0
        assert "Hello, World!" in result.stdout

    def test_hello_with_name(self, runner):
        """Test hello command with custom name."""
        result = runner.invoke(app, ["hello", "Alice"])
        assert result.exit_code == 0
        assert "Hello, Alice!" in result.stdout

    def test_version(self, runner):
        """Test version command."""
        result = runner.invoke(app, ["version"])
        assert result.exit_code == 0
        assert "Version:" in result.stdout

    def test_process_missing_input(self, runner):
        """Test process command with missing input file."""
        result = runner.invoke(app, ["process", "--input", "nonexistent.txt"])
        assert result.exit_code == 1
        assert "Error:" in result.stdout or "Error:" in result.stderr

    def test_process_with_valid_input(self, runner, temp_file):
        """Test process command with valid input file."""
        result = runner.invoke(app, ["process", "--input", str(temp_file)])
        assert result.exit_code == 0
        assert "Processing complete!" in result.stdout

    def test_process_with_output(self, runner, temp_file, tmp_path):
        """Test process command with output file."""
        output_file = tmp_path / "output.txt"
        result = runner.invoke(
            app, ["process", "--input", str(temp_file), "--output", str(output_file)]
        )
        assert result.exit_code == 0
        assert "Writing output to" in result.stdout

    def test_process_verbose(self, runner, temp_file):
        """Test process command with verbose flag."""
        result = runner.invoke(app, ["process", "--input", str(temp_file), "--verbose"])
        assert result.exit_code == 0
        assert "Processing" in result.stdout


@pytest.mark.parametrize(
    "command,expected_exit_code",
    [
        (["hello"], 0),
        (["version"], 0),
        (["--help"], 0),
    ],
)
def test_cli_commands_exist(runner, command, expected_exit_code):
    """Test that CLI commands exist and run without errors."""
    result = runner.invoke(app, command)
    assert result.exit_code == expected_exit_code

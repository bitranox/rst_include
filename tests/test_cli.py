# EXT
from click.testing import CliRunner

# OWN
import rst_include.rst_include_cli as rst_include_cli

runner = CliRunner()
runner.invoke(rst_include_cli.cli_main, ['--version'])
runner.invoke(rst_include_cli.cli_main, ['-h'])
runner.invoke(rst_include_cli.cli_main, ['info'])

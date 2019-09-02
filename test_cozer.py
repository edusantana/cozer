from click.testing import CliRunner
from cozer import cli, misturar

def test_hello_world():
  runner = CliRunner()
  result = runner.invoke(cli,misturar, '-r')
  assert result.exit_code == 0
  assert result.output == 'Hello Peter!\n'

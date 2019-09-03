import pytest
from click.testing import CliRunner
from cozer import cli, misturar, texto_comum

'''
def test_hello_world():
  runner = CliRunner()
  result = runner.invoke(cli,misturar, '-r')
  assert result.exit_code == 0
  assert result.output == 'Hello Peter!\n'
'''

@pytest.mark.parametrize("resultado, operacao, recipiente, como, ate, ingrediente",
    [
        ("[recipiente] Servir ingrediente. Como(como). Até(ate).",
        "servir","recipiente", "como", "ate", ["ingrediente"]),
        ("[recipiente] Servir. Como(como). Até(ate).",
            "servir","recipiente", "como", "ate", ()),
        ("[recipiente] Servir. Como(como). Até(ate).",
            "servir","recipiente", "como", "ate", None),
        ("[recipiente] Servir i1, i2, i3. Como(como). Até(ate).",
            "servir","recipiente", "como", "ate", ['i1', 'i2', 'i3']),
    ])
def test_texto_comum(operacao, recipiente, como, ate, ingrediente,resultado):
    assert  resultado == texto_comum(operacao, recipiente, como, ate, ingrediente)

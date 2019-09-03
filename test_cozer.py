from click.testing import CliRunner
from cozer import cli, misturar, texto_comum

'''
def test_hello_world():
  runner = CliRunner()
  result = runner.invoke(cli,misturar, '-r')
  assert result.exit_code == 0
  assert result.output == 'Hello Peter!\n'
'''

def test_texto_comum():
    assert "[recipiente] Servir ingrediente. Como(como). Até(ate)." \
        == texto_comum("servir","recipiente", "como", "ate", ["ingrediente"])

    assert "[recipiente] Servir. Como(como). Até(ate)." \
        == texto_comum("servir","recipiente", "como", "ate", [])

    assert "[recipiente] Servir i1, i2, i3. Como(como). Até(ate)." \
        == texto_comum("servir","recipiente", "como", "ate", ['i1', 'i2', 'i3'])

    assert "[recipiente] Servir i1, i2, i3. Até(ate)." \
        == texto_comum("servir","recipiente", None, "ate", ['i1', 'i2', 'i3'])

    assert "[recipiente]. Servir i1, i2, i3. Como(como)." \
        == texto_comum("servir","recipiente", "como", None, ['i1', 'i2', 'i3'])

    assert "[recipiente] Retirar. Recipiente(recipiente). Como(como). Até(ate)." \
        == texto_comum("retirar","recipiente", "como", "ate", None)

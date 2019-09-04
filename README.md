# cozer

Sistema para auxiliar ensino de conceitos de informática

## Receitas

- [Cuscuz nordestino com queijo](https://guiadacozinha.com.br/cuscuz-nordestino-com-queijo/)
- [https://guiadacozinha.com.br/baiao-de-dois-rapido/](https://guiadacozinha.com.br/baiao-de-dois-rapido/)
- [https://guiadacozinha.com.br/bolo-de-rolo-receita/](https://guiadacozinha.com.br/bolo-de-rolo-receita/)
- [https://guiadacozinha.com.br/canjica-leite-condensado-cozido/](https://guiadacozinha.com.br/canjica-leite-condensado-cozido/)

## Instalar

Atualização documentação:

- https://packaging.python.org/tutorials/packaging-projects/
- https://click.palletsprojects.com/en/7.x/setuptools/#introduction

```bash
aula=$(mktemp -d -t aula-XXXXXXXX)
cd $aula
git clone https://github.com/edusantana/cozer
cd cozer
python3 -m venv venv
. venv/bin/activate
pip install --editable .
```

### Autocomplete

Adicionar a `.bashrc` ou executar:

        eval "$(_COZER_COMPLETE=source cozer)"

## Testando instalação:

        cozer --version
        cozer --help
        cozer fogao -h

## Desfazendo instalação

        deactivate
        cd .. && rm -rf cozer

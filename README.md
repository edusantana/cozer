# cozer

Sistema para auxiliar ensino de conceitos de informática

## Receitas

- [Cuscuz nordestino com queijo](https://guiadacozinha.com.br/cuscuz-nordestino-com-queijo/)
- [https://guiadacozinha.com.br/baiao-de-dois-rapido/](https://guiadacozinha.com.br/baiao-de-dois-rapido/)
- [https://guiadacozinha.com.br/bolo-de-rolo-receita/](https://guiadacozinha.com.br/bolo-de-rolo-receita/)
- [https://guiadacozinha.com.br/canjica-leite-condensado-cozido/](https://guiadacozinha.com.br/canjica-leite-condensado-cozido/)

# Instalação

## Instalação temporária

Utilize essas instruções para testar a aplicação em diretório temporário

```bash
aula=$(mktemp -d -t aula-XXXXXXXX)
cd $aula
python3 -m venv venv
. venv/bin/activate
pip install cozer
# Ativando auto-completar:
eval "$(_COZER_COMPLETE=source cozer)"
```

## Outros métodos de instalação

- Instalação para o usuário:

```
pip3 install cozer --user
```

- Instalação global:

```
pip3 install cozer
```

### Autocomplete

Para agilizar utilização do cozer com o recurso de auto-completar adicionar a `.bashrc` ou executar:

```
eval "$(_COZER_COMPLETE=source cozer)"
```

## Testando instalação:

```
cozer --version
cozer --help
cozer fogao -h
```

# Desenvolvimento

Se você deseja incluir novas funcionalidas na aplicação, utilize da seguinte forma:

```
git clone https://github.com/edusantana/cozer
cd cozer
virtualenv venv
. venv/bin/activate
pip install --editable .
```

Para depurar incluir no local do debug:

```
import pdb
pdb.set_trace()
```

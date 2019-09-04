import click
import functools
from click_didyoumean import DYMGroup


CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help']
)

class DuracaoType(click.ParamType):
    name = "duracao"

    def convert(self, value, param, ctx):
        try:
            unidade = value[-1]
            quantidade=None
            if value.endswith("min"):
                unidade = "min"
                quantidade = float(value[0:-3])
            elif value.endswith("h"):
                unidade = "h"
                quantidade = float(value[0:-1])
            else:
                self.fail("{} não contém unidade válida (min|h)".format(str(value)), param, ctx)

            return (quantidade, unidade)
        except TypeError:
            self.fail(
                "expected string for float() conversion, got " +
                "{value!r} of type {type(value).__name__}",
                param,
                ctx,
            )
        except ValueError:
            self.fail("{0} não é uma duração válida".format(value), param, ctx)


def opcoes_comuns(func):
    @click.option('-r','--recipiente','recipiente',metavar='<recipiente>', help='nome do recipiente que será utilizado. Ex: -r panela', envvar="RECIPIENTE", show_envvar=True, required=True)
    @click.option('--como', 'como', metavar='<descricao>', help='descrição de como deve ser realizado a operação, ex: --como "com cuidado para não quebrar"')
    @click.option('--ate', 'ate', metavar='<acontecimento>', help='condição para terminar a operação, ex: --ate "ficar uniforme"')
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper



@click.group(cls=DYMGroup, context_settings=CONTEXT_SETTINGS)
@click.version_option()
def cli():
    """
    Script para auxiliar o aprendizado de leitura de documentação e invocação de comandos.

    Simula realização de modo de preparo de comidas.

    Os comandos assumem que as operações são realizadas em recipientes, ex: "Panela" ou "Frigideira".

    """
    pass


@cli.command()
@opcoes_comuns
@click.argument('ingrediente', nargs=-1)
def misturar(recipiente, como, ate, ingrediente):
    """Mistura ingredientes."""

    click.echo(texto_comum('misturar', recipiente, como, ate, ingrediente))

@cli.command()
@opcoes_comuns
@click.argument('ingrediente', nargs=-1, required=True)
def cortar(recipiente, como, ate, ingrediente):
    """Cortar ingredientes."""

    click.echo(texto_comum('cortar', recipiente, como, ate, ingrediente))


@cli.command()
@opcoes_comuns
@click.option('-t','--tirando-de', 'recipiente_anterior',metavar='<RECIPIENTE_ANTERIOR>', help='nome do recipiente de onde será tirado o conteúdo. Utilizado quando deseja-se trocar de recipiente. Ex: --tirando-de panela')
@click.argument('ingrediente', nargs=-1)
def colocar(recipiente, como, ate, recipiente_anterior, ingrediente):
    """
    Colocar ingredientes ou trocar de recipiente.

    Pode ser utilizado trocar recipientes, tirando de um colocando em outro.
    """
    if recipiente_anterior:
        retirar = texto_comum('retirar', recipiente_anterior, como, ate, ingrediente)
        colocar = texto_comum('colocar', recipiente, None, None, None)
        click.echo(retirar + colocar[1:len(colocar)])
    else:
        click.echo(texto_comum('colocar', recipiente, como, ate, ingrediente))


@cli.command()
@opcoes_comuns
@click.argument('ingrediente', nargs=-1, required=True)
def adicionar(recipiente, como, ate, ingrediente):
    """
    Adicionar ingredientes em recipientes.

    INGREDIENTE: ingrediente que será utilizado.

    Exemplos:

        cozer adicionar -r panela sal pimenta

        cozer adicionar -r bacia tudo
    """

    click.echo(texto_comum('adicionar', recipiente, como, ate, ingrediente))

@cli.command()
@opcoes_comuns
@click.argument('ingrediente', nargs=-1)
def bater(recipiente, como, ate, ingrediente):
    """
    Bater ingredientes em recipientes.

    INGREDIENTE: ingrediente que será utilizado.

    Exemplos:

        cozer bater -r liquidificador --ate "ficar uniforme" mistura

        cozer bater -r bacia --como "sempre para o mesmo lado" ovos
    """

    click.echo(texto_comum('bater', recipiente, como, ate, ingrediente))

@cli.command(epilog="<duracao> número indicando o tempo de duração. Ex: 20min, 1.5h")
@opcoes_comuns
@click.option('--por', 'duracao', metavar='<duracao>', type=(DuracaoType()), help='Tempo de duração no fogão. Ex: --por 5min')
@click.option('-a','--aonde', 'aonde',metavar='<aonde>', help='Local aonde o recipiente ficará guardado. Ex: --aonde geladeira')
@click.argument('ingrediente', nargs=-1)
def reservar(recipiente, como, ate, duracao, aonde, ingrediente):
    """
    Reservar ingredientes em recipientes. Reservar equivale a deixar guardado para utilizar depois.

    INGREDIENTE: ingrediente que será utilizado.

    Exemplos:

        cozer reservar -r prato --por 24h --aonde geladeira mistura

    """

    click.echo(texto_completo('reservar', recipiente, como, ate, ingrediente, None, duracao, ("Aonde", aonde)))


@cli.command()
@opcoes_comuns
@click.option('-a','--acompanhamento', 'acompanhamento',metavar='<ACOMPANHAMENTO>', help='acompanhamento a servir junto. Ex: --acompanhamento "arroz e fritas"')
@click.argument('ingrediente', nargs=-1)
def servir(recipiente, como, ate, ingrediente, acompanhamento):
    """
    Servir ingredientes em recipientes.

    INGREDIENTE: ingrediente que será utilizado.

    Exemplos:

        cozer servir -r bandeija --como "ainda quente" peixe
    """

    click.echo(texto_completo('servir', recipiente, como, ate, ingrediente, None, None, ("Acompanhamento", acompanhamento)))


def texto_comum(operacao,recipiente, como, ate, ingrediente):
    return texto_completo(operacao,recipiente, como, ate, ingrediente, None, None)

def texto_completo(operacao,recipiente, como, ate, ingrediente, local, duracao, *args):
    if ingrediente == () or ingrediente is None:
        ingredientes = ""
    else:
        ingredientes = ", ".join(map(str,ingrediente))
    operacao_msg = "{}.".format(operacao.capitalize()) if (ingredientes=="") else ("{} {}.".format(operacao.capitalize(), ingredientes))
    if recipiente is None:
        recipiente_msg = ""
    elif (local is None):
         recipiente_msg = "[{}] ".format(recipiente)
    else:
        recipiente_msg = "[{}>{}] ".format(local, recipiente)

    como_msg = "" if (como is None) else (" Como({}).".format(como))
    ate_msg = "" if (ate is None) else (" Até({}).".format(ate))
    duracao_msg = "" if (duracao is None) else (" Por({} {}).".format(duracao[0], duracao[1]))
    local_msg = "" if (local is None) else ("[{}] ".format(local))
    final_msg = ""

    for indicador in args:
        if indicador[1] is True:
            final_msg += " {}.".format(indicador[0])
        elif indicador[1] is not None and indicador[1] is not False:
            final_msg += " {}({}).".format(indicador[0], indicador[1])
    return '%s%s%s%s%s%s' % ( recipiente_msg, operacao_msg, como_msg, duracao_msg, ate_msg, final_msg)


OPERACORES = ['esquentar', 'assar', 'fritar', 'cozinhar', 'refogar', 'derreter', 'dissolver', 'desligar']

@cli.command(epilog="<duracao> número indicando o tempo de duração. Ex: 20min, 1.5h")
@click.argument('operacao', type=click.Choice(OPERACORES), required=True)
@opcoes_comuns
@click.option('-i','--intensidade', metavar='<intensidade>',  type=click.Choice(['baixo', 'medio', 'alto']), help='Nível de intensidade do fogo.', envvar="INTENSIDADE", show_envvar=True)
@click.option('--fogo', 'fogo', flag_value='fogo', default=True, help="Utilizar o fogo (bocas de cima).")
@click.option('--forno', 'fogo', flag_value='forno', help="Utilizar o forno.")
@click.option('--por', 'duracao', metavar='<duracao>', type=(DuracaoType()), help='Tempo de duração no fogão. Ex: --por 5min')
@click.option('--preaquecido', is_flag=True, help='indica que o forno deve ser pré-aquecido')
@click.argument('ingrediente', nargs=-1)
def fogao(operacao, recipiente, como, ate, intensidade, fogo, duracao, preaquecido, ingrediente):
    """
    Utiliza o fogão para preparar os alimentos.
    """

    local = "Fogão>{}".format(fogo)
    click.echo(texto_completo(operacao,recipiente, como, ate, ingrediente, local, duracao, ('Fogo',intensidade), ('Pré-aquecido',preaquecido)))

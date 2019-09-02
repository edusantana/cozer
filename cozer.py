import click


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




@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('-r','--recipiente','recipiente',metavar='<recipiente>', help='nome do recipiente que será utilizado. Ex: -r panela', envvar="RECIPIENTE", show_envvar=True)
@click.option('--como', 'como', metavar='<descricao>', help='descrição de como deve ser realizado a operação, ex: --como "com cuidado para não quebrar"')
@click.option('--ate', 'ate', metavar='<acontecimento>', help='condição para terminar a operação, ex: --ate "ficar uniforme"')
@click.pass_context
def cli(ctx, recipiente, como, ate):
    """
    Script para auxiliar o aprendizado de leitura de documentação e invocação de comandos.

    Simula realização de modo de preparo de comidas.

    Os comandos assumem que as operações são realizadas em recipientes, ex: "Panela" ou "Frigideira".

    """

    ctx.ensure_object(dict)

    ctx.obj['recipiente'] = recipiente
    ctx.obj['como'] = como
    ctx.obj['ate'] = ate


@cli.command()
@click.option('-u','--utencilio', metavar='<utencilio>', help='utencilio para utilizar ao misturar, ex: -u "colher de pau"')
@click.argument('ingrediente', nargs=-1)
@click.pass_context
def misturar(ctx, utencilio, ingrediente):
    """Mistura ingredientes."""
    click.echo('. Misturar em usando ')

@cli.command()
@click.option('-t','--tirando-de', 'recipiente_anterior',metavar='<RECIPIENTE_ANTERIOR>', help='nome do recipiente de onde será tirado o conteúdo. Utilizado quando deseja-se trocar de recipiente. Ex: --tirando-de panela')
@click.argument('ingrediente', nargs=-1)
@click.pass_context
def colocar(ctx, recipiente_anterior, ingrediente):
    """
    Colocar ingredientes ou trocar de recipiente.

    Pode ser utilizado trocar recipientes, tirando de um colocando em outro.
    """

    recipiente = ctx.obj['recipiente']
    como = ctx.obj['como']
    ate = ctx.obj['ate']

    ingredientes = ", ".join(ingrediente)
    como_msg = "" if (como is None) else ("{}".format(como))
    ate_msg = "" if (ate is None) else ("até {}".format(ate))

    if recipiente_anterior:

        """
        Retirando ingredientes de recipiente
        """
        click.echo('. Retirar %s do(a) %s e colocar no(a) %s %s %s' % (
            ingredientes,
            recipiente_anterior,
            recipiente,
            como_msg,
            ate_msg))
    else:
        click.echo('. Colocar %s no(a) %s %s %s' % (
            ingredientes,
            recipiente,
            como_msg,
            ate_msg))


@cli.command()
@click.argument('ingrediente', nargs=-1)
@click.pass_context
def adicionar(ctx, ingrediente):
    """Adicionar ingredientes em recipientes."""

    recipiente = ctx.obj['recipiente']
    como = ctx.obj['como']
    ate = ctx.obj['ate']

    ingredientes = ", ".join(ingrediente)
    como_msg = "" if (como is None) else ("{}".format(como))
    ate_msg = "" if (ate is None) else ("até {}".format(ate))

    operacao = "adicionar"

    click.echo('. %s %s no(a) %s %s %s' % (
        operacao.capitalize(),
        ingredientes,
        recipiente,
        como_msg,
        ate_msg))


@cli.command(epilog="<duracao> número indicando o tempo de duração. Ex: 20m, 1.5h")
@click.option('-i','--intensidade', metavar='<intensidade>',  type=click.Choice(['baixo', 'medio', 'alto']), help='Nível de intensidade do fogo.', envvar="INTENSIDADE", show_envvar=True,  show_default=True, default="medio")
@click.option('--fogo', 'fogo', flag_value='fogo', default=True, help="Utilizar o fogo (bocas de cima).")
@click.option('--forno', 'fogo', flag_value='forno', help="Utilizar o forno.")
@click.option('--por', 'duracao', metavar='<duracao>', type=(DuracaoType()), help='Tempo de duração no fogão. Ex: --por 5m')
@click.option('--preaquecido', is_flag=True, help='indica que o forno deve ser pré-aquecido')
@click.option('--esquentar', 'operacao', flag_value='esquentar', help='Indica que devemos fritar os ingredientes.')
@click.option('--fritar', 'operacao', flag_value='fritar', help='Indica que devemos fritar os ingredientes.')
@click.option('--cozinhar', 'operacao', flag_value='cozinhar', help='Indica que devemos cozinhar os ingredientes.')
@click.option('--refogar', 'operacao', flag_value='refogar', help='Indica que devemos refogar os ingredientes.')
@click.option('-d', '--desligar', is_flag=True, help='Indica que a chama deve ser desligada depois.')
@click.argument('ingrediente', nargs=-1)
@click.pass_context
def fogao(ctx, intensidade, fogo, duracao, preaquecido, operacao, desligar, ingrediente):
    """
    Utiliza o fogão para aquecer os alimentos.
    """
    recipiente = ctx.obj['recipiente']
    como = ctx.obj['como']
    ate = ctx.obj['ate']

    if operacao is None:
        if desligar:
            click.echo('. Desligar o %s do(a) %s' % (fogo, recipiente ))
        else:
            raise click.BadParameter('Operação no fogão não foi definida. Utilize -h para ajuda.')
    else:

        if preaquecido and fogo == 'forno':
            click.echo('. Preaquecer o forno' )

        como_msg = "" if (como is None) else ("{}".format(como))
        por_msg = "" if (duracao is None) else ("por {0[0]} {0[1]}".format(duracao))
        ate_msg = "" if (ate is None) else ("até {}".format(ate))
        msg = " ".join([por_msg, ate_msg])
        ingredientes = ",".join(ingrediente)


        click.echo('. Usando %s e o %s %s, %s %s, %s %s' % (
            recipiente,
            fogo,
            intensidade,
            operacao,
            ingredientes,
            como_msg,
            msg))

        if desligar:
            click.echo('. Desligar o %s do(a) %s em seguida.' % (fogo, recipiente) )

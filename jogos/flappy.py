from sistemas import SistemaGravidade, SistemaInimigosFlappy,\
    SistemaPlayerBateParedeVertical, PlayerFlappySistema, \
    SistemaPlayerTrocaLadoHorizontal
from jogoabstrato import JogoAbstrato
from entidade import InimigoFlappy, PlayerFlappy


class Flappy(JogoAbstrato):
    def __init__(self, screen, entidades, player, inimigos, plataformas):
        super().__init__(screen, entidades, player, inimigos, plataformas)
        player.velocity = 0
        player.rect.y = 120

    def trocar_player(self, player):
        self.player = PlayerFlappy(player.width, player.height, player.rect.x, 120, player.color)

    def inimigo(self, x, y):
        return InimigoFlappy(x, y, (0, 255, 0))

    def inicializar_sistemas(self):
        self.inimigos_sys = SistemaInimigosFlappy(self.inimigos, self.player, self.plataformas)
        self.sistemas.append(self.inimigos_sys)

        self.sistemas.append(PlayerFlappySistema(self.player))
        self.sistemas.append(SistemaPlayerTrocaLadoHorizontal(self.player))

        super().inicializar_sistemas()

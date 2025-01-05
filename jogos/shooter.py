from sistemas import SistemaInimigosShooter,\
     PlayerShooterSistema, SistemaPlayerBateParedeVertical, SistemaPlayerBateParedeHorizontal
from jogoabstrato import JogoAbstrato
from entidade import InimigoShooter, PlayerShooter


class Shooter(JogoAbstrato):
    def trocar_player(self, player):
        self.player = PlayerShooter(player.width, player.height, player.rect.x, player.rect.y, player.color)

    def inimigo(self, x, y):
        return InimigoShooter(x, y - 8, (0, 255, 0))

    def inicializar_sistemas(self):
        self.inimigos_sys = SistemaInimigosShooter(self.inimigos, self.player, self.plataformas)
        self.sistemas.append(self.inimigos_sys)

        self.sistemas.append(PlayerShooterSistema(self.player))
        self.sistemas.append(SistemaPlayerBateParedeVertical(self.player))
        self.sistemas.append(SistemaPlayerBateParedeHorizontal(self.player))

        super().inicializar_sistemas()

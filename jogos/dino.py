from sistemas import SistemaInimigosDino, SistemaGravidade, PlayerDinoSistema
from jogoabstrato import JogoAbstrato
from entidade import PlayerDino, DinoEnemy


class Dino(JogoAbstrato):
    def trocar_player(self, player):
        self.player = PlayerDino(player.width, player.height, player.rect.x, player.rect.y, player.color)

    def inimigo(self, x, y):
        return DinoEnemy(x, y, (255, 0, 0))

    def inicializar_sistemas(self):
        self.inimigos_sys = SistemaInimigosDino(self.inimigos, self.player, self.plataformas)
        self.sistemas.append(self.inimigos_sys)

        self.sistemas.append(PlayerDinoSistema(self.player))
        self.sistemas.append(SistemaGravidade(self.player, self.plataformas, 0.8, self.inimigos_sys))

        super().inicializar_sistemas()
from sistemas import SistemaInimigosAsteroid,\
     PlayerAsteroidSistema, SistemaPlayerTrocaLadoHorizontal, SistemaPlayerTrocaLadoVertical
from jogoabstrato import JogoAbstrato
from entidade import InimigoAsteroid, PlayerAsteroid


class Asteroid(JogoAbstrato):
    def inimigo(self, x, y):
        return InimigoAsteroid(x, y - 8, (255, 0, 255))

    def trocar_player(self, player):
        self.player = PlayerAsteroid(player.width, player.height, player.rect.x, player.rect.y, player.color)

    def inicializar_sistemas(self):
        asteroid = PlayerAsteroidSistema(self.player)
        self.sistemas.append(asteroid)

        self.inimigos_sys = SistemaInimigosAsteroid(self.inimigos, self.player, self.plataformas, asteroid)
        self.sistemas.append(self.inimigos_sys)

        self.sistemas.append(SistemaPlayerTrocaLadoHorizontal(self.player))
        self.sistemas.append(SistemaPlayerTrocaLadoVertical(self.player))

        super().inicializar_sistemas([asteroid])

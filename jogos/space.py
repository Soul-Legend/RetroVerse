from jogoabstrato import JogoAbstrato
from sistemas import InimigosSpaceSistema,PlayerSpaceSistema, SistemaPlayerBateParedeHorizontal, SistemaGravidade
from entidade import InimigoSpace, PlayerSpace
import random


class Space(JogoAbstrato):
    def inimigo(self, x, y):
        if y > 400:
            y -= 300
        return InimigoSpace(x, y, (255, 0, 255))

    def trocar_player(self, player):
        self.player = PlayerSpace(player.width, player.height, player.rect.x, player.rect.y, player.color)

    def gen_inimigo_coords(self):
        for _ in range(1000):
            x_novo = random.randint(0, 1150)
            y_novo = random.randint(65, 250)
            if not any(abs(x_novo - inimigo.rect.x) < 55 and abs(y_novo - inimigo.rect.y) < 55 for inimigo in self.inimigos)\
                and not abs(x_novo - self.player.rect.x) < 150 and not abs(y_novo - self.player.rect.y) < 150:
                break
        return (x_novo, y_novo)

    def inicializar_sistemas(self):
        space = PlayerSpaceSistema(self.player)
        self.sistemas.append(space)

        self.inimigos_sys = InimigosSpaceSistema(self.inimigos, self.player, self.plataformas, space)
        self.sistemas.append(self.inimigos_sys)

        self.sistemas.append(SistemaPlayerBateParedeHorizontal(self.player))

        super().inicializar_sistemas([space])
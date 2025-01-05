class Highscore:
    def __init__(self):
        self.highscore = self.carregar_highscore()

    def carregar_highscore(self):
        try:
            with open('highscore.txt', 'r') as f:
                return int(f.read())
        except FileNotFoundError:
            return 0

    def salvar_highscore(self, new_highscore):
        with open('highscore.txt', 'w') as f:
            f.write(str(new_highscore))

    def update_highscore(self, score):
        if score > self.highscore:
            self.highscore = score
            self.salvar_highscore(self.highscore)

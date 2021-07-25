from random import random

import pyxel
                                                             ## Definições de atributos, tais como caraterísticas das artes e classes.
titulo = 0
jogo = 1
gameover = 2

player_largura = 5
player_altura = 8
player_velocidade = 2

Bala_largura = 2
Bala_altura = 8
Bala_cor = 11
Bala_velocidade = 4

inimigo_largura = 8
inimigo_altura = 8
inimigo_velocidade = 1.5

Explode_inicio = 1
Explode_fim = 8
Explode_cor_centro = 7
Explode_cor_fora = 10

inimigo_lista = []
Bala_lista = []
Explode_lista = []


def atualiza_lista(list):
    for elem in list:
        elem.atualiza()


def desenha_lista(list):
    for elem in list:
        elem.desenha()


def limpa_lista(list):
    i = 0
    while i < len(list):
        elem = list[i]
        if not elem.alive:
            list.pop(i)
        else:
            i += 1

class Player:                                                ##Definimos os atributos do player para podermos utilizá-lo mais tarde...
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = player_largura
        self.h = player_altura
        self.alive = True

    def atualiza(self):
        if pyxel.btn(pyxel.KEY_LEFT):                                       #Se o "gamer" clicar para a direita vamos mecher no eixo X para que a nave vá para a mesma direção
            self.x -= player_velocidade

        if pyxel.btn(pyxel.KEY_RIGHT):                                      #Se o "gamer" clicar para a esquerda vamos mecher no eixo X para que a nave vá para a mesma direção
            self.x += player_velocidade

        if pyxel.btn(pyxel.KEY_UP):                                         #Se o "gamer" clicar para a cima vamos mecher no eixo X para que a nave vá para a mesma direção
            self.y -= player_velocidade

        if pyxel.btn(pyxel.KEY_DOWN):                                       #Se o "gamer" clicar para baixo vamos mecher no eixo X para que a nave vá para a mesma direção
            self.y += player_velocidade

        self.x = max(self.x, 0)
        self.x = min(self.x, pyxel.width - self.w)
        self.y = max(self.y, 0)
        self.y = min(self.y, pyxel.height - self.h)

        if pyxel.btnp(pyxel.KEY_SPACE):                                              ## ATIRA NO SPACE!
            Bala(   
                self.x + (player_largura - Bala_largura) / 2, self.y - Bala_altura / 2
            )

            pyxel.play(0, 0)

    def desenha(self):
        pyxel.blt(self.x, self.y, 0, 0, 0, self.w, self.h, 0)


class Bala:                                                     ## Definimos a classe "Bala" para termos os atributos do disparo
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = Bala_largura
        self.h = Bala_altura
        self.alive = True

        Bala_lista.append(self)

    def atualiza(self):
        self.y -= Bala_velocidade

        if self.y + self.h - 1 < 0:
            self.alive = False

    def desenha(self):
        pyxel.rect(self.x, self.y, self.w, self.h, Bala_cor)


class Inimigo:                                             #Aqui definimos os alienigenas, os Sith que querem ter domínio sobre a força!
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = inimigo_largura
        self.h = inimigo_altura
        self.dir = 1
        self.alive = True
        self.offset = int(random() * 60)

        inimigo_lista.append(self)

    def atualiza(self):                                   #Como ninguém controla os Sith, faremos com que eles se controlem aleatoriamente!
        if (pyxel.frame_count + self.offset) % 60 < 30:
            self.x += inimigo_velocidade
            self.dir = 1
        else:
            self.x -= inimigo_velocidade
            self.dir = -1

        self.y += inimigo_velocidade

        if self.y > pyxel.height - 1:
            self.alive = False

    def desenha(self):
        pyxel.blt(self.x, self.y, 0, 8, 0, self.w * self.dir, self.h, 0)


class Explode:                                      #Até onde sabemos a vitório não é uma certeza, e se explodirmos?
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = Explode_inicio
        self.alive = True

        Explode_lista.append(self)

    def atualiza(self):
        self.radius += 1

        if self.radius > Explode_fim:
            self.alive = False

    def desenha(self):
        pyxel.circ(self.x, self.y, self.radius, Explode_cor_centro)
        pyxel.circb(self.x, self.y, self.radius, Explode_cor_fora)


class App:                                                                ## A classe mestra dos magos, onde temos tudo e todos
    def __init__(self):
        pyxel.init(120, 160, caption="Spacescape 2.0")

        pyxel.image(0).set(
            0,
            0,
           [    
                "19191919",
                "99999999",
                "66666666",
                "16161616",
            ],
        )
        pyxel.image(0).set(8, 0,
            [
                "00099000",
                "55099055",
                "00599500",

            ],
        )

        self.scene = titulo
        self.score = 0
        self.player = Player(pyxel.width / 2, pyxel.height - 20)

        pyxel.run(self.atualiza, self.desenha)

    def atualiza(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.scene == titulo:
            self.atualiza_cena_titulo()
        elif self.scene == jogo:
            self.atualiza_cena_inicio()
        elif self.scene == gameover:
            self.atualiza_cena_gameover()

    def atualiza_cena_titulo(self):
        if pyxel.btnp(pyxel.KEY_ENTER):
            self.scene = jogo

    def atualiza_cena_inicio(self):
        if pyxel.frame_count % 6 == 0:
            Inimigo(random() * (pyxel.width - player_largura), 0)     

        for a in inimigo_lista:                 
            pyxel.play (1, 1)

        for a in inimigo_lista:                                      ##Aqui temos a situação onde o inimigo é atingido por um projetil
            for b in Bala_lista:
                if (
                    a.x + a.w > b.x
                    and b.x + b.w > a.x
                    and a.y + a.h > b.y
                    and b.y + b.h > a.y
                ):
                    a.alive = False
                    b.alive = False

                    Explode_lista.append(
                        Explode(a.x + inimigo_largura / 2, a.y + inimigo_altura / 2)
                    )

                    pyxel.play(1, 1)

                    self.score += 10

        for inimigo in inimigo_lista:
            if (
                self.player.x + self.player.w > inimigo.x
                and inimigo.x + inimigo.w > self.player.x
                and self.player.y + self.player.h > inimigo.y
                and inimigo.y + inimigo.h > self.player.y
            ):
                inimigo.alive = False   

                Explode_lista.append(                                                    ## e aqui, ele Explode Lol
                    Explode(
                        self.player.x + player_largura / 2,
                        self.player.y + player_altura / 2,
                    )
                )

                pyxel.play(1, 1)

                self.scene = gameover

        self.player.atualiza()                                                  ## Atualizamos os parametros para que o game funcione   
        atualiza_lista(Bala_lista)
        atualiza_lista(inimigo_lista)
        atualiza_lista(Explode_lista)

        limpa_lista(inimigo_lista)
        limpa_lista(Bala_lista)
        limpa_lista(Explode_lista)

    def atualiza_cena_gameover(self):
        atualiza_lista(Bala_lista)
        atualiza_lista(inimigo_lista)
        atualiza_lista(Explode_lista)

        limpa_lista(inimigo_lista)
        limpa_lista(Bala_lista)
        limpa_lista(Explode_lista)

        if pyxel.btnp(pyxel.KEY_ENTER):
            self.scene = jogo
            self.player.x = pyxel.width / 2
            self.player.y = pyxel.height - 20
            self.score = 0

            inimigo_lista.clear()
            Bala_lista.clear()
            Explode_lista.clear()

    def desenha(self):                                ## Que comecem os jogos                         
        pyxel.cls(0)

        if self.scene == titulo:
            self.desenha_cena_titulo()
        elif self.scene == jogo:
            self.desenha_cena_inicio()
        elif self.scene == gameover:
            self.desenha_gameover_scene()

        pyxel.text(39, 4, "PONTOS {:5}".format(self.score), 7)

    def desenha_cena_titulo(self):
        pyxel.text(35, 66, "Spacescape", 15)
        pyxel.text(31, 126, "- APERTA ENTER -", 13)

    def desenha_cena_inicio(self):
        self.player.desenha()
        desenha_lista(Bala_lista)
        desenha_lista(inimigo_lista)
        desenha_lista(Explode_lista)

    def desenha_gameover_scene(self):
        desenha_lista(Bala_lista)
        desenha_lista(inimigo_lista)
        desenha_lista(Explode_lista)

        pyxel.text(43, 66, "MAS JA?", 8)
        pyxel.text(20, 100, "SENTA O DEDO NO ENTER!", 13)


App()
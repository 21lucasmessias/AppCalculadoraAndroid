#-*-coding:utf8;-*-
#qpy:2
#qpy:kivy

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.effects.scroll import ScrollEffect
from math import sqrt, pow
import __future__


class Manager(ScreenManager):
    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        self.transition = NoTransition()


class Menu(Screen):
    pass


class Calculadora(Screen):
    def __init__(self, **kwargs):
        super(Calculadora, self).__init__(**kwargs)
        self.start = True
        self.renew = True
        self.simb = False
        self.enter = False
        self.calcular = False
        self.zero_div = False
        self.negativo = False
        self.cont_halign = 0
        self.font_size = 0
        self.calculo = []
        self.lpc = 0
        self.lc = 0

    def whenstart(self):
        self.ids.scrollview_1.effect_x = ScrollEffect()
        self.ids.scrollview_2.effect_x = ScrollEffect()
        self.ids.scrollview_1.bar_width = 0
        self.ids.scrollview_2.bar_width = 0
        self.font_size = self.ids.tela_1.font_size
        self.start = False

    def halign_tela(self, obj):
        if self.start:
            self.whenstart()
        obj.text_size = (None, obj.height)
        obj.texture_update()
        obj.text_size = max(obj._label.content_width, obj.parent.width), obj.height
        if self.cont_halign < 5:
            if obj.text_size[0] > obj.parent.width:
                obj.font_size = obj.font_size * 0.9
                self.cont_halign += 1

    def press_numero(self, numero):
        join_calculo = ''
        if self.renew:
            del self.calculo[:]
            self.calculo.append(numero)
            self.ids.tela_2.text = ''
            self.lpc = 1
            self.lc = 1
            if numero == '0':
                self.renew = True
            else:
                self.renew = False
        else:
            if self.simb:
                self.calculo.append(numero)
                self.lpc += 1
                self.lc = 1
                self.simb = False
            elif numero == '0' and self.calculo[self.lpc - 1] == '0':
                pass
            elif self.calculo[self.lpc - 1] == '0':
                self.calculo[self.lpc - 1] = numero
            else:
                self.calculo[self.lpc - 1] += numero
                self.lc += 1
        self.ids.tela_1.text = '{}'.format(join_calculo.join(self.calculo))
        try:
            if self.calcular:
                self.ids.tela_2.text = str(eval(compile(self.ids.tela_1.text, '<string>', 'eval',
                                                        __future__.division.compiler_flag)))
                if self.ids.tela_2.text[-2:] == '.0':
                    self.ids.tela_2.text = self.ids.tela_2.text[:-2]
                self.zero_div = False
        except ZeroDivisionError:
            self.zero_div = True
        # print(self.calculo)

    def press_ponto(self):
        join_calculo = ''
        if self.lc > 0:
            if '.' not in self.calculo[self.lpc - 1]:
                self.calculo[self.lpc - 1] += '.'
                self.ids.tela_1.text = join_calculo.join(self.calculo)
                self.lc += 1
                self.renew = False
        else:
            self.calculo.append('0.')
            self.ids.tela_1.text = join_calculo.join(self.calculo)
            self.lpc += 1
            self.lc = 2
            self.simb = False
            self.renew = False

    def press_sinal(self, sinal):
        join_calculo = ''
        if self.zero_div:
            self.calculo.pop(self.lpc - 1)
            self.lpc -= 1
            self.lc = 0
            self.calculo[self.lpc - 1] = sinal
            self.zero_div = False
            self.simb = True
        elif self.lpc % 2 != 0:
            if self.renew:
                self.renew = False
                self.lpc = 2
            else:
                self.lpc += 1
            self.calculo.append(sinal)
            self.lc = 0
            self.simb = True
            self.calcular = True
        elif self.lpc % 2 == 0 and not self.renew:
            self.calculo[self.lpc - 1] = sinal
        self.ids.tela_1.text = join_calculo.join(self.calculo)

    def press_negativo(self, sinal):
        join_calculo = ''
        if self.zero_div:
            self.calculo.pop(self.lpc - 1)
            self.lpc -= 1
            self.lc = 0
            self.calculo[self.lpc - 1] = sinal
            self.zero_div = False
            self.simb = True
        elif self.lpc % 2 != 0:
            if self.renew:
                self.renew = False
                self.lpc = 2
            else:
                self.lpc += 1
            self.calculo.append(sinal)
            self.lc = 0
            self.simb = True
            self.calcular = True
        elif self.lpc % 2 == 0 and not self.renew:
            self.calculo[self.lpc - 1] = sinal
        self.ids.tela_1.text = join_calculo.join(self.calculo)

    def press_c(self):
        self.ids.tela_1.text = ''
        self.ids.tela_2.text = ''
        self.ids.tela_1.font_size = self.font_size
        self.cont_halign = 0
        self.lc = 0
        self.lpc = 0
        del self.calculo[:]
        self.renew = True
        self.simb = False
        self.enter = False
        self.calcular = False
        self.zero_div = False

    def resultado(self):
        del self.calculo[:]
        if self.lpc == 0:
            return
        if len(self.ids.tela_2.text) > 0:
            self.calculo.append(self.ids.tela_2.text)
            self.ids.tela_2.text = ''
        else:
            self.calculo.append(self.ids.tela_1.text)
        self.lc = len(self.ids.tela_1.text)
        self.enter = True
        if self.zero_div:
            self.ids.tela_1.text = ''
            self.zero_div = False
            del self.calculo[:]
            self.lpc = 0
            self.ids.tela_2.text = 'Divisao por zero'
        else:
            self.lpc = 1
            self.ids.tela_1.text = self.calculo[0]
        self.lc = len(self.ids.tela_1.text)
        self.renew = True
        self.calcular = False

    def press_backspace(self):
        join_calculo = ''
        if self.lc > 0:
            self.calculo[self.lpc - 1] = self.calculo[self.lpc - 1][:-1]
            self.ids.tela_1.text = join_calculo.join(self.calculo)
            self.lc -= 1
            if self.lc == 0:
                del self.calculo[self.lpc - 1]
                self.lpc -= 1
                if self.lpc > 0:
                    self.lc = len(self.calculo[self.lpc - 1])
                else:
                    self.press_c()
        try:
            if self.calcular and self.lpc % 2 != 0:
                self.ids.tela_2.text = str(eval(compile(self.ids.tela_1.text, '<string>', 'eval',
                                                        __future__.division.compiler_flag)))
                if self.ids.tela_2.text[-2:] == '.0':
                    self.ids.tela_2.text = self.ids.tela_2.text[:-2]
        except ZeroDivisionError:
            pass
        except Exception as erro:
            print(erro)


class TestApp(App):
    def build(self):
        return Manager()


TestApp().run()

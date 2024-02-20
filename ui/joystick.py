import sys
import pygame
from pygame.locals import *
from classe.axis import Axis
from server.send_udp_msg import udpMsg
from ui.constants import Colors
from classe.button import Button


def desenha_texto_no_centro(window, fonte, texto, cor, delta_y=0):
    img_texto = fonte.render(texto, True, cor)
    # Queremos centralizar o texto e sabemos as dimensões da janela e do texto
    texto_x = int(window.get_width() / 2 - img_texto.get_width() / 2)
    texto_y = 20
    window.blit(img_texto, (texto_x, texto_y))


def desenha_texto(window, fonte, texto, cor, delta_y=0, delta_x=0):
    img_texto = fonte.render(texto, True, cor)
    window.blit(img_texto, (delta_x, delta_y))


def joystick():
    # graphics
    nickNameDisplay = 'RACER RC CAR'
    width, height = 390, 500
    pygame.init()
    pygame.display.set_caption(nickNameDisplay)
    screen = pygame.display.set_mode((width, height), 0, 32)
    clock = pygame.time.Clock()

    default_font_name = pygame.font.get_default_font()
    font = pygame.font.Font(default_font_name, 24)
    font1 = pygame.font.Font(default_font_name, 15)
    font2 = pygame.font.Font(default_font_name, 30)

    lin1 = 310
    lin2 = 370
    lin3 = 430

    Colum1 = 20
    Colum2 = 110
    Colum3 = 200
    Colum4 = 290

    move_volante = False

    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

    for joystick in joysticks:
        print("joystick name:" + joystick.get_name())

    # joystickCar
    button_farol = Button('Farol', 'FAROL', 3, lin1, Colum1, 80, Colors.blue, Colors.red, [0, 1])
    button_milha = Button('Farol AUX', 'AUX', 0, lin1, Colum2, 80, Colors.blue, Colors.red, [0, 1])
    button_sd = Button('Seta Direita', 'SETADIR', 5, lin1, Colum4, 80, Colors.blue, Colors.red, [0, 1])
    button_se = Button('Seta Esquerda', 'SETAESQ', 4, lin1, Colum3, 80, Colors.blue, Colors.red, [0, 1])

    button_RE = Button('RE', 'RE', 11, lin2, Colum3, 80, Colors.blue, Colors.red, [0, 1])
    button_marcha = Button('marcha', 'MARCHA', 1, lin2, Colum1, 80, Colors.blue, Colors.red,
                           [30, 50, 70, 100])  # 30,50,70,100
    button_4x4 = Button('TRAÇÃO', '4X4', 2, lin2, Colum2, 80, Colors.blue, Colors.red, [0, 1])

    button_D = Button('Func_axis_D', 'D', 10, lin3, Colum1, 80, Colors.blue, Colors.red, [0, 1])

    volante = Axis('Volante', 'V', 0, 50, False, -100, 100, 0, 100, Colors.blue, Colors.red)
    acelerador = Axis('Acelerador', 'A', 2, 0, True, 100, -100, 0, 100, Colors.blue, Colors.red)
    acelerador.setmaxout(button_marcha.buttonvelue())

    linha_ini_a, coluna_ini_a = 100, 250
    altura_fim_a, largura_fim_a = 200, 60

    linha_ini_v, coluna_ini_v = 100, 20
    altura_fim_v, largura_fim_v = 200, 200

    while True:

        screen.fill(Colors.black)

        desenha_texto_no_centro(screen, font2, nickNameDisplay, Colors.white, 1)

        desenha_texto(screen, font1, '<-- Volante --> ', Colors.white, 80, 70)
        pygame.draw.rect(screen, Colors.white, [coluna_ini_v, linha_ini_v, largura_fim_v + 10, altura_fim_v])
        pygame.draw.rect(screen, Colors.blue,
                         pygame.Rect([coluna_ini_v + (volante.getvelueout() * 2), linha_ini_v, 10, altura_fim_v]))

        desenha_texto(screen, font1, 'Acelerador', Colors.white, 80, 240)
        pygame.draw.rect(screen, Colors.white, [coluna_ini_a, linha_ini_a, largura_fim_a, altura_fim_a])
        pygame.draw.rect(screen, Colors.blue,
                         pygame.Rect(
                             [coluna_ini_a, altura_fim_a + linha_ini_a - (acelerador.getvelueout() * 2), largura_fim_a,
                              (acelerador.getvelueout() * 2)]))

        pygame.draw.rect(screen, button_farol.coloraction,
                         [button_farol.columbutton, button_farol.linbutton, button_farol.sizebutton, 50])
        desenha_texto(screen, font1, button_farol.tag, Colors.white, button_farol.linbutton + 6,
                      button_farol.columbutton + 14)
        desenha_texto(screen, font1, 'Ligado' if button_farol.status else 'Desligado', Colors.white,
                      button_farol.linbutton + 28,
                      button_farol.columbutton + (14 if button_farol.status else 5))

        pygame.draw.rect(screen, button_milha.coloraction,
                         [button_milha.columbutton, button_milha.linbutton, button_milha.sizebutton, 50])
        desenha_texto(screen, font1, button_milha.tag, Colors.white, button_milha.linbutton + 6,
                      button_milha.columbutton + 18)
        desenha_texto(screen, font1, 'Ligado' if button_milha.status else 'Desligado', Colors.white,
                      button_milha.linbutton + 28,
                      button_milha.columbutton + (14 if button_milha.status else 5))

        pygame.draw.rect(screen, button_se.coloraction,
                         [button_se.columbutton, button_se.linbutton, button_se.sizebutton, 50])
        desenha_texto(screen, font1, button_se.tag, Colors.white, button_se.linbutton + 6, button_se.columbutton + 6)
        desenha_texto(screen, font1, 'Ligado' if button_se.status else 'Desligado', Colors.white,
                      button_se.linbutton + 28, button_se.columbutton + (14 if button_se.status else 5))

        pygame.draw.rect(screen, button_sd.coloraction,
                         [button_sd.columbutton, button_sd.linbutton, button_sd.sizebutton, 50])
        desenha_texto(screen, font1, button_sd.tag, Colors.white, button_sd.linbutton + 6, button_sd.columbutton + 6)
        desenha_texto(screen, font1, 'Ligado' if button_sd.status else 'Desligado', Colors.white,
                      button_sd.linbutton + 28, button_sd.columbutton + (14 if button_sd.status else 5))

        pygame.draw.rect(screen, button_RE.coloraction,
                         [button_RE.columbutton, button_RE.linbutton, button_RE.sizebutton, 50])
        desenha_texto(screen, font1, button_RE.tag, Colors.white, button_RE.linbutton + 6, button_RE.columbutton + 12)
        desenha_texto(screen, font1, 'D' if button_RE.status else 'R', Colors.white,
                      button_RE.linbutton + 28, button_RE.columbutton + (14 if button_RE.status else 5))

        # linha_ini, coluna_ini, linha_fim, coluna_fim
        pygame.draw.rect(screen, button_marcha.coloraction,
                         [button_marcha.columbutton, button_marcha.linbutton, button_marcha.sizebutton, 50])
        desenha_texto(screen, font1, button_marcha.tag, Colors.white, button_marcha.linbutton + 6,
                      button_marcha.columbutton + 6)

        match (button_marcha.buttonvelue()):
            case 30:
                value = 1
            case 50:
                value = 2
            case 70:
                value = 3
            case 100:
                value = 4
            case _:
                value = 0
        desenha_texto(screen, font, str(value), Colors.white, button_marcha.linbutton + 24,
                      button_marcha.columbutton + 25)

        pygame.draw.rect(screen, button_4x4.coloraction,
                         [button_4x4.columbutton, button_4x4.linbutton, button_4x4.sizebutton, 50])
        desenha_texto(screen, font1, button_4x4.name, Colors.white, button_4x4.linbutton + 6,
                      button_4x4.columbutton + 6)
        desenha_texto(screen, font, '4x4' if button_4x4.status else '4x2', Colors.white, button_4x4.linbutton + 22,
                      button_4x4.columbutton + 20)

        for event in pygame.event.get():

            if event.type == JOYBUTTONDOWN:
                # print(event)

                if event.button == button_farol.hardwarebutton:
                    button_farol.buttonaction()

                if event.button == button_milha.hardwarebutton:
                    button_milha.buttonaction()

                if event.button == button_sd.hardwarebutton:
                    if button_se.status:
                        button_se.buttonaction()
                    button_sd.buttonaction()

                if event.button == button_se.hardwarebutton:
                    if button_sd.status:
                        button_sd.buttonaction()
                    button_se.buttonaction()

                if event.button == button_4x4.hardwarebutton:
                    button_4x4.buttonaction()

                if event.button == button_marcha.hardwarebutton:
                    button_marcha.buttonoptions()
                    acelerador.setmaxout(button_marcha.buttonvelue())

                if event.button == button_RE.hardwarebutton:
                    button_RE.buttonaction()

            # if event.type == JOYBUTTONUP:
            #     print(event)

            if event.type == JOYAXISMOTION:
                if event.axis == 0:
                    volante.setvelue((round(event.value, 2) * 100))

                    # controle das funcoes do pisca
                    if button_se.status and volante.getvelueout() >= 45:
                        if volante.getvelueout() == 45:
                            move_volante = True

                        if move_volante and volante.getvelueout() >= 50:
                            button_se.buttonaction()
                            move_volante = False

                    if button_sd.status and volante.getvelueout() <= 55:
                        if volante.getvelueout() == 55:
                            move_volante = True

                        if move_volante and volante.getvelueout() <= 50:
                            button_sd.buttonaction()
                            move_volante = False

                if event.axis == 2:
                    acelerador.setvelue((round(event.value, 2) * 100))
                    # Para nova versão relizar tratamento para o camando abaixo
                    # ir para classe necessario revisão rcCArServer Arduino
                    udpMsg(['{ ' + acelerador.tag + ' : ' + str(
                        acelerador.getvelueout()) + ' , ' + button_RE.tag + ' : ' + str(
                        button_RE.buttonvelue()) + ' }'])

                # if event.axis == 3:
                #     print('Eixo: ' + str(event.axis) + ' Val: ' + str(round(event.value,2)*100))
                #     freio = (round(event.value, 2) * 100)
                #     udpMsg(['{ "F" : ' + str(freio) + ' }'])

            # if event.type == JOYAXISMOTION:
            #     print(event)
            # if event.axis < 2:
            # motion[event.axis] = event.value

            # if event.type == JOYHATMOTION:
            # print(event)

            if event.type == JOYDEVICEADDED:
                joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
                for joystick in joysticks:
                    print("joystick name:" + joystick.get_name())

            if event.type == JOYDEVICEREMOVED:
                joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

            if event.type == QUIT:
                print("QUIT" + joystick.get_name())
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                print("KEYDOWN" + joystick.get_name())
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(60)

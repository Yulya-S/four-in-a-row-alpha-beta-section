from game import Game
import pyglet

game = Game()

# Создание окна pyglet
window = pyglet.window.Window(500, 440)
pyglet.gl.glClearColor(1, 1, 1, 1)


# Обработка движения мыши
@window.event()
def on_mouse_motion(x, y, dx, dy):
    # блокировка мыши после окончания игры
    if not game.winner:
        game.mark_mouse(x)


# Обработка клика мышью
@window.event
def on_mouse_press(x, y, buttons, modifiers):
    # блокировка мыши после окончания игры
    if not game.winner:
        game.press()


# Рисование интерфейса
@window.event
def on_draw():
    window.clear()
    # проверка окончания игры
    if not game.winner:
        game.end
    game.draw()


# Запуск приложения
pyglet.app.run()

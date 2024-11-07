from game import Game
import pyglet

game = Game()

window = pyglet.window.Window(500, 440)
pyglet.gl.glClearColor(1,1,1,1)

@window.event()
def on_mouse_motion(x, y, dx, dy):
    if not game.winner:
        game.mark_mouse(x)


@window.event
def on_mouse_press(x, y, buttons, modifiers):
    if not game.winner:
        game.press()

@window.event
def on_draw():
    window.clear()
    if not game.winner:
        game.end
    game.draw()


pyglet.app.run()

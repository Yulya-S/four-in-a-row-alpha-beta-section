import game

g = game.four_in_line()
end = True

while end:
    g.draw()
    end = g.play()
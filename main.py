import game

if __name__ == '__main__':
    # create the game object
    g = game
    t = g.Game()
    t.show_start_screen()
    while True:
        t.new()
        t.run()
        t.show_go_screen()

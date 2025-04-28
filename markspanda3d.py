from direct.showbase.ShowBase import ShowBase

class MyApp(ShowBase):
    def __init__(self):
        super().__init__()       # initialize the Panda3D engine
        # (At this point you’ll see an empty window with a 3D camera.)

if __name__ == "__main__":
    app = MyApp()
    app.run()                   # start the main loop

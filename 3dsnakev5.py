from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3, LineSegs, NodePath
from direct.gui.OnscreenText import OnscreenText
import sys
import random

class Snake3DGame(ShowBase):
    def __init__(self):
        super().__init__()
        self.game_close = False
        # Disable default camera controls and set an isometric view
        self.disableMouse()
        self.step = 1                # movement increment
        self.grid_size = 10          # grid spans from -10 to +10 on x and y
        self.layer_count = 10         # number of Z-layers
        self.move_interval = 0.2     # seconds between moves
        self.elapsed = 0             # accumulator for timing

        # Camera positioning for a clear 3D view
        cam_dist = self.grid_size * 1.5
        cam_height = self.grid_size * .8
        cam_tilt = self.grid_size * 1
        self.camera.setPos(cam_tilt , -cam_dist, cam_height)
        self.camera.lookAt(0, 0, 0)

        # Draw grid lines on every layer and cube edges
        self.draw_grid()
        self.draw_border_edges()

        #reset and quit screens
        self.end_text = OnscreenText(text="", pos=(0,0.2), scale=0.1, fg=(1,0,0,1),mayChange=True)
        self.prompt_text = OnscreenText(text="", pos=(0,-0.2), scale=0.07, fg=(1,1,1,1), mayChange=True)
        self.reset_game()

    def reset_game(self):
        #destroy old nodes
        for node in getattr(self, 'snake_nodes', []):
            node.removeNode()
        getattr(self, 'food_node', NodePath()).removeNode()
        
        #reset flags and hidden text
        self.game_close = False
        self.end_text.setText("")
        self.prompt_text.setText("")

        # Initial snake direction and position (center layer)
        self.direction = Vec3(self.step, 0, 0)
        start_z = 0  # middle layer
        self.snake_positions = [
            Vec3(0, 0, start_z),
            Vec3(-self.step, 0, start_z),
            Vec3(-2*self.step, 0, start_z)
        ]
        self.snake_nodes = []
        for pos in self.snake_positions:
            node = self.loader.loadModel("models/box")
            node.reparentTo(self.render)
            node.setScale(0.5)
            node.setPos(pos)
            self.snake_nodes.append(node)
            node.setColor(0, 255, 0, 1)

        # Spawn the first food in 3D space
        self.spawn_food()

        # Controls: arrow keys for X/Y, Z/X for up/down layers
        self.accept("arrow_up",    self.set_direction, [Vec3(0,  self.step, 0)])
        self.accept("arrow_down",  self.set_direction, [Vec3(0, -self.step, 0)])
        self.accept("arrow_left",  self.set_direction, [Vec3(-self.step, 0, 0)])
        self.accept("arrow_right", self.set_direction, [Vec3(self.step,  0, 0)])
        self.accept("z",           self.set_direction, [Vec3(0, 0,  self.step)])
        self.accept("x",           self.set_direction, [Vec3(0, 0, -self.step)])
        self.accept("c",           self.on_restart)
        self.accept("q",           self.on_quit)

        # Main update task
        self.taskMgr.remove("update")
        self.taskMgr.add(self.update, "update")

    def draw_grid(self):
        # Draw and color grid
        segs = LineSegs()
        segs.setColor(0, 0, 255, 1)
        segs.setThickness(1.0)
        half = (self.grid_size // 2) * self.step
        for layer in range(self.layer_count):
            z = (layer - self.layer_count // 2) * self.step
            for i in range(-half, half + 1, self.step):
                # horizontal line
                segs.moveTo(-half, i, z)
                segs.drawTo(half, i, z)
                # vertical line
                segs.moveTo(i, -half, z)
                segs.drawTo(i, half, z)
        grid_node = segs.create()
        NodePath(grid_node).reparentTo(self.render)

    def draw_border_edges(self):
        # Draw the cube edges (vertical and horizontal borders)
        segs = LineSegs()
        segs.setColor(1, 1, 1, 1)
        segs.setThickness(2.0)
        half = (self.grid_size // 2) * self.step
        # Horizontal square on each layer
        for layer in range(self.layer_count):
            z = (layer - self.layer_count // 2) * self.step
            segs.moveTo(-half, -half, z)
            segs.drawTo( half, -half, z)
            segs.drawTo( half,  half, z)
            segs.drawTo(-half,  half, z)
            segs.drawTo(-half, -half, z)
        # Vertical edges
        for x in (-half, half):
            for y in (-half, half):
                segs.moveTo(x, y, -half)
                segs.drawTo(x, y,  half)
        border_node = segs.create()
        NodePath(border_node).reparentTo(self.render)

    def set_direction(self, new_dir):
        # Prevent immediate reversal
        if new_dir + self.direction != Vec3(0, 0, 0):
            self.direction = new_dir

    def spawn_food(self):
        # Remove old food if present
        if hasattr(self, 'food_node'):
            self.food_node.removeNode()
        # Random X, Y, and layer
        limit = self.grid_size // 2
        x = random.randint(-limit, limit) * self.step
        y = random.randint(-limit, limit) * self.step
        layer = random.randint(0, self.layer_count - 1)
        z = (layer - self.layer_count // 2) * self.step
        self.food_pos = Vec3(x, y, z)
        # Create food node
        self.food_node = self.loader.loadModel("models/box")
        self.food_node.reparentTo(self.render)
        self.food_node.setColor(1, 0, 0, 1)
        self.food_node.setScale(0.5)
        self.food_node.setPos(self.food_pos)

    def update(self, task):
        if self.game_close:
            return task.cont
        dt = globalClock.getDt()
        self.elapsed += dt
        if self.elapsed < self.move_interval:
            return task.cont
        self.elapsed = 0

        # Compute new head and check collisions
        new_head = self.snake_positions[0] + self.direction
        half = (self.grid_size // 2) * self.step
        max_z = (self.layer_count // 2) * self.step
        # Wall collisions in X/Y
        if abs(new_head.x) > half or abs(new_head.y) > half:
            self.trigger_game_over(); return task.cont

        # Layer collisions
        if abs(new_head.z) > max_z:
            self.trigger_game_over(); return task.cont

        # Self-collision
        if new_head in self.snake_positions:
            self.trigger_game_over(); return task.cont

        # Move snake body
        self.snake_positions = [new_head] + self.snake_positions[:-1]
        for pos, node in zip(self.snake_positions, self.snake_nodes):
            node.setPos(pos)

        # Eating food
        if new_head == self.food_pos:
            tail = self.snake_positions[-1]
            self.snake_positions.append(tail)
            node = self.loader.loadModel("models/box")
            node.setColor(0, 255, 0, 1)
            node.reparentTo(self.render)
            node.setScale(0.5)
            node.setPos(tail)
            self.snake_nodes.append(node)
            self.spawn_food()

        return task.cont
    def trigger_game_over(self):
        self.game_close = True
        self.end_text.setText("you've been hacked thank you ;)")
        self.prompt_text.setText("Press C to play again or Q to quit")

    def on_quit(self):
        if self.game_close:
            sys.exit()

    def on_restart(self):
        if self.game_close:
            self.reset_game()

if __name__ == "__main__":
    # Requires panda3d-models: pip install panda3d-models
    game = Snake3DGame()
    game.run()

from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3, LineSegs, NodePath
import random

class Snake3DGame(ShowBase):
    def __init__(self):
        super().__init__()
        # Disable default camera controls and set an isometric view
        self.disableMouse()
        self.step = 1                # movement increment
        self.grid_size = 20          # grid spans from -10 to +10 on x and y
        self.layer_count = 3         # number of Z-layers
        self.move_interval = 0.2     # seconds between moves
        self.elapsed = 0             # accumulator for timing

        # Camera positioning for a clear 3D view
        mid_layer = self.layer_count // 2
        cam_dist = self.grid_size * 1.5
        cam_height = self.grid_size * 1.5
        self.camera.setPos(0, -cam_dist, cam_height)
        self.camera.lookAt(0, 0, 0)

        # Draw grid and border on the base plane (z=0)
        self.draw_grid()
        self.draw_border()

        # Initial snake direction and position (center layer)
        self.direction = Vec3(self.step, 0, 0)
        start_z = 0
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

        # Spawn the first food in 3D space
        self.spawn_food()

        # Controls: arrow keys for X/Y, Z/X for up/down layers
        self.accept("arrow_up",    self.set_direction, [Vec3(0,  self.step, 0)])
        self.accept("arrow_down",  self.set_direction, [Vec3(0, -self.step, 0)])
        self.accept("arrow_left",  self.set_direction, [Vec3(-self.step, 0, 0)])
        self.accept("arrow_right", self.set_direction, [Vec3(self.step,  0, 0)])
        self.accept("z",           self.set_direction, [Vec3(0, 0,  self.step)])
        self.accept("x",           self.set_direction, [Vec3(0, 0, -self.step)])

        # Main update task
        self.taskMgr.add(self.update, "update")

    def draw_grid(self):
        # Draw grid lines on z=0 plane
        lines = LineSegs()
        lines.setColor(0.7, 0.7, 0.7, 1)
        lines.setThickness(1.0)
        limit = (self.grid_size // 2) * self.step
        for i in range(-limit, limit + 1, self.step):
            # Horizontal line
            lines.moveTo(-limit, i, 0)
            lines.drawTo(limit, i, 0)
            # Vertical line
            lines.moveTo(i, -limit, 0)
            lines.drawTo(i, limit, 0)
        node = lines.create()
        grid_np = NodePath(node)
        grid_np.reparentTo(self.render)

    def draw_border(self):
        # Draw border around the grid
        border = LineSegs()
        border.setColor(1, 1, 1, 1)
        border.setThickness(3.0)
        limit = (self.grid_size // 2) * self.step
        border.moveTo(-limit, -limit, 0)
        border.drawTo(limit, -limit, 0)
        border.drawTo(limit, limit, 0)
        border.drawTo(-limit, limit, 0)
        border.drawTo(-limit, -limit, 0)
        node = border.create()
        border_np = NodePath(node)
        border_np.reparentTo(self.render)

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
        dt = globalClock.getDt()
        self.elapsed += dt
        if self.elapsed < self.move_interval:
            return task.cont
        self.elapsed = 0

        # Compute new head and check collisions
        new_head = self.snake_positions[0] + self.direction
        limit = (self.grid_size // 2) * self.step
        # Wall collisions in X/Y
        if abs(new_head.x) > limit or abs(new_head.y) > limit:
            print("Game Over: hit wall")
            return task.done
        # Layer collisions
        max_z = (self.layer_count // 2) * self.step
        if abs(new_head.z) > max_z:
            print("Game Over: out of layer bounds")
            return task.done
        # Self-collision
        if new_head in self.snake_positions:
            print("Game Over: hit self")
            return task.done

        # Move snake body
        self.snake_positions = [new_head] + self.snake_positions[:-1]
        for pos, node in zip(self.snake_positions, self.snake_nodes):
            node.setPos(pos)

        # Eating food
        if new_head == self.food_pos:
            tail = self.snake_positions[-1]
            self.snake_positions.append(tail)
            node = self.loader.loadModel("models/box")
            node.reparentTo(self.render)
            node.setScale(0.5)
            node.setPos(tail)
            self.snake_nodes.append(node)
            self.spawn_food()

        return task.cont

if __name__ == "__main__":
    # Requires panda3d-models: pip install panda3d-models
    game = Snake3DGame()
    game.run()

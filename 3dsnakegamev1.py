from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3
import random

class SnakeGame(ShowBase):
    def __init__(self):
        super().__init__()
        # Disable the default mouse-based camera control
        self.disableMouse()
        # Position and orient the camera
        self.camera.setPos(0, -30, 20)
        self.camera.lookAt(0, 0, 0)

        # Grid and movement settings
        self.step = 1            # grid size per move
        self.grid_size = 20      # total grid extends from -10 to +10
        self.direction = Vec3(self.step, 0, 0)
        self.move_interval = 0.2  # seconds between moves
        self.elapsed = 0         # time accumulator

        # Initialize snake (3 segments)
        self.snake_positions = [
            Vec3(0, 0, 0),
            Vec3(-self.step, 0, 0),
            Vec3(-2*self.step, 0, 0)
        ]
        self.snake_nodes = []
        for pos in self.snake_positions:
            node = self.loader.loadModel("models/box")  # requires panda3d-models
            node.reparentTo(self.render)
            node.setScale(0.5)
            node.setPos(pos)
            self.snake_nodes.append(node)

        # Spawn the first food
        self.spawn_food()

        # Key controls
        self.accept("arrow_up", self.set_direction, [Vec3(0, self.step, 0)])
        self.accept("arrow_down", self.set_direction, [Vec3(0, -self.step, 0)])
        self.accept("arrow_left", self.set_direction, [Vec3(-self.step, 0, 0)])
        self.accept("arrow_right", self.set_direction, [Vec3(self.step, 0, 0)])

        # Add the update task
        self.taskMgr.add(self.update, "update")

    def set_direction(self, new_dir):
        # Prevent reversing directly onto itself
        if new_dir + self.direction != Vec3(0, 0, 0):
            self.direction = new_dir

    def spawn_food(self):
        # Remove old food node if exists
        if hasattr(self, 'food_node'):
            self.food_node.removeNode()
        # Random position within grid
        x = random.randint(-self.grid_size//2, self.grid_size//2) * self.step
        y = random.randint(-self.grid_size//2, self.grid_size//2) * self.step
        self.food_pos = Vec3(x, y, 0)
        # Create a red box as food
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

        # Compute new head position
        new_head = self.snake_positions[0] + self.direction

        # Check wall collision
        limit = (self.grid_size // 2) * self.step
        if abs(new_head.x) > limit or abs(new_head.y) > limit:
            print("Game Over: hit wall")
            return task.done

        # Check self-collision
        if new_head in self.snake_positions:
            print("Game Over: hit self")
            return task.done

        # Move snake: update positions list
        self.snake_positions = [new_head] + self.snake_positions[:-1]
        # Update node positions
        for pos, node in zip(self.snake_positions, self.snake_nodes):
            node.setPos(pos)

        # Check food collision
        if new_head == self.food_pos:
            # Grow snake by adding a segment at the tail
            tail = self.snake_positions[-1]
            self.snake_positions.append(tail)
            node = self.loader.loadModel("models/box")
            node.reparentTo(self.render)
            node.setScale(0.5)
            node.setPos(tail)
            self.snake_nodes.append(node)
            # Spawn new food
            self.spawn_food()

        return task.cont

if __name__ == "__main__":
    # Make sure you have installed panda3d-models: pip install panda3d-models
    game = SnakeGame()
    game.run()
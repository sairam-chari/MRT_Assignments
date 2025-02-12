import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray, String
import argparse
param = 1
class ObstacleNavigation(Node):
    def __init__(self):
        super().__init__("obstacle_navigation")

        if param==1:
            self.declare_parameter('start_x', 0)
            self.declare_parameter('start_y', 0)
            self.declare_parameter('goal_x', 0)
            self.declare_parameter('goal_y', 0)

            start_x = self.get_parameter('start_x').get_parameter_value().integer_value
            start_y = self.get_parameter('start_y').get_parameter_value().integer_value
            goal_x = self.get_parameter('goal_x').get_parameter_value().integer_value
            goal_y = self.get_parameter('goal_y').get_parameter_value().integer_value
        if param==0:
            start_x = 0
            start_y = 0
            goal_x = 0
            goal_y = 0
        self.current_position = (start_x, start_y)
        self.goal_position = (goal_x, goal_y)
        self.steps_taken = 0
        self.path = []
        self.pf = False

        
        self.create_subscription(
            Float32MultiArray, 
            "/obstacle_coordinates", 
            self.obstacle_callback, 
            10
        )

        
        self.status_publisher = self.create_publisher(String, "/navigation/status", 10)
        if param==0:
            self.create_subscription(Float32MultiArray, "/target_coordinates", self.target_callback, 10)

    def target_callback(self, msg):
        self.goal_position = tuple(msg.data)
        self.pf = False
        self.steps_taken = 0
    def obstacle_callback(self, msg):
        
        array = msg.data
        x = int(array[0])
        y = int(array[1])
        grid = array[2:]  

        
        obstacle_grid = [
            [grid[i * x + j] for j in range(x)] for i in range(y)
        ]

        self.get_logger().info(f"Received grid: {x}x{y}")
        self.get_logger().info(f"Current position: {self.current_position}")
        self.get_logger().info(f"Goal position: {self.goal_position}")

        
        self.navigate(obstacle_grid)
        if self.pf:
            self.get_logger().info(f"Goal reached in {self.steps_taken} steps")
            self.status_publisher.publish(String(data=f"Goal Reached in {self.steps_taken} steps"))
        else:
            self.get_logger().info("Path not possible")
            self.status_publisher.publish(String(data="Path not possible"))

    def navigate(self, obstacle_grid):
        """
        Navigate towards the goal using a simple pathfinding logic.
        Returns True if the goal is reached, False if a path is not possible.
        """
        goal_x, goal_y = self.goal_position
        curr_x, curr_y = self.current_position

        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]  

        queue = [(curr_x, curr_y, 0)]  

        while queue and not self.pf:
            x, y, steps = queue.pop(0)
            self.current_position = (x, y)

            
            if (x, y) == (goal_x, goal_y):
                self.pf = True
                self.steps_taken = steps

            self.path.append((x, y)) if (x, y) not in self.path else None

            if not self.pf:
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    self.get_logger().info(f"Exploring {nx}, {ny} \n steps: {steps + 1}")
                    if (0 <= nx < len(obstacle_grid[0]) and 0 <= ny < len(obstacle_grid) and (nx, ny) not in self.path and obstacle_grid[ny][nx] == 0):  # Not an obstacle
                        queue.append((nx, ny, steps + 1))

        if not queue and self.pf == True:
            self.current_position = (goal_x, goal_y)
          

def main(args=None):
    if param==2:
        parser = argparse.ArgumentParser()
        parser.add_argument("-x", type=int, help="Starting x-coordinate")
        parser.add_argument("-y", type=int, help="Starting y-coordinate")
        parser.add_argument("-X", type=int, help="Goal x-coordinate")
        parser.add_argument("-Y", type=int, help="Goal y-coordinate")
    rclpy.init(args=args)
    node = ObstacleNavigation()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

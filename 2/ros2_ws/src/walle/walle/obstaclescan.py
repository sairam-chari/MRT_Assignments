import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
import argparse

class ObstacleAvoidance(Node):
    def __init__(self, grid):
        super().__init__("obstacle_avoidance")
        self.grid = grid
        self.publisher_ = self.create_publisher(Float32MultiArray, "/obstacle_coordinates", 10)
        self.timer = self.create_timer(1.0, self.publish_obstacles)



    def publish_obstacles(self):
        msg = Float32MultiArray()
        x, y = len(self.grid[0]), len(self.grid)
        msg.data.extend([x, y])  # Publish dimensions as x, y
        for row in self.grid:
            msg.data.extend(row)  # Flatten the grid into a single list
        self.publisher_.publish(msg)
        self.get_logger().info(f"Published obstacle grid dimensions {x}x{y}")
        self.get_logger().info(f"\n".join([str(i) for i in self.grid]))
        #for i in self.grid:
        #    self.get_logger().info(f"{i}")

def parse_args():
    global grid,x,y
    parser = argparse.ArgumentParser()
    parser.add_argument("x", type=int, help="Number of columns in the grid")
    parser.add_argument("y", type=int, help="Number of rows in the grid")
    parser.add_argument("grid_string", type=str, help="Binary string representing the grid")
    args = parser.parse_args()
    x,y,grid_string =  int(args.x), int(args.y), str(args.grid_string)
    grid = [] 
    for i in range(y):
        row = [int(grid_string[j]) for j in range(i * x, (i + 1) * x)]
        grid.append(row)
    

def main(args=None):
    rclpy.init(args=args)
    parse_args()
    node = ObstacleAvoidance(grid)
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
import time

class ObstacleNavigation(Node):
    def __init__(self):
        super().__init__('obstacle_navigation')
        self.create_subscription(Float32MultiArray, '/obstaclecoordinates', self.obstacle_nav, 10)

    def obstacle_nav(self, msg):
        array = msg.data
        self.get_logger().info(f'Received obstacle coordinates: {array}')
        x = int(array[1])
        y = int(array[0])
        del array[0:2]  # Remove first two elements
        array2 = []
        for i in range(y):
            for j in range(x):
                if array[i * x + j] == 1:
                    array2.append([j, i])
        self.get_logger().info(f'Matrix dimensions: {x}x{y}')
        self.get_logger().info(f'Obstacle coordinates: {array2}') #first element is origin

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleNavigation()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('Shutting down')
        try:
            rclpy.shutdown()
        except Exception as e:
            print(f'Error during shutdown: {e}')

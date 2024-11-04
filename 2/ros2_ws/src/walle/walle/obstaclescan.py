import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
import time
class ObstacleScan(Node):
    def __init__(self):
        super().__init__("obstacle_scan")
        self.obstacle_matrix = [[1,1],[0,1],[1,0],[0,0]]
        self.publisher_ = self.create_publisher(Float32MultiArray, "/obstaclecoordinates", 10)
        self.timer = self.create_timer(1.0, self.publish_obstacle_coordinates)
        #self.publish_obstacle_coordinates()
    def publish_obstacle_coordinates(self):
        msg = Float32MultiArray()
        msg.data.extend([len(self.obstacle_matrix), len(self.obstacle_matrix[0])])
        for coordinates in self.obstacle_matrix:
            for i in coordinates:
                msg.data.append(i)
        self.publisher_.publish(msg)
        self.get_logger().info(f"Publishing: {msg.data}")


            

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleScan()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print("Shutting down")
        try:
            rclpy.shutdown()
        except:
            pass

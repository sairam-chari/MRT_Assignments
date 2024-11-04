import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray

class ObstacleScan(Node):
    def __init__(self):
        self.obstacle_matrix = [[0, 0], [1, 1], [2, 2], [3, 3]]
        super().__init__("obstacle_scan")
        self.publisher =self.create_publisher(Float32MultiArray, "/obstaclecoordinates", 10)
        self.publish_obstacle_matrix()

    def publish_obstacle_coordinates(self):
        msg = Float32MultiArray()
        msg.data.extend([len(self.obstacle_matrix)[0], len(self.obstacle_matrix)])
        for coordinates in self.obstacle_coordinates:
            for i in coordinates:
                msg.data.append(i)
        self.publisher.publish(msg)
        self.get_logger().info(f"Publishing: {msg.data}")

        def main(args=None):
            global node
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
                node.destroy_node()
                try:
                    rclpy.shutdown()
                except:
                    pass
            


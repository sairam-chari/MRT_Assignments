import rclpy
from rclpy.node import Node
from example_interfaces.srv import SetBool
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import String

class CollectionService(Node):
    def __init__(self):
        super().__init__('collection_service')

        # Service to handle collection requests (now uses SetBool)
        self.srv = self.create_service(SetBool, 'soil_collection', self.handle_request)

        # Publisher to send navigation commands
        self.nav_pub = self.create_publisher(Float32MultiArray, '/target_coordinates', 10)

        # Subscriber to listen for navigation status
        self.create_subscription(Float32MultiArray, "/obstacle_coordinates", self.obstacle_callback, 10)
        self.status_sub = self.create_subscription(String, '/navigation/status', self.status_callback, 10)

        self.current_request = None  # Track the current request being processed
        self.status = None           # Track the latest navigation status

        self.get_logger().info("Soil Collection Service is ready.")

    def handle_request(self, request, response):

        target_x, target_y = tuple(request.data)  

        self.get_logger().info(f"Received collection request: ({target_x}, {target_y})")

        # Send coordinates to navigation node
        self.nav_pub.publish(Float32MultiArray(data=[target_x, target_y]))  # Publish to navigation
        self.current_request = (target_x, target_y)
        
        # Response success or failure based on some internal logic (e.g., obstacle detection, navigation status)
        response.success = True
        response.message = f"Navigation to ({target_x}, {target_y}) started."
        return response

    def status_callback(self, msg):
        self.status = msg.data
        self.get_logger().info(f"Navigation status: {self.status}")

        if self.current_request:
            if self.status.startswith("Goal Reached"):
                self.log_collection_success(self.current_request)
            elif self.status.startswith("Path not possible"):
                self.log_collection_failure(self.current_request)
                self.return_to_base()
            self.current_request = None

    def obstacle_callback(self, msg):
        array = msg.data
        x = int(array[0])
        y = int(array[1])
        grid = array[2:]  

        obstacle_grid = [
            [grid[i * x + j] for j in range(x)] for i in range(y)
        ]
        self.get_logger().info(f"Received grid: {x}x{y}")

    def log_collection_success(self, target):
        self.get_logger().info(f"Collection successful at {target}.")
        self.publish_status("Collection Successful")

    def log_collection_failure(self, target):
        self.get_logger().error(f"Collection failed at {target}.")
        self.publish_status("Collection Failed")

    def return_to_base(self):
        self.get_logger().info("Returning to base due to obstacle.")
        point = [0, 0]  # Assume (0, 0) is the base
        self.nav_pub.publish(Float32MultiArray(data=point))

    def publish_status(self, status):
        # Publish collection status to /soil_collection/status
        status_pub = self.create_publisher(String, '/soil_collection/status', 10)
        status_pub.publish(String(data=status))


def main(args=None):
    rclpy.init(args=args)
    node = CollectionService()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()

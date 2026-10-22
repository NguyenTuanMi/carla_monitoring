#!/usr/bin/env python3

import rclpy
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String 
from rclpy.node import Node


class CarlaMonitorNode(Node):
    def __init__(self):
        super().__init__('carla_monitor_node')

        self.declare_parameter('warning_radius', 20.0)
        self.declare_parameter('target_x', 983.5)
        self.declare_parameter('target_y', 5442.8)  

        self.target_x = float(self.get_parameter('target_x').value)
        self.target_y = float(self.get_parameter('target_y').value)
        self.warning_radius = float(self.get_parameter('warning_radius').value)

        self.subscription = self.create_subscription(
            PoseStamped,
            '/carla/hero/odom',
            self.pose_callback,
            10,
        )

        self.status_publisher = self.create_publisher(
            String,
            '/carla/hero/status',
            10,
        )

    def pose_callback(self, msg):
        x = msg.pose.position.x
        y = msg.pose.position.y
        z = msg.pose.position.z

        if (x-self.target_x)**2 + (y-self.target_y)**2 < self.warning_radius**2:
            status_msg = String()
            status_msg.data = 'WARNING'
            self.status_publisher.publish(status_msg)
        else:  
            status_msg = String()
            status_msg.data = 'SAFE'
            self.status_publisher.publish(status_msg)


def main(args=None):
    rclpy.init(args=args)
    node = CarlaMonitorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
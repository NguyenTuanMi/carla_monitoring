#!/usr/bin/env python3

import math

import rclpy
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String 
from rclpy.node import Node


class CarlaMonitorNode(Node):
    def __init__(self):
        super().__init__('carla_monitor_node')

        self.declare_parameter('warning_radius', [20.0])
        self.declare_parameter('target_x', [983.5])
        self.declare_parameter('target_y', [5442.8])  

        self.target_x = self.get_parameter('target_x').value
        self.target_y = self.get_parameter('target_y').value
        self.warning_radius = self.get_parameter('warning_radius').value

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
        distances = [
            math.hypot(
                x - float(target_x),
                y - float(target_y),
            )
            for target_x, target_y in zip(self.target_x, self.target_y)
        ]
        warning_radius = [float(r) for r in self.warning_radius]
        if not distances:
            return

        nearest_index, nearest_distance = min(
            enumerate(distances),
            key=lambda item: item[1],
        )
        status_msg = String()
        status = 'WARNING' if nearest_distance < warning_radius[nearest_index] else 'SAFE'
        status_msg.data = status
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
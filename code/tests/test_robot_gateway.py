import unittest

from app.robot_gateway import ControlWatchdog, SafeRobotGateway


class RobotGatewayTests(unittest.TestCase):
    def test_gateway_authorizes_only_bounded_operations(self):
        gateway = SafeRobotGateway()
        self.assertEqual(gateway.gesture("friendly", 1.0).status, "AUTHORIZED")
        self.assertEqual(gateway.gesture("unknown", 1.0).status, "REJECTED")
        self.assertEqual(gateway.gesture("friendly", 31.0).status, "REJECTED")

    def test_protective_stop_blocks_future_operations(self):
        gateway = SafeRobotGateway()
        self.assertEqual(gateway.protective_stop().status, "STOPPED")
        self.assertEqual(gateway.speak("hello.wav").status, "STOPPED")

    def test_app_response_contract_is_executable(self):
        gateway = SafeRobotGateway()
        self.assertEqual(gateway.gesture("excited", 8.0).status, "AUTHORIZED")

    def test_watchdog_requires_periodic_heartbeat(self):
        watchdog = ControlWatchdog(timeout_seconds=0.25)
        baseline = watchdog._last_heartbeat
        self.assertFalse(watchdog.expired(baseline + 0.2))
        self.assertTrue(watchdog.expired(baseline + 0.3))
        watchdog.heartbeat()
        self.assertFalse(watchdog.expired(watchdog._last_heartbeat + 0.1))

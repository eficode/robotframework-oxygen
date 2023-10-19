import sys

from unittest import TestCase
from unittest.mock import ANY, Mock, create_autospec, patch

from robot.running.model import TestSuite

from oxygen.oxygen import OxygenCLI
from ..helpers import RESOURCES_PATH


class TestOxygenZapCLI(TestCase):
    ZAP_XML = str(RESOURCES_PATH / "zap" / "zap.xml")

    def setUp(self):
        self.cli = OxygenCLI()
        self.handler = self.cli.handlers["oxygen.zap"]
        self.expected_suite = create_autospec(TestSuite)
        self.mock = Mock()
        self.mock.running.build_suite = Mock(return_value=self.expected_suite)

    def tearDown(self):
        self.cli = None
        self.handler = None
        self.expected_suite = None
        self.mock = None

    def test_cli(self):
        self.assertEqual(
            self.handler.cli(),
            {
                ("--accepted-risk-level",): {
                    "help": "Set accepted risk level",
                    "type": int,
                },
                ("--required-confidence-level",): {
                    "help": "Set required confidence level",
                    "type": int,
                },
                ("result_file",): {},
            },
        )

    @patch("oxygen.oxygen.RobotInterface")
    def test_cli_run(self, mock_robot_iface):
        mock_robot_iface.return_value = self.mock

        cmd_args = f"oxygen oxygen.zap {self.ZAP_XML}"
        with patch.object(sys, "argv", cmd_args.split()):
            self.cli.run()

        self.assertEqual(self.handler._config["accepted_risk_level"], 2)
        self.assertEqual(self.handler._config["required_confidence_level"], 1)

        self.mock.running.build_suite.assert_called_once()

        self.expected_suite.run.assert_called_once_with(
            output=str(RESOURCES_PATH / "zap" / "zap_robot_output.xml"),
            log=None,
            report=None,
            stdout=ANY,
        )

    @patch("oxygen.oxygen.RobotInterface")
    def test_cli_run_with_levels(self, mock_robot_iface):
        mock_robot_iface.return_value = self.mock

        cmd_args = (
            f"oxygen oxygen.zap {self.ZAP_XML} --accepted-risk-level 3"
            " --required-confidence-level 3"
        )
        with patch.object(sys, "argv", cmd_args.split()):
            self.cli.run()

        self.assertEqual(self.handler._config["accepted_risk_level"], 3)
        self.assertEqual(self.handler._config["required_confidence_level"], 3)

    @patch("oxygen.oxygen.RobotInterface")
    def test_cli_run_with_accepted_risk_level(self, mock_robot_iface):
        mock_robot_iface.return_value = self.mock

        cmd_args = f"oxygen oxygen.zap {self.ZAP_XML} --accepted-risk-level 3"
        with patch.object(sys, "argv", cmd_args.split()):
            self.cli.run()

        self.assertEqual(self.handler._config["accepted_risk_level"], 3)
        self.assertEqual(self.handler._config["required_confidence_level"], 1)

    @patch("oxygen.oxygen.RobotInterface")
    def test_cli_run_with_required_confidence_level(self, mock_robot_iface):
        mock_robot_iface.return_value = self.mock

        cmd_args = f"oxygen oxygen.zap {self.ZAP_XML} --required-confidence-level 3"
        with patch.object(sys, "argv", cmd_args.split()):
            self.cli.run()

        self.assertEqual(self.handler._config["accepted_risk_level"], 2)
        self.assertEqual(self.handler._config["required_confidence_level"], 3)

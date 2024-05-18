# TODO: Separate creation from usage
# TODO: Avoid assumptions and generalize the code
# TODO: Add default values to your functions
# TODO: Protect your attributes from the user
# TODO: Handle exceptions and errors

from flexsea.device import Device
from time import sleep

from flexsea.utilities.constants import baudRate


class Motor(Device):
    """
    A class to represent a Motor.

    Args:
        port (str): The port to connect to the motor.
        firmware (str): The firmware version of the motor.
    """

    def __init__(
        self,
        port: str,
        firmware: str,
        frequency: float,
        gear_ratio: float,
        motor_torque_constant: float,
    ) -> None:
        super().__init__(firmwareVersion=firmware, port=port)
        self.frequency = frequency
        self.gear_ratio = gear_ratio
        self.motor_torque_constant = motor_torque_constant

    def start(self) -> None:
        """
        Starts the motor.
        """
        self.open()
        self.start_streaming(frequency=self.frequency)

    def update(self) -> None:
        """
        Updates the motor data.
        """
        return self.read()

    def command_motor_torque(self, value: float) -> None:
        """
        Commands the motor a torque value.

        Args:
            value (float): Torque value to command in Nm.
        """
        current = value / (self.gear_ratio * self.motor_torque_constant)
        self.command_motor_current(value=current)

    def stop(self) -> None:
        """
        Stops the motor.
        """
        self.stop_motor()


if __name__ == "__main__":
    pass

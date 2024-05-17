﻿# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #
# pylint: disable=W0201

from typing import List  # pylint: disable=unused-import
from ..protobufs import main_pb2


class MovementFailedExceptionData:
    """
    Contains additional data for MovementFailedException.
    """

    @property
    def warnings(self) -> List[str]:
        """
        The full list of warnings.
        """

        return self._warnings

    @warnings.setter
    def warnings(self, value: List[str]) -> None:
        self._warnings = value

    @property
    def reason(self) -> str:
        """
        The reason for the Exception.
        """

        return self._reason

    @reason.setter
    def reason(self, value: str) -> None:
        self._reason = value

    @property
    def device(self) -> int:
        """
        The address of the device that performed the failed movement.
        """

        return self._device

    @device.setter
    def device(self, value: int) -> None:
        self._device = value

    @property
    def axis(self) -> int:
        """
        The number of the axis that performed the failed movement.
        """

        return self._axis

    @axis.setter
    def axis(self, value: int) -> None:
        self._axis = value

    def __repr__(self) -> str:
        return str(self.__dict__)

    @staticmethod
    def from_protobuf(
        pb_data: main_pb2.MovementFailedExceptionData
    ) -> 'MovementFailedExceptionData':
        instance = MovementFailedExceptionData.__new__(
            MovementFailedExceptionData
        )  # type: MovementFailedExceptionData
        instance.warnings = list(pb_data.warnings)
        instance.reason = pb_data.reason
        instance.device = pb_data.device
        instance.axis = pb_data.axis
        return instance

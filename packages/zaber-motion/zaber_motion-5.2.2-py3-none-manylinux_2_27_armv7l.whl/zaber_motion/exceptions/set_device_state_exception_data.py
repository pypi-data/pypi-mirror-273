﻿# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #
# pylint: disable=W0201

from typing import List  # pylint: disable=unused-import
from ..protobufs import main_pb2
from .set_peripheral_state_exception_data import SetPeripheralStateExceptionData


class SetDeviceStateExceptionData:
    """
    Contains additional data for a SetDeviceStateFailedException.
    """

    @property
    def settings(self) -> List[str]:
        """
        A list of settings which could not be set.
        """

        return self._settings

    @settings.setter
    def settings(self, value: List[str]) -> None:
        self._settings = value

    @property
    def stream_buffers(self) -> List[str]:
        """
        The reason the stream buffers could not be set.
        """

        return self._stream_buffers

    @stream_buffers.setter
    def stream_buffers(self, value: List[str]) -> None:
        self._stream_buffers = value

    @property
    def pvt_buffers(self) -> List[str]:
        """
        The reason the pvt buffers could not be set.
        """

        return self._pvt_buffers

    @pvt_buffers.setter
    def pvt_buffers(self, value: List[str]) -> None:
        self._pvt_buffers = value

    @property
    def triggers(self) -> List[str]:
        """
        The reason the triggers could not be set.
        """

        return self._triggers

    @triggers.setter
    def triggers(self, value: List[str]) -> None:
        self._triggers = value

    @property
    def servo_tuning(self) -> str:
        """
        The reason servo tuning could not be set.
        """

        return self._servo_tuning

    @servo_tuning.setter
    def servo_tuning(self, value: str) -> None:
        self._servo_tuning = value

    @property
    def stored_positions(self) -> List[str]:
        """
        The reasons stored positions could not be set.
        """

        return self._stored_positions

    @stored_positions.setter
    def stored_positions(self, value: List[str]) -> None:
        self._stored_positions = value

    @property
    def storage(self) -> List[str]:
        """
        The reasons storage could not be set.
        """

        return self._storage

    @storage.setter
    def storage(self, value: List[str]) -> None:
        self._storage = value

    @property
    def peripherals(self) -> List[SetPeripheralStateExceptionData]:
        """
        Errors for any peripherals that could not be set.
        """

        return self._peripherals

    @peripherals.setter
    def peripherals(self, value: List[SetPeripheralStateExceptionData]) -> None:
        self._peripherals = value

    def __repr__(self) -> str:
        return str(self.__dict__)

    @staticmethod
    def from_protobuf(
        pb_data: main_pb2.SetDeviceStateExceptionData
    ) -> 'SetDeviceStateExceptionData':
        instance = SetDeviceStateExceptionData.__new__(
            SetDeviceStateExceptionData
        )  # type: SetDeviceStateExceptionData
        instance.settings = list(pb_data.settings)
        instance.stream_buffers = list(pb_data.stream_buffers)
        instance.pvt_buffers = list(pb_data.pvt_buffers)
        instance.triggers = list(pb_data.triggers)
        instance.servo_tuning = pb_data.servo_tuning
        instance.stored_positions = list(pb_data.stored_positions)
        instance.storage = list(pb_data.storage)
        instance.peripherals = [SetPeripheralStateExceptionData.from_protobuf(item) for item in pb_data.peripherals]
        return instance

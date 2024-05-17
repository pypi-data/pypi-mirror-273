﻿# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #

from typing import TYPE_CHECKING, List, Optional
from ..call import call, call_async, call_sync

from ..protobufs import main_pb2
from .device_settings import DeviceSettings
from .axis import Axis
from .all_axes import AllAxes
from .warnings import Warnings
from .device_identity import DeviceIdentity
from .device_io import DeviceIO
from .response import Response
from .lockstep import Lockstep
from .oscilloscope import Oscilloscope
from .storage import DeviceStorage
from .can_set_state_device_response import CanSetStateDeviceResponse
from .pvt import Pvt
from .triggers import Triggers
from .streams import Streams
from ..firmware_version import FirmwareVersion
from ..measurement import Measurement

if TYPE_CHECKING:
    from .connection import Connection


class Device:
    """
    Represents the controller part of one device - may be either a standalone controller or an integrated controller.
    """

    @property
    def connection(self) -> 'Connection':
        """
        Connection of this device.
        """
        return self._connection

    @property
    def device_address(self) -> int:
        """
        The device address uniquely identifies the device on the connection.
        It can be configured or automatically assigned by the renumber command.
        """
        return self._device_address

    @property
    def settings(self) -> DeviceSettings:
        """
        Settings and properties of this device.
        """
        return self._settings

    @property
    def storage(self) -> DeviceStorage:
        """
        Key-value storage of this device.
        """
        return self._storage

    @property
    def io(self) -> DeviceIO:
        """
        I/O channels of this device.
        """
        return self._io

    @property
    def all_axes(self) -> AllAxes:
        """
        Virtual axis which allows you to target all axes of this device.
        """
        return self._all_axes

    @property
    def warnings(self) -> Warnings:
        """
        Warnings and faults of this device and all its axes.
        """
        return self._warnings

    @property
    def identity(self) -> DeviceIdentity:
        """
        Identity of the device.
        """
        return self.__retrieve_identity()

    @property
    def is_identified(self) -> bool:
        """
        Indicates whether or not the device has been identified.
        """
        return self.__retrieve_is_identified()

    @property
    def oscilloscope(self) -> Oscilloscope:
        """
        Oscilloscope recording helper for this device.
        Requires at least Firmware 7.00.
        """
        return self._oscilloscope

    @property
    def device_id(self) -> int:
        """
        Unique ID of the device hardware.
        """
        return self.identity.device_id

    @property
    def serial_number(self) -> int:
        """
        Serial number of the device.
        """
        return self.identity.serial_number

    @property
    def name(self) -> str:
        """
        Name of the product.
        """
        return self.identity.name

    @property
    def axis_count(self) -> int:
        """
        Number of axes this device has.
        """
        return self.identity.axis_count

    @property
    def firmware_version(self) -> FirmwareVersion:
        """
        Version of the firmware.
        """
        return self.identity.firmware_version

    @property
    def is_integrated(self) -> bool:
        """
        The device is an integrated product.
        """
        return self.identity.is_integrated

    @property
    def label(self) -> str:
        """
        User-assigned label of the device.
        """
        return self.__retrieve_label()

    @property
    def triggers(self) -> Triggers:
        """
        Triggers for this device.
        Requires at least Firmware 7.06.
        """
        return self._triggers

    @property
    def streams(self) -> Streams:
        """
        Gets an object that provides access to Streams on this device.
        Requires at least Firmware 7.05.
        """
        return self._streams

    @property
    def pvt(self) -> Pvt:
        """
        Gets an object that provides access to PVT functions of this device.
        Note that as of ZML v5.0.0, this returns a Pvt object and NOT a PvtSequence object.
        The PvtSequence can now be obtained from the Pvt object.
        Requires at least Firmware 7.33.
        """
        return self._pvt

    def __init__(self, connection: 'Connection', device_address: int):
        self._connection = connection
        self._device_address = device_address
        self._settings = DeviceSettings(self)
        self._storage = DeviceStorage(self)
        self._io = DeviceIO(self)
        self._all_axes = AllAxes(self)
        self._warnings = Warnings(self, 0)
        self._oscilloscope = Oscilloscope(self)
        self._triggers = Triggers(self)
        self._streams = Streams(self)
        self._pvt = Pvt(self)

    def identify(
            self,
            assume_version: Optional[FirmwareVersion] = None
    ) -> DeviceIdentity:
        """
        Queries the device and the database, gathering information about the product.
        Without this information features such as unit conversions will not work.
        Usually, called automatically by detect devices method.

        Args:
            assume_version: The identification assumes the specified firmware version
                instead of the version queried from the device.
                Providing this argument can lead to unexpected compatibility issues.

        Returns:
            Device identification data.
        """
        request = main_pb2.DeviceIdentifyRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        request.assume_version.CopyFrom(FirmwareVersion.to_protobuf(assume_version))
        response = main_pb2.DeviceIdentity()
        call("device/identify", request, response)
        return DeviceIdentity.from_protobuf(response)

    async def identify_async(
            self,
            assume_version: Optional[FirmwareVersion] = None
    ) -> DeviceIdentity:
        """
        Queries the device and the database, gathering information about the product.
        Without this information features such as unit conversions will not work.
        Usually, called automatically by detect devices method.

        Args:
            assume_version: The identification assumes the specified firmware version
                instead of the version queried from the device.
                Providing this argument can lead to unexpected compatibility issues.

        Returns:
            Device identification data.
        """
        request = main_pb2.DeviceIdentifyRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        request.assume_version.CopyFrom(FirmwareVersion.to_protobuf(assume_version))
        response = main_pb2.DeviceIdentity()
        await call_async("device/identify", request, response)
        return DeviceIdentity.from_protobuf(response)

    def generic_command(
            self,
            command: str,
            axis: int = 0,
            check_errors: bool = True,
            timeout: int = 0
    ) -> Response:
        """
        Sends a generic ASCII command to this device.
        For more information refer to: [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_commands).

        Args:
            command: Command and its parameters.
            axis: Optional axis number to send the command to.
            check_errors: Controls whether to throw an exception when the device rejects the command.
            timeout: The timeout, in milliseconds, for a device to respond to the command.
                Overrides the connection default request timeout.

        Returns:
            A response to the command.
        """
        request = main_pb2.GenericCommandRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        request.command = command
        request.axis = axis
        request.check_errors = check_errors
        request.timeout = timeout
        response = main_pb2.GenericCommandResponse()
        call("interface/generic_command", request, response)
        return Response.from_protobuf(response)

    async def generic_command_async(
            self,
            command: str,
            axis: int = 0,
            check_errors: bool = True,
            timeout: int = 0
    ) -> Response:
        """
        Sends a generic ASCII command to this device.
        For more information refer to: [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_commands).

        Args:
            command: Command and its parameters.
            axis: Optional axis number to send the command to.
            check_errors: Controls whether to throw an exception when the device rejects the command.
            timeout: The timeout, in milliseconds, for a device to respond to the command.
                Overrides the connection default request timeout.

        Returns:
            A response to the command.
        """
        request = main_pb2.GenericCommandRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        request.command = command
        request.axis = axis
        request.check_errors = check_errors
        request.timeout = timeout
        response = main_pb2.GenericCommandResponse()
        await call_async("interface/generic_command", request, response)
        return Response.from_protobuf(response)

    def generic_command_multi_response(
            self,
            command: str,
            axis: int = 0,
            check_errors: bool = True,
            timeout: int = 0
    ) -> List[Response]:
        """
        Sends a generic ASCII command to this device and expect multiple responses.
        Responses are returned in order of arrival.
        For more information refer to: [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_commands).

        Args:
            command: Command and its parameters.
            axis: Optional axis number to send the command to.
            check_errors: Controls whether to throw an exception when a device rejects the command.
            timeout: The timeout, in milliseconds, for a device to respond to the command.
                Overrides the connection default request timeout.

        Returns:
            All responses to the command.
        """
        request = main_pb2.GenericCommandRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        request.command = command
        request.axis = axis
        request.check_errors = check_errors
        request.timeout = timeout
        response = main_pb2.GenericCommandResponseCollection()
        call("interface/generic_command_multi_response", request, response)
        return [Response.from_protobuf(a) for a in response.responses]

    async def generic_command_multi_response_async(
            self,
            command: str,
            axis: int = 0,
            check_errors: bool = True,
            timeout: int = 0
    ) -> List[Response]:
        """
        Sends a generic ASCII command to this device and expect multiple responses.
        Responses are returned in order of arrival.
        For more information refer to: [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_commands).

        Args:
            command: Command and its parameters.
            axis: Optional axis number to send the command to.
            check_errors: Controls whether to throw an exception when a device rejects the command.
            timeout: The timeout, in milliseconds, for a device to respond to the command.
                Overrides the connection default request timeout.

        Returns:
            All responses to the command.
        """
        request = main_pb2.GenericCommandRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        request.command = command
        request.axis = axis
        request.check_errors = check_errors
        request.timeout = timeout
        response = main_pb2.GenericCommandResponseCollection()
        await call_async("interface/generic_command_multi_response", request, response)
        return [Response.from_protobuf(a) for a in response.responses]

    def generic_command_no_response(
            self,
            command: str,
            axis: int = 0
    ) -> None:
        """
        Sends a generic ASCII command to this device without expecting a response and without adding a message ID
        For more information refer to: [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_commands).

        Args:
            command: Command and its parameters.
            axis: Optional axis number to send the command to.
                Specifying -1 omits the number completely.
        """
        request = main_pb2.GenericCommandRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        request.command = command
        request.axis = axis
        call("interface/generic_command_no_response", request)

    async def generic_command_no_response_async(
            self,
            command: str,
            axis: int = 0
    ) -> None:
        """
        Sends a generic ASCII command to this device without expecting a response and without adding a message ID
        For more information refer to: [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_commands).

        Args:
            command: Command and its parameters.
            axis: Optional axis number to send the command to.
                Specifying -1 omits the number completely.
        """
        request = main_pb2.GenericCommandRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        request.command = command
        request.axis = axis
        await call_async("interface/generic_command_no_response", request)

    def get_axis(
            self,
            axis_number: int
    ) -> Axis:
        """
        Gets an Axis class instance which allows you to control a particular axis on this device.
        Axes are numbered from 1.

        Args:
            axis_number: Number of axis intended to control.

        Returns:
            Axis instance.
        """
        if axis_number <= 0:
            raise ValueError('Invalid value; physical axes are numbered from 1.')

        return Axis(self, axis_number)

    def get_lockstep(
            self,
            lockstep_group_id: int
    ) -> Lockstep:
        """
        Gets a Lockstep class instance which allows you to control a particular lockstep group on the device.
        Requires at least Firmware 6.15 or 7.11.

        Args:
            lockstep_group_id: The ID of the lockstep group to control. Lockstep group IDs start at one.

        Returns:
            Lockstep instance.
        """
        if lockstep_group_id <= 0:
            raise ValueError('Invalid value; lockstep groups are numbered from 1.')

        return Lockstep(self, lockstep_group_id)

    def prepare_command(
            self,
            command_template: str,
            *parameters: Measurement
    ) -> str:
        """
        Formats parameters into a command and performs unit conversions.
        Parameters in the command template are denoted by a question mark.
        Command returned is only valid for this device.
        Unit conversion is not supported for commands where axes can be remapped, such as stream and PVT commands.
        For more information refer to: [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_commands).

        Args:
            command_template: Template of a command to prepare. Parameters are denoted by question marks.
            parameters: Variable number of command parameters.

        Returns:
            Command with converted parameters.
        """
        request = main_pb2.PrepareCommandRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        request.command_template = command_template
        request.parameters.extend([Measurement.to_protobuf(a) for a in parameters])
        response = main_pb2.StringResponse()
        call_sync("device/prepare_command", request, response)
        return response.value

    def set_label(
            self,
            label: str
    ) -> None:
        """
        Sets the user-assigned device label.
        The label is stored on the controller and recognized by other software.

        Args:
            label: Label to set.
        """
        request = main_pb2.DeviceSetStorageRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        request.value = label
        call("device/set_label", request)

    async def set_label_async(
            self,
            label: str
    ) -> None:
        """
        Sets the user-assigned device label.
        The label is stored on the controller and recognized by other software.

        Args:
            label: Label to set.
        """
        request = main_pb2.DeviceSetStorageRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        request.value = label
        await call_async("device/set_label", request)

    def __retrieve_label(
            self
    ) -> str:
        """
        Gets the device name.

        Returns:
            The label.
        """
        request = main_pb2.AxisEmptyRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        response = main_pb2.StringResponse()
        call_sync("device/get_label", request, response)
        return response.value

    def __repr__(
            self
    ) -> str:
        """
        Returns a string that represents the device.

        Returns:
            A string that represents the device.
        """
        request = main_pb2.AxisToStringRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        response = main_pb2.StringResponse()
        call_sync("device/device_to_string", request, response)
        return response.value

    def get_state(
            self
    ) -> str:
        """
        Returns a serialization of the current device state that can be saved and reapplied.

        Returns:
            A serialization of the current state of the device.
        """
        request = main_pb2.AxisEmptyRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        response = main_pb2.StringResponse()
        call("device/get_state", request, response)
        return response.value

    async def get_state_async(
            self
    ) -> str:
        """
        Returns a serialization of the current device state that can be saved and reapplied.

        Returns:
            A serialization of the current state of the device.
        """
        request = main_pb2.AxisEmptyRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        response = main_pb2.StringResponse()
        await call_async("device/get_state", request, response)
        return response.value

    def set_state(
            self,
            state: str,
            device_only: bool = False
    ) -> None:
        """
        Applies a saved state to this device.

        Args:
            state: The state object to apply to this device.
            device_only: If true, only device scope settings and features will be set.
        """
        request = main_pb2.SetStateRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        request.state = state
        request.device_only = device_only
        call("device/set_state", request)

    async def set_state_async(
            self,
            state: str,
            device_only: bool = False
    ) -> None:
        """
        Applies a saved state to this device.

        Args:
            state: The state object to apply to this device.
            device_only: If true, only device scope settings and features will be set.
        """
        request = main_pb2.SetStateRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        request.state = state
        request.device_only = device_only
        await call_async("device/set_state", request)

    def can_set_state(
            self,
            state: str
    ) -> CanSetStateDeviceResponse:
        """
        Checks if a state can be applied to this device.
        This only covers exceptions that can be determined statically such as mismatches of ID or version,
        the process of applying the state can still fail when running.

        Args:
            state: The state object to check against.

        Returns:
            An object listing errors that come up when trying to set the state.
        """
        request = main_pb2.CanSetStateRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        request.state = state
        response = main_pb2.CanSetStateDeviceResponse()
        call("device/can_set_state", request, response)
        return CanSetStateDeviceResponse.from_protobuf(response)

    async def can_set_state_async(
            self,
            state: str
    ) -> CanSetStateDeviceResponse:
        """
        Checks if a state can be applied to this device.
        This only covers exceptions that can be determined statically such as mismatches of ID or version,
        the process of applying the state can still fail when running.

        Args:
            state: The state object to check against.

        Returns:
            An object listing errors that come up when trying to set the state.
        """
        request = main_pb2.CanSetStateRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        request.state = state
        response = main_pb2.CanSetStateDeviceResponse()
        await call_async("device/can_set_state", request, response)
        return CanSetStateDeviceResponse.from_protobuf(response)

    def wait_to_respond(
            self,
            timeout: float
    ) -> None:
        """
        Waits for the device to start responding to messages.
        Useful to call after resetting the device.
        Throws RequestTimeoutException upon timeout.

        Args:
            timeout: For how long to wait in milliseconds for the device to start responding.
        """
        request = main_pb2.WaitToRespondRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        request.timeout = timeout
        call("device/wait_to_respond", request)

    async def wait_to_respond_async(
            self,
            timeout: float
    ) -> None:
        """
        Waits for the device to start responding to messages.
        Useful to call after resetting the device.
        Throws RequestTimeoutException upon timeout.

        Args:
            timeout: For how long to wait in milliseconds for the device to start responding.
        """
        request = main_pb2.WaitToRespondRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        request.timeout = timeout
        await call_async("device/wait_to_respond", request)

    def __retrieve_identity(
            self
    ) -> DeviceIdentity:
        """
        Returns identity.

        Returns:
            Device identity.
        """
        request = main_pb2.DeviceEmptyRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        response = main_pb2.DeviceIdentity()
        call_sync("device/get_identity", request, response)
        return DeviceIdentity.from_protobuf(response)

    def __retrieve_is_identified(
            self
    ) -> bool:
        """
        Returns whether or not the device have been identified.

        Returns:
            True if the device has already been identified. False otherwise.
        """
        request = main_pb2.DeviceEmptyRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        response = main_pb2.BoolResponse()
        call_sync("device/get_is_identified", request, response)
        return response.value

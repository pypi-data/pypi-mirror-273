﻿# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #

from typing import Generator, List, Any, Callable, Optional
import asyncio
from rx.subject import ReplaySubject
from rx.core import Observable
from rx import operators as rxop

from ..call import call, call_async, call_sync
from ..convert_exception import convert_exception
from ..events import events
from ..exceptions.motion_lib_exception import MotionLibException

from .device import Device
from .response import Response
from .transport import Transport
from .unknown_response_event import UnknownResponseEvent
from .alert_event import AlertEvent
from ..protobufs import main_pb2


class Connection:
    """
    Class representing access to particular connection (serial port, TCP connection).
    """

    @property
    def unknown_response(self) -> Observable:
        """
        Event invoked when a response from a device cannot be matched to any known request.
        """
        return self._unknown_response

    @property
    def alert(self) -> Observable:
        """
        Event invoked when an alert is received from a device.
        """
        return self._alert

    @property
    def disconnected(self) -> Observable:
        """
        Event invoked when connection is interrupted or closed.
        """
        return self._disconnected

    DEFAULT_BAUD_RATE = 115200
    """
    Default baud rate for serial connections.
    """

    TCP_PORT_CHAIN = 55550
    """
    Commands sent over this port are forwarded to the device chain.
    The bandwidth may be limited as the commands are forwarded over a serial connection.
    """

    NETWORK_SHARE_PORT = 11421
    """
    Local area network share port.
    """

    TCP_PORT_DEVICE_ONLY = 55551
    """
    Commands send over this port are processed only by the device
    and not forwarded to the rest of the chain.
    Using this port typically makes the communication faster.
    """

    @property
    def interface_id(self) -> int:
        """
        The interface ID identifies this Connection instance with the underlying library.
        """
        return self._interface_id

    @property
    def default_request_timeout(self) -> int:
        """
        The default timeout, in milliseconds, for a device to respond to a request.
        Setting the timeout to a too low value may cause request timeout exceptions.
        The initial value is 1000 (one second).
        """
        return self.__retrieve_timeout()

    @default_request_timeout.setter
    def default_request_timeout(self, value: int) -> None:
        """
        The default timeout, in milliseconds, for a device to respond to a request.
        Setting the timeout to a too low value may cause request timeout exceptions.
        The initial value is 1000 (one second).
        """
        self.__change_timeout(value)

    @property
    def checksum_enabled(self) -> bool:
        """
        Controls whether outgoing messages contain checksum.
        """
        return self.__retrieve_checksum_enabled()

    @checksum_enabled.setter
    def checksum_enabled(self, value: bool) -> None:
        """
        Controls whether outgoing messages contain checksum.
        """
        self.__change_checksum_enabled(value)

    def __init__(self, interface_id: int):
        self._interface_id = interface_id
        self.__setup_events()

    @staticmethod
    def open_serial_port(
            port_name: str,
            baud_rate: int = DEFAULT_BAUD_RATE,
            direct: bool = False
    ) -> 'Connection':
        """
        Opens a serial port, if Zaber Launcher controls the port, the port will be opened through Zaber Launcher.
        Zaber Launcher allows sharing of the port between multiple applications,
        If port sharing is not desirable, use the `direct` parameter.

        Args:
            port_name: Name of the port to open.
            baud_rate: Optional baud rate (defaults to 115200).
            direct: If true will connect to the serial port directly,
                failing if the connection is already opened by a message router instance.

        Returns:
            An object representing the port.
        """
        request = main_pb2.OpenInterfaceRequest()
        request.interface_type = main_pb2.SERIAL_PORT
        request.port_name = port_name
        request.baud_rate = baud_rate
        request.reject_routed_connection = direct
        response = main_pb2.OpenInterfaceResponse()
        call("interface/open", request, response)
        return Connection(response.interface_id)

    @staticmethod
    def open_serial_port_async(
            port_name: str,
            baud_rate: int = DEFAULT_BAUD_RATE,
            direct: bool = False
    ) -> 'AsyncConnectionOpener':
        """
        Opens a serial port, if Zaber Launcher controls the port, the port will be opened through Zaber Launcher.
        Zaber Launcher allows sharing of the port between multiple applications,
        If port sharing is not desirable, use the `direct` parameter.

        Args:
            port_name: Name of the port to open.
            baud_rate: Optional baud rate (defaults to 115200).
            direct: If true will connect to the serial port directly,
                failing if the connection is already opened by a message router instance.

        Returns:
            An object representing the port.
        """
        request = main_pb2.OpenInterfaceRequest()
        request.interface_type = main_pb2.SERIAL_PORT
        request.port_name = port_name
        request.baud_rate = baud_rate
        request.reject_routed_connection = direct
        return AsyncConnectionOpener(request)

    @staticmethod
    def open_tcp(
            host_name: str,
            port: int = TCP_PORT_CHAIN
    ) -> 'Connection':
        """
        Opens a TCP connection.

        Args:
            host_name: Hostname or IP address.
            port: Optional port number (defaults to 55550).

        Returns:
            An object representing the connection.
        """
        request = main_pb2.OpenInterfaceRequest()
        request.interface_type = main_pb2.TCP
        request.host_name = host_name
        request.port = port
        response = main_pb2.OpenInterfaceResponse()
        call("interface/open", request, response)
        return Connection(response.interface_id)

    @staticmethod
    def open_tcp_async(
            host_name: str,
            port: int = TCP_PORT_CHAIN
    ) -> 'AsyncConnectionOpener':
        """
        Opens a TCP connection.

        Args:
            host_name: Hostname or IP address.
            port: Optional port number (defaults to 55550).

        Returns:
            An object representing the connection.
        """
        request = main_pb2.OpenInterfaceRequest()
        request.interface_type = main_pb2.TCP
        request.host_name = host_name
        request.port = port
        return AsyncConnectionOpener(request)

    @staticmethod
    def open_custom(
            transport: Transport
    ) -> 'Connection':
        """
        Opens a connection using a custom transport.

        Args:
            transport: The custom connection transport.

        Returns:
            An object representing the connection.
        """
        request = main_pb2.OpenInterfaceRequest()
        request.interface_type = main_pb2.CUSTOM
        request.transport = transport.transport_id
        response = main_pb2.OpenInterfaceResponse()
        call("interface/open", request, response)
        return Connection(response.interface_id)

    @staticmethod
    def open_custom_async(
            transport: Transport
    ) -> 'AsyncConnectionOpener':
        """
        Opens a connection using a custom transport.

        Args:
            transport: The custom connection transport.

        Returns:
            An object representing the connection.
        """
        request = main_pb2.OpenInterfaceRequest()
        request.interface_type = main_pb2.CUSTOM
        request.transport = transport.transport_id
        return AsyncConnectionOpener(request)

    @staticmethod
    def open_iot(
            cloud_id: str,
            token: str = "unauthenticated",
            connection_name: str = "",
            realm: str = "",
            api: str = "https://api.zaber.io"
    ) -> 'Connection':
        """
        Opens a secured connection to a cloud connected device chain.
        Use this method to connect to devices on your account.

        Args:
            cloud_id: The cloud ID to connect to.
            token: The token to authenticate with. By default the connection will be unauthenticated.
            connection_name: The name of the connection to open.
                Can be left empty to default to the only connection present.
                Otherwise, use serial port name for serial port connection or hostname:port for TCP connection.
            realm: The realm to connect to.
                Can be left empty for the default account realm.
            api: The URL of the API to receive connection info from.

        Returns:
            An object representing the connection.
        """
        request = main_pb2.OpenInterfaceRequest()
        request.interface_type = main_pb2.IOT
        request.cloud_id = cloud_id
        request.token = token
        request.connection_name = connection_name
        request.realm = realm
        request.api = api
        response = main_pb2.OpenInterfaceResponse()
        call("interface/open", request, response)
        return Connection(response.interface_id)

    @staticmethod
    def open_iot_async(
            cloud_id: str,
            token: str = "unauthenticated",
            connection_name: str = "",
            realm: str = "",
            api: str = "https://api.zaber.io"
    ) -> 'AsyncConnectionOpener':
        """
        Opens a secured connection to a cloud connected device chain.
        Use this method to connect to devices on your account.

        Args:
            cloud_id: The cloud ID to connect to.
            token: The token to authenticate with. By default the connection will be unauthenticated.
            connection_name: The name of the connection to open.
                Can be left empty to default to the only connection present.
                Otherwise, use serial port name for serial port connection or hostname:port for TCP connection.
            realm: The realm to connect to.
                Can be left empty for the default account realm.
            api: The URL of the API to receive connection info from.

        Returns:
            An object representing the connection.
        """
        request = main_pb2.OpenInterfaceRequest()
        request.interface_type = main_pb2.IOT
        request.cloud_id = cloud_id
        request.token = token
        request.connection_name = connection_name
        request.realm = realm
        request.api = api
        return AsyncConnectionOpener(request)

    @staticmethod
    def open_network_share(
            host_name: str,
            port: int = NETWORK_SHARE_PORT,
            connection_name: str = ""
    ) -> 'Connection':
        """
        Opens a connection to Zaber Launcher in your Local Area Network.
        The connection is not secured.

        Args:
            host_name: Hostname or IP address.
            port: Port number.
            connection_name: The name of the connection to open.
                Can be left empty to default to the only connection present.
                Otherwise, use serial port name for serial port connection or hostname:port for TCP connection.

        Returns:
            An object representing the connection.
        """
        request = main_pb2.OpenInterfaceRequest()
        request.interface_type = main_pb2.NETWORK_SHARE
        request.host_name = host_name
        request.port = port
        request.connection_name = connection_name
        response = main_pb2.OpenInterfaceResponse()
        call("interface/open", request, response)
        return Connection(response.interface_id)

    @staticmethod
    def open_network_share_async(
            host_name: str,
            port: int = NETWORK_SHARE_PORT,
            connection_name: str = ""
    ) -> 'AsyncConnectionOpener':
        """
        Opens a connection to Zaber Launcher in your Local Area Network.
        The connection is not secured.

        Args:
            host_name: Hostname or IP address.
            port: Port number.
            connection_name: The name of the connection to open.
                Can be left empty to default to the only connection present.
                Otherwise, use serial port name for serial port connection or hostname:port for TCP connection.

        Returns:
            An object representing the connection.
        """
        request = main_pb2.OpenInterfaceRequest()
        request.interface_type = main_pb2.NETWORK_SHARE
        request.host_name = host_name
        request.port = port
        request.connection_name = connection_name
        return AsyncConnectionOpener(request)

    def generic_command(
            self,
            command: str,
            device: int = 0,
            axis: int = 0,
            check_errors: bool = True,
            timeout: int = 0
    ) -> Response:
        """
        Sends a generic ASCII command to this connection.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_commands).

        Args:
            command: Command and its parameters.
            device: Optional device address to send the command to.
            axis: Optional axis number to send the command to.
            check_errors: Controls whether to throw an exception when the device rejects the command.
            timeout: The timeout, in milliseconds, for a device to respond to the command.
                Overrides the connection default request timeout.

        Returns:
            A response to the command.
        """
        request = main_pb2.GenericCommandRequest()
        request.interface_id = self.interface_id
        request.command = command
        request.device = device
        request.axis = axis
        request.check_errors = check_errors
        request.timeout = timeout
        response = main_pb2.GenericCommandResponse()
        call("interface/generic_command", request, response)
        return Response.from_protobuf(response)

    async def generic_command_async(
            self,
            command: str,
            device: int = 0,
            axis: int = 0,
            check_errors: bool = True,
            timeout: int = 0
    ) -> Response:
        """
        Sends a generic ASCII command to this connection.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_commands).

        Args:
            command: Command and its parameters.
            device: Optional device address to send the command to.
            axis: Optional axis number to send the command to.
            check_errors: Controls whether to throw an exception when the device rejects the command.
            timeout: The timeout, in milliseconds, for a device to respond to the command.
                Overrides the connection default request timeout.

        Returns:
            A response to the command.
        """
        request = main_pb2.GenericCommandRequest()
        request.interface_id = self.interface_id
        request.command = command
        request.device = device
        request.axis = axis
        request.check_errors = check_errors
        request.timeout = timeout
        response = main_pb2.GenericCommandResponse()
        await call_async("interface/generic_command", request, response)
        return Response.from_protobuf(response)

    def generic_command_no_response(
            self,
            command: str,
            device: int = 0,
            axis: int = 0
    ) -> None:
        """
        Sends a generic ASCII command to this connection without expecting a response and without adding a message ID.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_commands).

        Args:
            command: Command and its parameters.
            device: Optional device address to send the command to.
                Specifying -1 omits the number completely.
            axis: Optional axis number to send the command to.
                Specifying -1 omits the number completely.
        """
        request = main_pb2.GenericCommandRequest()
        request.interface_id = self.interface_id
        request.command = command
        request.device = device
        request.axis = axis
        call("interface/generic_command_no_response", request)

    async def generic_command_no_response_async(
            self,
            command: str,
            device: int = 0,
            axis: int = 0
    ) -> None:
        """
        Sends a generic ASCII command to this connection without expecting a response and without adding a message ID.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_commands).

        Args:
            command: Command and its parameters.
            device: Optional device address to send the command to.
                Specifying -1 omits the number completely.
            axis: Optional axis number to send the command to.
                Specifying -1 omits the number completely.
        """
        request = main_pb2.GenericCommandRequest()
        request.interface_id = self.interface_id
        request.command = command
        request.device = device
        request.axis = axis
        await call_async("interface/generic_command_no_response", request)

    def generic_command_multi_response(
            self,
            command: str,
            device: int = 0,
            axis: int = 0,
            check_errors: bool = True,
            timeout: int = 0
    ) -> List[Response]:
        """
        Sends a generic ASCII command to this connection and expect multiple responses,
        either from one device or from many devices.
        Responses are returned in order of arrival.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_commands).

        Args:
            command: Command and its parameters.
            device: Optional device address to send the command to.
            axis: Optional axis number to send the command to.
            check_errors: Controls whether to throw an exception when a device rejects the command.
            timeout: The timeout, in milliseconds, for a device to respond to the command.
                Overrides the connection default request timeout.

        Returns:
            All responses to the command.
        """
        request = main_pb2.GenericCommandRequest()
        request.interface_id = self.interface_id
        request.command = command
        request.device = device
        request.axis = axis
        request.check_errors = check_errors
        request.timeout = timeout
        response = main_pb2.GenericCommandResponseCollection()
        call("interface/generic_command_multi_response", request, response)
        return [Response.from_protobuf(a) for a in response.responses]

    async def generic_command_multi_response_async(
            self,
            command: str,
            device: int = 0,
            axis: int = 0,
            check_errors: bool = True,
            timeout: int = 0
    ) -> List[Response]:
        """
        Sends a generic ASCII command to this connection and expect multiple responses,
        either from one device or from many devices.
        Responses are returned in order of arrival.
        For more information refer to the [ASCII Protocol Manual](https://www.zaber.com/protocol-manual#topic_commands).

        Args:
            command: Command and its parameters.
            device: Optional device address to send the command to.
            axis: Optional axis number to send the command to.
            check_errors: Controls whether to throw an exception when a device rejects the command.
            timeout: The timeout, in milliseconds, for a device to respond to the command.
                Overrides the connection default request timeout.

        Returns:
            All responses to the command.
        """
        request = main_pb2.GenericCommandRequest()
        request.interface_id = self.interface_id
        request.command = command
        request.device = device
        request.axis = axis
        request.check_errors = check_errors
        request.timeout = timeout
        response = main_pb2.GenericCommandResponseCollection()
        await call_async("interface/generic_command_multi_response", request, response)
        return [Response.from_protobuf(a) for a in response.responses]

    def enable_alerts(
            self
    ) -> None:
        """
        Enables alerts for all devices on the connection.
        This will change the "comm.alert" setting to 1 on all supported devices.
        """
        request = main_pb2.GenericCommandRequest()
        request.interface_id = self.interface_id
        request.command = "set comm.alert 1"
        call("interface/generic_command_no_response", request)

    async def enable_alerts_async(
            self
    ) -> None:
        """
        Enables alerts for all devices on the connection.
        This will change the "comm.alert" setting to 1 on all supported devices.
        """
        request = main_pb2.GenericCommandRequest()
        request.interface_id = self.interface_id
        request.command = "set comm.alert 1"
        await call_async("interface/generic_command_no_response", request)

    def disable_alerts(
            self
    ) -> None:
        """
        Disables alerts for all devices on the connection.
        This will change the "comm.alert" setting to 0 on all supported devices.
        """
        request = main_pb2.GenericCommandRequest()
        request.interface_id = self.interface_id
        request.command = "set comm.alert 0"
        call("interface/generic_command_no_response", request)

    async def disable_alerts_async(
            self
    ) -> None:
        """
        Disables alerts for all devices on the connection.
        This will change the "comm.alert" setting to 0 on all supported devices.
        """
        request = main_pb2.GenericCommandRequest()
        request.interface_id = self.interface_id
        request.command = "set comm.alert 0"
        await call_async("interface/generic_command_no_response", request)

    def reset_ids(
            self
    ) -> None:
        """
        Resets ASCII protocol message IDs. Only for testing purposes.
        """
        request = main_pb2.InterfaceEmptyRequest()
        request.interface_id = self.interface_id
        call_sync("interface/reset_ids", request)

    def close(
            self
    ) -> None:
        """
        Close the connection.
        """
        request = main_pb2.InterfaceEmptyRequest()
        request.interface_id = self.interface_id
        call("interface/close", request)

    async def close_async(
            self
    ) -> None:
        """
        Close the connection.
        """
        request = main_pb2.InterfaceEmptyRequest()
        request.interface_id = self.interface_id
        await call_async("interface/close", request)

    def get_device(
            self,
            device_address: int
    ) -> Device:
        """
        Gets a Device class instance which allows you to control a particular device on this connection.
        Devices are numbered from 1.

        Args:
            device_address: Address of device intended to control. Address is configured for each device.

        Returns:
            Device instance.
        """
        if device_address <= 0:
            raise ValueError('Invalid value; physical devices are numbered from 1.')

        return Device(self, device_address)

    def renumber_devices(
            self,
            first_address: int = 1
    ) -> int:
        """
        Renumbers devices present on this connection. After renumbering, devices need to be identified again.

        Args:
            first_address: This is the address that the device closest to the computer is given.
                Remaining devices are numbered consecutively.

        Returns:
            Total number of devices that responded to the renumber.
        """
        if first_address <= 0:
            raise ValueError('Invalid value; device addresses are numbered from 1.')

        request = main_pb2.DeviceRenumberRequest()
        request.interface_id = self.interface_id
        request.first_address = first_address
        response = main_pb2.IntResponse()
        call("device/renumber", request, response)
        return response.value

    async def renumber_devices_async(
            self,
            first_address: int = 1
    ) -> int:
        """
        Renumbers devices present on this connection. After renumbering, devices need to be identified again.

        Args:
            first_address: This is the address that the device closest to the computer is given.
                Remaining devices are numbered consecutively.

        Returns:
            Total number of devices that responded to the renumber.
        """
        if first_address <= 0:
            raise ValueError('Invalid value; device addresses are numbered from 1.')

        request = main_pb2.DeviceRenumberRequest()
        request.interface_id = self.interface_id
        request.first_address = first_address
        response = main_pb2.IntResponse()
        await call_async("device/renumber", request, response)
        return response.value

    def detect_devices(
            self,
            identify_devices: bool = True
    ) -> List[Device]:
        """
        Attempts to detect any devices present on this connection.

        Args:
            identify_devices: Determines whether device identification should be performed as well.

        Returns:
            Array of detected devices.
        """
        request = main_pb2.DeviceDetectRequest()
        request.interface_id = self.interface_id
        request.identify_devices = identify_devices
        response = main_pb2.DeviceDetectResponse()
        call("device/detect", request, response)
        return list(map(self.get_device, response.devices))

    async def detect_devices_async(
            self,
            identify_devices: bool = True
    ) -> List[Device]:
        """
        Attempts to detect any devices present on this connection.

        Args:
            identify_devices: Determines whether device identification should be performed as well.

        Returns:
            Array of detected devices.
        """
        request = main_pb2.DeviceDetectRequest()
        request.interface_id = self.interface_id
        request.identify_devices = identify_devices
        response = main_pb2.DeviceDetectResponse()
        await call_async("device/detect", request, response)
        return list(map(self.get_device, response.devices))

    def stop_all(
            self,
            wait_until_idle: bool = True
    ) -> List[int]:
        """
        Stops all of the devices on this connection.

        Args:
            wait_until_idle: Determines whether the function should return immediately
                or wait until the devices are stopped.

        Returns:
            The addresses of the devices that were stopped by this command.
        """
        request = main_pb2.DeviceOnAllRequest()
        request.interface_id = self.interface_id
        request.wait_until_idle = wait_until_idle
        response = main_pb2.DeviceOnAllResponse()
        call("device/stop_all", request, response)
        return list(response.device_addresses)

    async def stop_all_async(
            self,
            wait_until_idle: bool = True
    ) -> List[int]:
        """
        Stops all of the devices on this connection.

        Args:
            wait_until_idle: Determines whether the function should return immediately
                or wait until the devices are stopped.

        Returns:
            The addresses of the devices that were stopped by this command.
        """
        request = main_pb2.DeviceOnAllRequest()
        request.interface_id = self.interface_id
        request.wait_until_idle = wait_until_idle
        response = main_pb2.DeviceOnAllResponse()
        await call_async("device/stop_all", request, response)
        return list(response.device_addresses)

    def home_all(
            self,
            wait_until_idle: bool = True
    ) -> List[int]:
        """
        Homes all of the devices on this connection.

        Args:
            wait_until_idle: Determines whether the function should return immediately
                or wait until the devices are homed.

        Returns:
            The addresses of the devices that were homed by this command.
        """
        request = main_pb2.DeviceOnAllRequest()
        request.interface_id = self.interface_id
        request.wait_until_idle = wait_until_idle
        response = main_pb2.DeviceOnAllResponse()
        call("device/home_all", request, response)
        return list(response.device_addresses)

    async def home_all_async(
            self,
            wait_until_idle: bool = True
    ) -> List[int]:
        """
        Homes all of the devices on this connection.

        Args:
            wait_until_idle: Determines whether the function should return immediately
                or wait until the devices are homed.

        Returns:
            The addresses of the devices that were homed by this command.
        """
        request = main_pb2.DeviceOnAllRequest()
        request.interface_id = self.interface_id
        request.wait_until_idle = wait_until_idle
        response = main_pb2.DeviceOnAllResponse()
        await call_async("device/home_all", request, response)
        return list(response.device_addresses)

    def __repr__(
            self
    ) -> str:
        """
        Returns a string that represents the connection.

        Returns:
            A string that represents the connection.
        """
        request = main_pb2.InterfaceEmptyRequest()
        request.interface_id = self.interface_id
        response = main_pb2.StringResponse()
        call_sync("interface/to_string", request, response)
        return response.value

    def __retrieve_timeout(
            self
    ) -> int:
        """
        Returns default request timeout.

        Returns:
            Default request timeout.
        """
        request = main_pb2.InterfaceEmptyRequest()
        request.interface_id = self.interface_id
        response = main_pb2.IntResponse()
        call_sync("interface/get_timeout", request, response)
        return response.value

    def __change_timeout(
            self,
            timeout: int
    ) -> None:
        """
        Sets default request timeout.

        Args:
            timeout: Default request timeout.
        """
        request = main_pb2.SetInterfaceTimeoutRequest()
        request.interface_id = self.interface_id
        request.timeout = timeout
        call_sync("interface/set_timeout", request)

    def __retrieve_checksum_enabled(
            self
    ) -> bool:
        """
        Returns checksum enabled.

        Returns:
            Checksum enabled.
        """
        request = main_pb2.InterfaceEmptyRequest()
        request.interface_id = self.interface_id
        response = main_pb2.BoolResponse()
        call_sync("interface/get_checksum_enabled", request, response)
        return response.value

    def __change_checksum_enabled(
            self,
            is_enabled: bool
    ) -> None:
        """
        Sets checksum enabled.

        Args:
            is_enabled: Checksum enabled.
        """
        request = main_pb2.SetInterfaceChecksumEnabledRequest()
        request.interface_id = self.interface_id
        request.is_enabled = is_enabled
        call_sync("interface/set_checksum_enabled", request)

    def __enter__(self) -> 'Connection':
        """ __enter__ """
        return self

    def __exit__(self, _type: Any, _value: Any, _traceback: Any) -> None:
        """ __exit__ """
        self.close()

    def __filter_event(self, event_name: str) -> Callable[[Any], bool]:
        def filter_event(event: Any) -> bool:
            return event[0] == event_name and event[1].interface_id == self._interface_id  # type: ignore
        return filter_event

    def __setup_events(self) -> None:
        self._disconnected = ReplaySubject()  # terminates all the events

        self._unknown_response = events.pipe(
            rxop.take_until(self.disconnected),
            rxop.filter(self.__filter_event('interface/unknown_response')),
            rxop.map(lambda ev: UnknownResponseEvent.from_protobuf(ev[1]))
        )

        self._alert = events.pipe(
            rxop.take_until(self.disconnected),
            rxop.filter(self.__filter_event('interface/alert')),
            rxop.map(lambda ev: AlertEvent.from_protobuf(ev[1]))
        )

        events.pipe(
            rxop.filter(self.__filter_event('interface/disconnected')),
            rxop.take(1),
            rxop.map(lambda ev: convert_exception(ev[1].error_type, ev[1].error_message))
        ).subscribe(self._disconnected)


class AsyncConnectionOpener:
    '''Provides a connection in an asynchronous context using `await` or `async with`'''
    def __init__(self, request: main_pb2.OpenInterfaceRequest) -> None:
        self._request = request
        self._resource: Optional[Connection] = None

    async def _create_resource(self) -> Connection:
        response = main_pb2.OpenInterfaceResponse()
        task = asyncio.ensure_future(call_async("interface/open", self._request, response))

        try:
            await asyncio.shield(task)
        except asyncio.CancelledError:
            async def cancel() -> None:
                try:
                    await task
                    await Connection(response.interface_id).close_async()
                except MotionLibException:
                    pass

            asyncio.ensure_future(cancel())
            raise

        return Connection(response.interface_id)

    def __await__(self) -> Generator[Any, None, 'Connection']:
        return self._create_resource().__await__()

    async def __aenter__(self) -> 'Connection':
        self._resource = await self._create_resource()
        return self._resource

    async def __aexit__(self, exc_type: Any, exc: Any, trace: Any) -> None:
        if self._resource is not None:
            await self._resource.close_async()

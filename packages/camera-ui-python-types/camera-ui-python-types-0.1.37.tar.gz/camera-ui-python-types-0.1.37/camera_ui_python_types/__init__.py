from abc import ABC, abstractmethod
from typing_extensions import (
    NotRequired,
    Literal,
    Protocol,
    runtime_checkable,
    TypedDict,
)
from typing import (
    List,
    Optional,
    Union,
    Any,
    overload,
    AsyncGenerator,
    Tuple,
    Dict,
    Callable,
    TypeVar,
    Coroutine,
    Awaitable,
)

from rx.core.typing import Observable
from PIL import Image
import numpy as np


Callback = Union[
    Callable[..., Any],
    Callable[..., Coroutine[Any, Any, Any]],
]


# schema
JsonSchemaType = Literal["string", "number", "boolean", "object", "array"]


class JsonBaseSchema(TypedDict, total=False):
    key: str
    title: str
    description: str
    required: bool
    readonly: bool
    placeholder: str
    hidden: bool
    group: str
    defaultValue: Union[str, int, bool]


class PluginJsonBaseSchema(JsonBaseSchema, total=False):
    store: bool
    onSet: NotRequired[Callable[[Any, Any], Awaitable[Union[None, Any]]]]
    onGet: NotRequired[Callable[[], Awaitable[Union[Any, None]]]]


class PluginJsonSchemaString(PluginJsonBaseSchema):
    type: Literal["string"]
    format: NotRequired[str]
    minLength: NotRequired[int]
    maxLength: NotRequired[int]


class PluginJsonSchemaNumber(PluginJsonBaseSchema):
    type: Literal["number"]
    minimum: NotRequired[int]
    maximum: NotRequired[int]


class PluginJsonSchemaBoolean(PluginJsonBaseSchema):
    type: Literal["boolean"]


class PluginJsonSchemaEnum(PluginJsonBaseSchema):
    type: Literal["string"]
    enum: List[str]
    multiple: NotRequired[bool]


class PluginJsonSchemaObject(PluginJsonBaseSchema):
    type: Literal["object"]
    opened: NotRequired[bool]
    properties: NotRequired["PluginJsonSchemaForm"]


PluginJsonSchema = Union[
    PluginJsonSchemaString,
    PluginJsonSchemaNumber,
    PluginJsonSchemaBoolean,
    PluginJsonSchemaEnum,
    PluginJsonSchemaObject,
]


PluginJsonSchemaForm = Dict[str, PluginJsonSchema]


class PluginRootSchema(TypedDict):
    schema: PluginJsonSchemaForm


class JsonSchemaString(JsonBaseSchema):
    type: Literal["string"]
    format: NotRequired[str]
    minLength: NotRequired[int]
    maxLength: NotRequired[int]


class JsonSchemaNumber(JsonBaseSchema):
    type: Literal["number"]
    minimum: NotRequired[int]
    maximum: NotRequired[int]


class JsonSchemaBoolean(JsonBaseSchema):
    type: Literal["boolean"]


class JsonSchemaEnum(JsonBaseSchema):
    type: Literal["string"]
    enum: List[str]
    multiple: NotRequired[bool]


class JsonSchemaObject(JsonBaseSchema):
    type: Literal["object"]
    opened: NotRequired[bool]
    properties: NotRequired["JsonSchemaForm"]


class JsonSchemaButton(TypedDict):
    label: str
    onSubmit: str


class JsonSchemaObjectWithButtons(JsonSchemaObject):
    buttons: NotRequired[Tuple[JsonSchemaButton, NotRequired[JsonSchemaButton]]]


class JsonSchemaAnyOf(TypedDict):
    anyOf: List["JsonSchema"]


class JsonSchemaArray(JsonBaseSchema):
    type: Literal["array"]
    opened: NotRequired[bool]
    items: NotRequired[Union["JsonSchema", JsonSchemaAnyOf]]


JsonSchema = Union[
    JsonSchemaString,
    JsonSchemaNumber,
    JsonSchemaBoolean,
    JsonSchemaEnum,
    JsonSchemaObject,
    JsonSchemaObjectWithButtons,
    JsonSchemaArray,
]


JsonSchemaForm = Dict[str, JsonSchema]


class RootSchema(TypedDict):
    schema: JsonSchemaForm


class SchemaConfig(TypedDict):
    rootSchema: PluginRootSchema
    config: Dict[str, Union[str, int, bool]]


# camera object
class Go2RtcFFMPEGSource(TypedDict):
    aac: str
    opus: str


class Go2RtcWSSource(TypedDict):
    webrtc: str


class Go2RtcRTSPSource(TypedDict):
    single: str
    default: str
    mp4: str


class Go2RtcEndpoint(TypedDict):
    webrtc: str
    mse: str
    lmp4: str
    mmp4: str
    mp4: str
    mp4Snapshot: str
    jpegSnapshot: str
    lHlsTs: str
    lHlsFmp4: str
    mHlsFmp4: str
    mjpeg: str
    mjpegHtml: str


class StreamUrls(TypedDict):
    ws: Go2RtcWSSource
    rtsp: Go2RtcRTSPSource
    transcoded: Go2RtcFFMPEGSource
    www: Go2RtcEndpoint


class CameraInput(TypedDict):
    _id: str
    name: str
    roles: List["CameraRoles"]
    urls: StreamUrls


CameraRoles = Literal["detect", "record", "stream", "snapshot", "none"]

CameraExtension = Literal[
    "hub",
    "prebuffer",
    "motionDetection",
    "objectDetection",
    "audioDetection",
    "ptz",
    "intercom",
]


class CameraZone(TypedDict):
    name: str
    regions: List["ZoneRegion"]


class ZoneRegion(TypedDict):
    _id: str
    coords: List["ZoneCoord"]


class ZoneCoord(TypedDict):
    _id: str
    points: Tuple[int, int]


class CameraInformation(TypedDict):
    model: str
    manufacturer: str
    hardware: str
    serialNumber: str
    firmwareVersion: str
    supportUrl: str


CameraType = Literal["camera", "doorbell"]


class BaseCamera(TypedDict):
    _id: str
    nativeId: NotRequired[str]
    pluginId: str
    name: str
    disabled: bool
    isCloud: bool
    hasLight: bool
    hasSiren: bool
    hasBinarySensor: bool
    hasBattery: bool
    info: CameraInformation
    type: CameraType
    motionZones: List[CameraZone]
    objectZones: List[CameraZone]


class Camera(BaseCamera):
    hasAudioDetector: bool
    hasMotionDetector: bool
    hasObjectDetector: bool
    hasPrebuffer: bool
    hasIntercom: bool
    hasPtz: bool
    sources: List[CameraInput]


# camera device
class BaseState(TypedDict):
    timestamp: int
    lastTriggered: int


class Detection(TypedDict):
    id: NotRequired[str]
    label: NotRequired[str]
    boundingBox: Tuple[int, int, int, int]


class MotionSetEvent(TypedDict):
    state: bool
    detections: List[Detection]


class AudioSetEvent(TypedDict):
    state: bool


class ObjectSetEvent(TypedDict):
    state: bool
    detections: List[Detection]


class LightSetEvent(TypedDict):
    state: bool


class DoorbellSetEvent(TypedDict):
    state: bool


class SirenSetEvent(TypedDict):
    state: bool


class BatterySetEvent(TypedDict):
    state: int


class DeviceSetEvent(TypedDict):
    pass


class LightState(BaseState, LightSetEvent):
    pass


class MotionState(BaseState, MotionSetEvent):
    pass


class AudioState(BaseState, AudioSetEvent):
    pass


class DoorbellState(BaseState, DoorbellSetEvent):
    pass


class SirenState(BaseState, SirenSetEvent):
    pass


class ObjectState(BaseState, ObjectSetEvent):
    pass


class BatteryState(BaseState, BatterySetEvent):
    pass


State = Union[
    LightState,
    MotionState,
    AudioState,
    DoorbellState,
    SirenState,
    ObjectState,
    BatteryState,
]

T = TypeVar(
    "T",
    LightState,
    MotionState,
    AudioState,
    DoorbellState,
    SirenState,
    ObjectState,
    BatteryState,
)


class StateValues(Protocol):
    light: LightState
    motion: MotionState
    audio: AudioState
    object: ObjectState
    doorbell: DoorbellState
    siren: SirenState
    battery: BatteryState


CameraStateCallbacks = Dict[str, Callable[[T], None]]

StateValue = Union[
    LightState,
    MotionState,
    AudioState,
    DoorbellState,
    SirenState,
    ObjectState,
    BatteryState,
]

OnSetEvent = Union[
    LightSetEvent,
    MotionSetEvent,
    AudioSetEvent,
    DoorbellSetEvent,
    SirenSetEvent,
    BatterySetEvent,
    ObjectSetEvent,
]

StateNames = Literal[
    "light", "motion", "audio", "doorbell", "siren", "battery", "object"
]

OnChangeCallback = Callable[[T, T], None]


class CameraDelegate(ABC):
    @abstractmethod
    async def snapshot_request(self, request_id: str) -> bytes:
        pass

    @abstractmethod
    async def prepare_stream(self, request_id: str) -> None:
        pass

    @abstractmethod
    async def on_offer(self, request_id: str, sdp: str) -> str:
        pass

    @abstractmethod
    async def on_candidates(self, request_id: str, candidates: str) -> None:
        pass

    @abstractmethod
    async def reboot(self) -> None:
        pass


class CameraPrebufferDelegate(ABC):
    @abstractmethod
    async def is_prebuffering(self, source_name: str, type: str) -> bool:
        pass

    @abstractmethod
    async def get_prebuffer_raw_url(self, source_name: str, type: str) -> Optional[str]:
        pass

    @abstractmethod
    async def get_stream_info(self, source_name: str) -> Optional[Dict[str, Any]]:
        pass


class CameraSource(Protocol):
    # CameraInput
    _id: str
    name: str
    roles: List["CameraRoles"]
    urls: StreamUrls

    async def is_prebuffering(self, type: str) -> bool: ...
    async def get_prebuffer_raw_url(self, type: str) -> Optional[str]: ...
    async def get_stream_info(self) -> Optional[Dict[str, Any]]: ...


class ImageCrop(TypedDict):
    top: float
    left: float
    bottom: float
    right: float


class ImageResize(TypedDict, total=False):
    width: NotRequired[int]
    height: NotRequired[int]
    filter: str


class ImageOptions(TypedDict, total=False):
    format: str
    crop: ImageCrop
    resize: ImageResize
    rotate: int


class IceServer(TypedDict):
    urls: List[str]
    username: NotRequired[str]
    credential: NotRequired[str]


class FrameMetadata(TypedDict):
    format: str
    frameSize: int
    width: int
    height: int


class Frame(TypedDict):
    metadata: FrameMetadata
    data: bytes


class VideoFrame(Protocol):
    metadata: FrameMetadata
    image: Image.Image

    def input_width(self) -> int: ...
    def input_height(self) -> int: ...
    def input_format(self) -> str: ...
    def to_buffer(self, options: Optional[ImageOptions] = None) -> bytes: ...
    def to_numpy(
        self, options: Optional[ImageOptions] = None
    ) -> np.ndarray[Any, Any]: ...
    def to_image(self, options: Optional[ImageOptions] = None) -> Image.Image: ...


class CameraDevice(Protocol):
    id: str
    plugin_id: str
    native_id: Optional[str] = None
    state: bool
    disabled: bool
    name: str
    type: CameraType
    info: CameraInformation
    sources: List[CameraSource]
    motion_zones: List[CameraZone]
    object_zones: List[CameraZone]
    is_cloud: bool
    has_light: bool
    has_siren: bool
    has_binary_sensor: bool
    has_battery: bool
    has_motion_detector: bool
    has_audio_detector: bool
    has_object_detector: bool
    has_ptz: bool
    has_prebuffer: bool
    has_intercom: bool

    on_connected: Observable[bool]
    on_light_switched: Observable[LightState]
    on_motion_detected: Observable[MotionState]
    on_audio_detected: Observable[AudioState]
    on_object_detected: Observable[ObjectState]
    on_doorbell_pressed: Observable[DoorbellState]
    on_siren_detected: Observable[SirenState]
    on_battery_changed: Observable[BatteryState]

    stream_source: CameraSource
    snapshot_source: CameraSource
    recording_source: CameraSource
    detection_source: CameraSource
    delegate: Optional[CameraDelegate] = None
    prebuffer_delegate: Optional[CameraPrebufferDelegate] = None

    async def connect(self) -> None: ...
    async def disconnect(self) -> None: ...
    async def reboot(self) -> None: ...
    async def snapshot(self, force_new: Optional[bool] = None) -> bytes: ...
    async def generate_frames(self) -> AsyncGenerator[VideoFrame, None]: ...
    async def get_ffmpeg_path(self) -> str: ...
    async def get_ice_servers(self) -> List[IceServer]: ...
    # async def create_session(self, options: Any) -> Any: ... # todo
    # async def stream_video(self, source_name: str, options: Any) -> None: ...  # todo
    # async def record_to_file(
    #     self, source_name: str, output_path: str, duration: Optional[int] = 60  # todo
    # ) -> None: ...
    async def get_value(
        self, state_name: str
    ) -> Union[
        LightState,
        MotionState,
        AudioState,
        ObjectState,
        DoorbellState,
        SirenState,
        BatteryState,
    ]: ...

    @overload
    async def update_state(
        self,
        state_name: Literal["light"],
        event_data: LightSetEvent,
    ) -> None: ...

    @overload
    async def update_state(
        self,
        state_name: Literal["motion"],
        event_data: MotionSetEvent,
    ) -> None: ...

    @overload
    async def update_state(
        self,
        state_name: Literal["audio"],
        event_data: AudioSetEvent,
    ) -> None: ...

    @overload
    async def update_state(
        self,
        state_name: Literal["object"],
        event_data: ObjectSetEvent,
    ) -> None: ...

    @overload
    async def update_state(
        self,
        state_name: Literal["doorbell"],
        event_data: DoorbellSetEvent,
    ) -> None: ...

    @overload
    async def update_state(
        self,
        state_name: Literal["siren"],
        event_data: SirenSetEvent,
    ) -> None: ...

    @overload
    async def update_state(
        self,
        state_name: Literal["battery"],
        event_data: BatterySetEvent,
    ) -> None: ...
    async def update_state(self, state_name: str, event_data: Any) -> None: ...
    def on_state_change(self, state_name: StateNames) -> Observable[Any]: ...
    def on_property_change(self, property_name: str) -> Observable[Any]: ...
    def remove_all_listeners(self) -> None: ...


# camera create config
class BaseCameraConfig(TypedDict):
    name: str
    nativeId: NotRequired[str]
    isCloud: NotRequired[bool]
    hasLight: NotRequired[bool]
    hasSiren: NotRequired[bool]
    hasBinarySensor: NotRequired[bool]
    hasBattery: NotRequired[bool]
    disabled: NotRequired[bool]
    info: NotRequired[CameraInformation]


class CameraInputSettings(TypedDict):
    _id: str
    name: str
    roles: List[CameraRoles]
    urls: List[str]


class CameraConfigWithSources(BaseCameraConfig):
    sources: NotRequired[List[CameraInputSettings]]


class CameraConfigWithDelegate(BaseCameraConfig):
    delegate: NotRequired[CameraDelegate]


CameraConfig = Union[CameraConfigWithSources, CameraConfigWithDelegate]


# events and callbacks
CameraSelectedCallback = Union[
    Callable[[CameraDevice, CameraExtension], None],
    Callable[[CameraDevice, CameraExtension], Coroutine[None, None, None]],
]
CameraDeselectedCallback = Union[
    Callable[[str, CameraExtension], None],
    Callable[[str, CameraExtension], Coroutine[None, None, None]],
]
CameraAddedCallback = Union[
    Callable[[CameraDevice], None],
    Callable[[CameraDevice], Coroutine[None, None, None]],
]
CameraRemovedCallback = Union[
    Callable[[str], None], Callable[[str], Coroutine[None, None, None]]
]
CameraUpdatedCallback = Union[
    Callable[[str, CameraDevice], None],
    Callable[[str, CameraDevice], Coroutine[None, None, None]],
]


# abstract


# DeviceManager
DeviceManagerEventType = Literal[
    "cameraSelected",
    "cameraDeselected",
    "cameraUpdated",
]


@runtime_checkable
class DeviceManager(Protocol):
    async def get_camera_by_id(self, id: str) -> Optional[CameraDevice]: ...
    async def get_camera_by_name(self, name: str) -> Optional[CameraDevice]: ...
    async def create_camera(self, config: CameraConfig) -> CameraDevice: ...
    async def remove_camera_by_id(self, id: str) -> None: ...
    async def remove_camera_by_name(self, name: str) -> None: ...

    @overload
    def on(
        self, event: Literal["cameraSelected"], listener: CameraSelectedCallback
    ) -> "DeviceManager": ...
    @overload
    def on(
        self, event: Literal["cameraDeselected"], listener: CameraDeselectedCallback
    ) -> "DeviceManager": ...
    @overload
    def on(
        self, event: Literal["cameraUpdated"], listener: CameraUpdatedCallback
    ) -> "DeviceManager": ...

    @overload
    def once(
        self, event: Literal["cameraSelected"], listener: CameraSelectedCallback
    ) -> "DeviceManager": ...
    @overload
    def once(
        self, event: Literal["cameraDeselected"], listener: CameraDeselectedCallback
    ) -> "DeviceManager": ...
    @overload
    def once(
        self, event: Literal["cameraUpdated"], listener: CameraUpdatedCallback
    ) -> "DeviceManager": ...

    @overload
    def remove_listener(
        self, event: Literal["cameraSelected"], listener: CameraSelectedCallback
    ) -> "DeviceManager": ...
    @overload
    def remove_listener(
        self, event: Literal["cameraDeselected"], listener: CameraDeselectedCallback
    ) -> "DeviceManager": ...
    @overload
    def remove_listener(
        self, event: Literal["cameraUpdated"], listener: CameraUpdatedCallback
    ) -> "DeviceManager": ...

    def remove_all_listeners(
        self, event: Optional[DeviceManagerEventType] = None
    ) -> "DeviceManager": ...


# SystemManager
@runtime_checkable
class SystemManager(Protocol):
    def on(self, event: str, listener: Callback) -> "SystemManager": ...
    def once(self, event: str, listener: Callback) -> "SystemManager": ...
    def remove_listener(self, event: str, listener: Callback) -> "SystemManager": ...
    def remove_all_listeners(self, event: str) -> "SystemManager": ...


# PluginsManager
@runtime_checkable
class PluginsManager(Protocol):  # todo: add methods
    def on(self, event: str, listener: Callback) -> "PluginsManager": ...
    def once(self, event: str, listener: Callback) -> "PluginsManager": ...
    def remove_listener(self, event: str, listener: Callback) -> "PluginsManager": ...
    def remove_all_listeners(self, event: str) -> "PluginsManager": ...


# camera storage
P = TypeVar("P")


@runtime_checkable
class CameraStorage(Protocol):
    async def initialize_storage(self) -> None: ...
    @overload
    def get_value(self, path: str) -> Union[Awaitable[P], P, None]: ...
    @overload
    def get_value(self, path: str, default_value: P) -> Union[Awaitable[P], P]: ...
    def get_value(
        self, path: str, default_value: Optional[P] = None
    ) -> Union[Awaitable[P], P, None]: ...
    async def set_value(self, path: str, new_value: Any) -> None: ...
    def has_value(self, path: str) -> bool: ...
    async def getConfig(self) -> SchemaConfig: ...
    async def setConfig(self, new_config: Dict[str, Any]) -> None: ...
    @overload
    async def add_schema(self, schema_or_path: PluginJsonSchemaForm) -> None: ...
    @overload
    async def add_schema(
        self, schema_or_path: str, schema: PluginJsonSchema
    ) -> None: ...
    async def add_schema(
        self,
        schema_or_path: Union[PluginJsonSchemaForm, str],
        schema: Optional[PluginJsonSchema] = None,
    ) -> None: ...
    def remove_schema(self, path: str) -> None: ...
    async def change_schema(self, path: str, new_schema: Dict[str, Any]) -> None: ...
    def get_schema(self, path: str) -> Optional[PluginJsonSchema]: ...
    def has_schema(self, path: str) -> bool: ...


# StorageController
@runtime_checkable
class StorageController(Protocol):
    def create_camera_storage(
        self,
        instance: Any,
        camera_id: str,
        schema: Optional[PluginJsonSchemaForm] = None,
    ) -> CameraStorage: ...
    def get_camera_storage(self, camera_id: str) -> Optional[CameraStorage]: ...
    def remove_camera_storage(self, camera_id: str) -> None: ...


# config service
@runtime_checkable
class PluginConfigService(Protocol):
    def get(
        self,
        key: str,
        default: Optional[Any] = None,
        validate: Optional[Callable[[Any], bool]] = None,
        refresh: bool = False,
        write_if_not_valid: bool = False,
    ) -> Any: ...

    def has(self, key: str, refresh: bool = False) -> bool: ...
    def ensure_exists(
        self, key: str, default: Optional[Any] = None, write: bool = False
    ) -> None: ...
    def set(self, key: str, value: Any, write: bool = False) -> None: ...
    def insert(
        self, key: str, value: Any, index: Optional[int] = None, write: bool = False
    ) -> None: ...
    def push(self, key: str, *values: Any, write: bool = False) -> None: ...
    def delete(self, key: str, write: bool = False) -> None: ...
    def all(self, refresh: bool = False) -> Dict[str, Any]: ...
    def replace(self, new_config: Dict[str, Any], write: bool = False) -> None: ...
    def update_value(
        self,
        path: str,
        search_key: str,
        search_value: Any,
        target_key: str,
        new_value: Any,
        write: bool = False,
    ) -> None: ...
    def replace_or_add_item(
        self,
        path: str,
        search_key: str,
        search_value: Any,
        new_item: Any,
        write: bool = False,
    ) -> None: ...


# Plugin API
APIEventType = Literal["finishLaunching", "shutdown"]


@runtime_checkable
class PluginAPI(Protocol):
    storage_path: str
    config_file: str
    config_service: PluginConfigService
    storage_controller: StorageController
    device_manager: DeviceManager
    system_manager: SystemManager
    plugins_manager: PluginsManager

    def on(self, event: APIEventType, listener: Callback) -> "PluginAPI": ...
    def once(self, event: APIEventType, listener: Callback) -> "PluginAPI": ...
    def off(self, event: APIEventType, listener: Callback) -> "PluginAPI": ...
    def remove_listener(
        self, event: APIEventType, listener: Callback
    ) -> "PluginAPI": ...
    def remove_all_listeners(
        self, event: Optional[APIEventType] = None
    ) -> "PluginAPI": ...


# logger
@runtime_checkable
class PluginLogger(Protocol):
    def log(self, *args: Any) -> None: ...
    def error(self, *args: Any) -> None: ...
    def warn(self, *args: Any) -> None: ...
    def attention(self, *args: Any) -> None: ...
    def debug(self, *args: Any) -> None: ...
    def trace(self, *args: Any) -> None: ...


# plugin
PluginConfig = Dict[str, Any]
JSONValue = Union[str, int, float, bool, Dict[str, Any], List[Any]]


class BasePlugin(ABC):
    @abstractmethod
    def __init__(self, logger: PluginLogger, api_instance: PluginAPI) -> None: ...
    @abstractmethod
    async def onFormSubmit(
        self, action_id: str, payload: Any
    ) -> Dict[Literal["toastMessage"], str]: ...
    @abstractmethod
    async def configure_cameras(self, cameras: List[CameraDevice]) -> None: ...

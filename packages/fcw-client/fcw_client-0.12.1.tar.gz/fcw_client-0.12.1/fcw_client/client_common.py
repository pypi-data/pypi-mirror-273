from __future__ import annotations

import logging
import os
import statistics
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Union

import numpy as np
import yaml

from era_5g_client.client import NetAppClient
from era_5g_client.client_base import NetAppClientBase
from era_5g_client.dataclasses import MiddlewareInfo
from era_5g_interface.channels import CallbackInfoClient, ChannelType
from era_5g_interface.interface_helpers import HEARTBEAT_CLIENT_EVENT
from era_5g_interface.measuring import Measuring
from fcw_core_utils.geometry import Camera

logger = logging.getLogger(__name__)

image_storage: Dict[int, np.ndarray] = dict()

DEBUG_PRINT_WARNING = True  # Prints score.
DEBUG_PRINT_DELAY = True  # Prints the delay between capturing image and receiving the results.

# URL of the FCW service.
NETAPP_ADDRESS = str(os.getenv("NETAPP_ADDRESS", "http://localhost:5896"))
HEARTBEAT_ADDRESS = str(os.getenv("HEARTBEAT_ADDRESS", "http://localhost:5898"))


class ResultsReader:
    """Default class for processing FCW results."""

    def __init__(self, extended_measuring: bool = False) -> None:
        """Constructor.

        Args:
            extended_measuring (bool): Enable logging of measuring.
        """

        self.delays = []
        self.delays_recv = []
        self.delays_send = []
        self.delays_process = []
        self.timestamps = [
            [
                "start_timestamp_ns",
                "recv_timestamp_ns",
                "send_timestamp_ns",
                "end_timestamp_ns",
                "timestamp_before_process",
                "timestamp_after_process",
            ]
        ]

        measuring_items = {
            "key_timestamp": 0,
            "final_timestamp": 0,
            "worker_recv_timestamp": 0,
            "worker_before_process_timestamp": 0,
            "worker_after_process_timestamp": 0,
            "worker_send_timestamp": 0,
        }
        prefix = f"client-final"
        self.measuring = Measuring(measuring_items, enabled=extended_measuring, filename_prefix=prefix)

    def stats(self, send_frames_count: int) -> None:
        """Print timestamps stats and can write them to CSV file.

        Args:
            send_frames_count (int): Number of send frames.
        """

        logger.info(f"-----")
        if len(self.delays) < 1 or len(self.delays_recv) < 1 or len(self.delays_send) < 1:
            logger.warning(f"No results data received")
        else:
            logger.info(f"Send frames: {send_frames_count}, dropped frames: {send_frames_count - len(self.delays)}")
            logger.info(
                f"Delay median:                 {statistics.median(self.delays) * 1.0e-9:.3f}s "
                f"mean: {statistics.mean(self.delays) * 1.0e-9:.3f}s "
                f"min: {min(self.delays) * 1.0e-9:.3f}s "
                f"max: {max(self.delays) * 1.0e-9:.3f}s"
            )
            logger.info(
                f"Delay service recv median:    {statistics.median(self.delays_recv) * 1.0e-9:.3f}s "
                f"mean: {statistics.mean(self.delays_recv) * 1.0e-9:.3f}s "
                f"min: {min(self.delays_recv) * 1.0e-9:.3f}s "
                f"max: {max(self.delays_recv) * 1.0e-9:.3f}s"
            )
            logger.info(
                f"Delay service send median:    {statistics.median(self.delays_send) * 1.0e-9:.3f}s "
                f"mean: {statistics.mean(self.delays_send) * 1.0e-9:.3f}s "
                f"min: {min(self.delays_send) * 1.0e-9:.3f}s "
                f"max: {max(self.delays_send) * 1.0e-9:.3f}s"
            )
            logger.info(
                f"Delay service process median: {statistics.median(self.delays_process) * 1.0e-9:.3f}s "
                f"mean: {statistics.mean(self.delays_process) * 1.0e-9:.3f}s "
                f"min: {min(self.delays_process) * 1.0e-9:.3f}s "
                f"max: {max(self.delays_process) * 1.0e-9:.3f}s"
            )

    def get_results(self, results: Dict[str, Any]) -> None:
        """Callback which process the results from the FCW service.

        Args:
            results (Dict[str, Any]): The results in JSON format.
        """

        results_timestamp = time.perf_counter_ns()

        # Process dangerous detections.
        if "dangerous_detections" in results:
            if DEBUG_PRINT_WARNING:
                for tracked_id, detection in results["dangerous_detections"].items():
                    score = float(detection["dangerous_distance"])
                    if score > 0:
                        logger.info(f"Dangerous distance {score:.2f}m to the object with id {tracked_id}")
        if "objects" in results:
            logger.info(f"objects {results['objects']}")

        # Process timestamps.
        if "timestamp" in results:
            key_timestamp = results["timestamp"]
            recv_timestamp = results["recv_timestamp"]
            send_timestamp = results["send_timestamp"]
            timestamp_before_process = results["timestamp_before_process"]
            timestamp_after_process = results["timestamp_after_process"]

            # Log the final recv time of this node
            self.measuring.log_measuring(key_timestamp, "final_timestamp", results_timestamp)

            # Log other misc timestamps from the received message
            self.measuring.log_measuring(key_timestamp, "worker_recv_timestamp", recv_timestamp)
            self.measuring.log_measuring(
                key_timestamp,
                "worker_before_process_timestamp",
                timestamp_before_process,
            )
            self.measuring.log_measuring(
                key_timestamp,
                "worker_after_process_timestamp",
                timestamp_after_process,
            )
            self.measuring.log_measuring(key_timestamp, "worker_send_timestamp", send_timestamp)

            self.measuring.store_measuring(key_timestamp)

            if DEBUG_PRINT_DELAY:
                logger.info(
                    f"Result number {len(self.timestamps)}"
                    f", delay: {(results_timestamp - key_timestamp) * 1.0e-9:.3f}s"
                    # f", recv frame delay: {(recv_timestamp - key_timestamp) * 1.0e-9:.3f}s"
                )
                self.delays.append((results_timestamp - key_timestamp))
                self.delays_recv.append((recv_timestamp - key_timestamp))
                self.delays_send.append((send_timestamp - key_timestamp))
                self.delays_process.append((timestamp_after_process - timestamp_before_process))

            self.timestamps.append(
                [
                    key_timestamp,
                    recv_timestamp,
                    send_timestamp,
                    results_timestamp,
                    timestamp_before_process,
                    timestamp_after_process,
                ]
            )


class StreamType(Enum):
    """Class for stream types."""

    JPEG = 1
    H264 = 2
    HEVC = 3


@dataclass
class MiddlewareAllInfo:
    """MiddlewareInfo with task ID, robot ID and resource lock values."""

    middleware_info: MiddlewareInfo
    task_id: str
    robot_id: str
    resource_lock = False


class CollisionWarningClient:
    """Wrapper class for FCW client."""

    def __init__(
        self,
        config: Path,
        camera_config: Path,
        netapp_info: Union[str, MiddlewareAllInfo] = NETAPP_ADDRESS,
        fps: float = 30,
        viz: bool = True,
        viz_zmq_port: int = 5558,
        results_callback: Optional[Callable] = None,
        stream_type: Optional[StreamType] = StreamType.H264,
        stats: bool = False,
        extended_measuring: bool = False,
    ) -> None:
        """Constructor.

        Args:
            config (Path): Path to FCW configuration file.
            camera_config (Path): Path to camera configuration file.
            netapp_info (Union[str, MiddlewareAllInfo]): The URI and port of the FCW service interface (default taken
                from environment variables NETAPP_ADDRESS) or MiddlewareInfo with task ID, robot ID and resource lock
                values.
            fps (float): Video FPS. Default to 30.
            viz (bool): Whether to enable visualization. Default to True.
            viz_zmq_port (int): Port of the ZMQ server. Default to 5558.
            results_callback (Callable, optional): Callback for receiving results. Default to ResultsReader.get_results.
            stream_type (StreamType, optional): Stream type JPEG or H264 or HEVC. Default to H264.
            stats (bool): Store output data sizes.
            extended_measuring (bool): Enable logging of measuring.
        """

        logger.info("Loading configuration file {cfg}".format(cfg=config))
        self.config_dict = yaml.safe_load(config.open())
        logger.info("Loading camera configuration {cfg}".format(cfg=camera_config))
        self.camera_config_dict = yaml.safe_load(camera_config.open())
        logger.info("Initializing camera calibration")
        self.camera = Camera.from_dict(self.camera_config_dict)

        self.fps = fps
        # Check bad loaded FPS.
        if self.fps > 60:
            logger.warning(f"FPS {self.fps} is strangely high, newly set to 30")
            self.fps = 30
        self.results_callback = results_callback
        if self.results_callback is None:
            self.results_viewer = ResultsReader(extended_measuring=extended_measuring)
            self.results_callback = self.results_viewer.get_results
        self.stream_type = stream_type
        self.frame_id = 0

        # Test heartbeat module
        self.heartbeat_client = NetAppClientBase(
            {},
            logging_level=logging.getLogger().level,
            stats=stats,
            extended_measuring=False,
        )

        logger.info(f"Register heartbeat client: {HEARTBEAT_ADDRESS}")
        # Register heartbeat client.
        try:
            self.heartbeat_client.register(HEARTBEAT_ADDRESS)
            logger.info(f"Heartbeat client registered")

            logger.info(
                self.heartbeat_client.send_data("GET_BEST_MIDDLEWARE_ADDRESS", HEARTBEAT_CLIENT_EVENT, blocking=True)
            )
        except Exception as ex:
            self.heartbeat_client.disconnect()
            logger.warning(f"Cannot connect to heartbeat module")
            # raise ex

        # Create FCW client.
        if isinstance(netapp_info, MiddlewareAllInfo):
            self.client = NetAppClient(
                {"results": CallbackInfoClient(ChannelType.JSON, self.results_callback)},
                logging_level=logging.getLogger().level,
                stats=stats,
                extended_measuring=extended_measuring,
            )
            logger.info(f"Register with netapp_info: {netapp_info}")
            self.client.connect_to_middleware(netapp_info.middleware_info)
            # Register client.
            try:
                self.client.run_task(
                    task_id=netapp_info.task_id,
                    robot_id=netapp_info.robot_id,
                    resource_lock=False,
                    args={
                        "config": self.config_dict,
                        "camera_config": self.camera_config_dict,
                        "fps": self.fps,
                        "viz": viz,
                        "viz_zmq_port": viz_zmq_port,
                    },
                )
            except Exception as ex:
                self.client.disconnect()
                raise ex
            logger.info(f"Client registered")
        else:
            self.client = NetAppClientBase(
                {"results": CallbackInfoClient(ChannelType.JSON, self.results_callback)},
                logging_level=logging.getLogger().level,
                stats=stats,
                extended_measuring=extended_measuring,
            )
            logger.info(f"Register with netapp_info: {netapp_info}")
            # Register client.
            try:
                self.client.register(
                    netapp_info,
                    args={
                        "config": self.config_dict,
                        "camera_config": self.camera_config_dict,
                        "fps": self.fps,
                        "viz": viz,
                        "viz_zmq_port": viz_zmq_port,
                    },
                )
            except Exception as ex:
                self.client.disconnect()
                raise ex
            logger.info(f"Client registered")

    def info_callback(self, data: Dict[str, Any]) -> None:
        logger.info(data)

    def send_image(self, frame: np.ndarray, timestamp: Optional[int] = None) -> None:
        """Send image to FCW service including rectification.

        Args:
            frame (np.ndarray): Image in numpy array format ("bgr24").
            timestamp (int, optional): Timestamp for frame and results synchronization. Default to current time
                (time.perf_counter_ns())
        """

        if self.client is not None:
            self.frame_id += 1
            frame_undistorted = self.camera.rectify_image(frame)
            if not timestamp:
                timestamp = time.perf_counter_ns()
            if self.stream_type is StreamType.H264:
                self.client.send_image(frame_undistorted, "image_h264", ChannelType.H264, timestamp)
            elif self.stream_type is StreamType.HEVC:
                self.client.send_image(frame_undistorted, "image_hevc", ChannelType.HEVC, timestamp)
            elif self.stream_type is StreamType.JPEG:
                self.client.send_image(frame_undistorted, "image_jpeg", ChannelType.JPEG, timestamp)

    def stop(self) -> None:
        """Print stats and disconnect from FCW service."""

        logger.info("Collision warning client stopping")

        if hasattr(self, "results_viewer") and self.results_viewer is not None:
            self.results_viewer.stats(self.frame_id)
        if self.client is not None:
            self.client.disconnect()

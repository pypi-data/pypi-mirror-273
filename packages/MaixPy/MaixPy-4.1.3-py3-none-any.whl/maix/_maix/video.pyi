"""
maix.video module
"""
from __future__ import annotations
import maix._maix.camera
import maix._maix.err
import maix._maix.image
import typing
__all__ = ['Frame', 'Packet', 'Video', 'VideoType']
class Frame:
    pass
class Packet:
    def __init__(self, data: int, len: int, pts: int = -1, dts: int = -1, duration: int = 0) -> None:
        ...
    def data(self) -> int:
        """
        Get raw data of packet
        
        Returns: raw data
        """
    def data_size(self) -> int:
        """
        Get raw data size of packet
        
        Returns: size of raw data
        """
    def get(self) -> list[int]:
        """
        Get raw data of packet
        
        Returns: raw data
        """
    def is_valid(self) -> bool:
        """
        Check packet is valid
        
        Returns: true, packet is valid; false, packet is invalid
        """
    def set_dts(self, dts: int) -> None:
        """
        Set dts
        
        Args:
          - dts: decoding time stamp.  unit: time_base
        
        
        Returns: true, packet is valid; false, packet is invalid
        """
    def set_duration(self, duration: int) -> None:
        """
        Set duration
        
        Args:
          - duration: packet display time. unit: time_base
        
        
        Returns: true, packet is valid; false, packet is invalid
        """
    def set_pts(self, pts: int) -> None:
        """
        Set pts
        
        Args:
          - pts: presentation time stamp. unit: time_base
        
        
        Returns: true, packet is valid; false, packet is invalid
        """
class Video:
    def __init__(self, path: str = '', width: int = 2560, height: int = 1440, format: maix._maix.image.Format = ..., time_base: int = 30, framerate: int = 30, capture: bool = False, open: bool = True) -> None:
        ...
    def bind_camera(self, camera: maix._maix.camera.Camera) -> maix._maix.err.Err:
        """
        Bind camera
        
        Args:
          - camera: camera object
        
        
        Returns: error code, err::ERR_NONE means success, others means failed
        """
    def capture(self) -> maix._maix.image.Image:
        """
        Capture image
        
        Returns: error code
        """
    def close(self) -> None:
        """
        Close video
        """
    def decode(self, frame: Frame = None) -> maix._maix.image.Image:
        """
        Decode frame
        
        Args:
          - frame: the frame will be decode
        
        
        Returns: decode result
        """
    def encode(self, img: maix._maix.image.Image = ...) -> Packet:
        """
        Encode image.
        
        Args:
          - img: the image will be encode.
        if the img is NULL, this function will try to get image from camera, you must use bind_camera() function to bind the camera.
        
        
        Returns: encode result
        """
    def finish(self) -> maix._maix.err.Err:
        """
        Encode or decode finish
        
        Returns: error code
        """
    def height(self) -> int:
        """
        Get video height
        
        Returns: video height
        """
    def is_closed(self) -> bool:
        """
        check video device is closed or not
        
        Returns: closed or not, bool type
        """
    def is_opened(self) -> bool:
        """
        Check if video is opened
        
        Returns: true if video is opened, false if not
        """
    def is_recording(self) -> bool:
        """
        Check if video is recording
        
        Returns: true if video is recording, false if not
        """
    def open(self, path: str = '', fps: float = 30.0) -> maix._maix.err.Err:
        """
        Open video and run
        
        Args:
          - path: video path. the path determines the location where you load or save the file, if path is none, the video module will not save or load file.
        xxx.h265 means video format is H265, xxx.mp4 means video format is MP4
          - fps: video fps
        
        
        Returns: error code, err::ERR_NONE means success, others means failed
        """
    def width(self) -> int:
        """
        Get video width
        
        Returns: video width
        """
class VideoType:
    """
    Members:
    
      VIDEO_NONE
    
      VIDEO_ENC_H265_CBR
    
      VIDEO_ENC_MP4_CBR
    
      VIDEO_DEC_H265_CBR
    
      VIDEO_DEC_MP4_CBR
    """
    VIDEO_DEC_H265_CBR: typing.ClassVar[VideoType]  # value = <VideoType.VIDEO_DEC_H265_CBR: 3>
    VIDEO_DEC_MP4_CBR: typing.ClassVar[VideoType]  # value = <VideoType.VIDEO_DEC_MP4_CBR: 4>
    VIDEO_ENC_H265_CBR: typing.ClassVar[VideoType]  # value = <VideoType.VIDEO_ENC_H265_CBR: 1>
    VIDEO_ENC_MP4_CBR: typing.ClassVar[VideoType]  # value = <VideoType.VIDEO_ENC_MP4_CBR: 2>
    VIDEO_NONE: typing.ClassVar[VideoType]  # value = <VideoType.VIDEO_NONE: 0>
    __members__: typing.ClassVar[dict[str, VideoType]]  # value = {'VIDEO_NONE': <VideoType.VIDEO_NONE: 0>, 'VIDEO_ENC_H265_CBR': <VideoType.VIDEO_ENC_H265_CBR: 1>, 'VIDEO_ENC_MP4_CBR': <VideoType.VIDEO_ENC_MP4_CBR: 2>, 'VIDEO_DEC_H265_CBR': <VideoType.VIDEO_DEC_H265_CBR: 3>, 'VIDEO_DEC_MP4_CBR': <VideoType.VIDEO_DEC_MP4_CBR: 4>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...

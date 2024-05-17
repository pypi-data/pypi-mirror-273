"""
maix.rtmp module
"""
from __future__ import annotations
import maix._maix.camera
import maix._maix.err
__all__ = ['Rtmp']
class Rtmp:
    def __init__(self, host: str, port: int = 1935, app: str = '', stream: str = '') -> None:
        ...
    def bind_camera(self, cam: maix._maix.camera.Camera) -> maix._maix.err.Err:
        """
        Bind camera
        
        Args:
          - cam: camera object
        
        
        Returns: error code, err::ERR_NONE means success, others means failed
        """
    def get_path(self) -> str:
        """
        Get the file path of the push stream
        
        Returns: file path
        """
    def start(self, path: str = '') -> maix._maix.err.Err:
        """
        Start push stream
        
        Args:
          - path: File path, if you passed file path, cyclic push the file, else if you bound camera, push the camera image.
        
        
        Returns: error code, err::ERR_NONE means success, others means failed
        """
    def stop(self) -> maix._maix.err.Err:
        """
        Stop push
        
        Returns: error code, err::ERR_NONE means success, others means failed
        """

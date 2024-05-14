import os
import base64
import hashlib
from pathlib import Path
from abc import ABC, abstractmethod
from refactor.common import Object


class ResourceInterface(Object):
  """
  This is inferface of resource class that is used for load content from 
  different sources such as file, base64 encoded or URL.
  """

  @property
  def ori(self):
    """
    Get origin source.
    """
    return self._ori
  
  @property
  def local(self):
    """
    Get local path.
    """
    return self._local

  @property
  def data(self):
    """
    Get resource data.
    """
    if self._data is None:
      return self._load(self.ori).data
    return self._data
  
  @property
  def hash(self):
    """
    Get resource hash.
    """
    if self._hash is None:
      self._hash = hashlib.md5(self.data).hexdigest()
    return self._hash
  
  @property
  def base64(self):
    """
    Get resource base64.
    """
    if self._base64 is None:
      self._base64 = str(base64.b64encode(self.data))
    return self._base64

  def __init__(self, ori: str):
    """
    Class constructor.
    :param src:   origin source. Can be file, base64 encoded or URL.
    """
    super().__init__()
    self._ori: str = None
    self._hash: str = None
    self._local: str = None
    self._data: bytes = None
    self._base64: str = None
    self.load(ori)

  @abstractmethod
  def _load(self, ori: str) -> bool:
    """
    Load resource from origin source.
    :param ori: origin source. Can be file, base64 encoded or URL.
    :return:    resource loaded or not.
    """
    self._ori = ori
    self._hash = None
    self._data = None
    self._local = None
    self._base64 = None
    return False

  def load(self, ori):
    """
    Load resource from origin source.
    :param ori: origin source. Can be file, base64 encoded or URL.
    :return:    loaded resource.
    """
    if self._load(ori) is None:
      raise FileNotFoundError(f'Cannot load resource {ori}')
    return self

  def checksum(self, md5: str) -> bool:
    """
    Perform checksum.
    :param md5:   md5 hash to be checked.
    :return:      true or false
    """
    return self.hash == md5
  
  def save(self, dir: str = os.path.join(os.getcwd(), 'resources'), name: str = None, format: str = 'bin') -> Path:
    """
    Save resource to local file.
    :param dir:     saved directory.
    :param name:    saved filename.
    :param format:  saved format.
    :return:        path to saved file.
    """
    dir = Path(dir).expanduser().resolve()
    dir.mkdir(exist_ok=True)
    self._local = dir.joinpath(f'{self.hash if name is None else name}.{format}')
    self._local.write_bytes(self._data)
    return self._local
  
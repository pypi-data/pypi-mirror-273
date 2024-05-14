import base64
import urllib.request
from pathlib import Path
from refactor.utils.resource.abs import ResourceInterface


class Resource(ResourceInterface):
  """
  Resource is used for load content from different sources such as file, base64 encoded or URL.
  """

  @staticmethod
  def __load_file(res: ResourceInterface, ori: str) -> ResourceInterface:
    """
    Load resource data from file.
    :param res:   resource to be loaded.
    :param ori:   path to file.
    :return:      resource.
    """
    path = Path(ori).expanduser().resolve()
    res._data = path.read_bytes()
    res._ori = path
    return res

  @staticmethod
  def __load_base64(res: ResourceInterface, ori: str) -> ResourceInterface:
    """
    Load resource data from base64 encoded string.
    :param res:   resource to be loaded.
    :param ori:   base64 string.
    :return:      resource.
    """
    res._data = base64.b64decode(ori, validate=True)
    return res

  @staticmethod
  def __load_url(res: ResourceInterface, ori: str) -> ResourceInterface:
    """
    Load resource data from URL.
    :param res:   resource to be loaded.
    :param ori:   url string.
    :return:      resource.
    """
    with urllib.request.urlopen(ori) as response:
      res._data = response.read()
      return res

  def _load(self, ori: str) -> ResourceInterface:
    """
    Load resource from origin source.
    :param ori:   origin source.
    :return:      loaded resource.
    """
    super()._load(ori)
    try:
      res = Resource.__load_file(self, ori)
      self.logger.debug(f'Sucess load file {ori}')
      return res
    except:
      self.logger.debug(f'Fail to load file {ori}')
    try:
      res = Resource.__load_base64(self, ori)
      self.logger.debug(f'Sucess load base64 {ori}-20s')
      return res
    except:
      self.logger.debug(f'Fail to load base64 {ori}-20s')
    try:
      res = Resource.__load_url(self, ori)
      self.logger.debug(f'Sucess load URL {ori}')
      return res
    except:
      self.logger.debug(f'Fail to load URL {ori}')

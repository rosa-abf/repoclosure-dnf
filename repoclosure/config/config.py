import re
import sys
import json

class Config:
  def __init__(self, path):
    self.__path = path
    self.__load()

  def __load(self):
    try:
      config_text = ''
      with open(self.__path, "r") as cf:
        config_text = cf.read()

      self.__json = json.loads(config_text)
    except Exception as e:
      print("Failed to load config file at %s: %s" % (self.path, e))
      sys.exit(1)

  def platforms(self):
    for platform in self.__json['platforms']:
      for repository in platform['repositories']:
        for arch in platform['arches']:
          for type in platform['types']:
            yield platform, repository, arch, type
            yield platform, repository, 'SRPMS+{}'.format(arch), type

  def output_path(self):
    return re.sub(r'\/+$', '', self.__json['output_path'])

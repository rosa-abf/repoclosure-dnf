import os
import sys
import time
from shutil import copyfile
from .config import Config
from .dnf import run_repoclosure
from .renders import render_repoclosure, render_index, render_compressed_repoclosure
from .utils import generate_compressed_report

def prepare_output_dir(output_path):
  new_path = output_path + '/new'
  try:
    if not os.path.isdir(output_path):
      os.makedirs(output_path)
    if not os.path.isdir(new_path):
      os.makedirs(new_path)
    else:
      os.system("rm -f %s/*.{html,png,css}" % new_path)
  except Exception as e:
    print("Don't have access to output directory or can't create one: %s" % e)
    sys.exit(1)

def copy_assets(path):
  c = 'repoclosure/templates/assets'
  for i in os.listdir(c):
    copyfile(c + '/' + i, path + '/' + i)

def replace_report(current_path, new_path):
  os.system("rm -f %s/*.{html,png,css}" % current_path)
  os.system("mv %s/*.{html,png,css} %s" % (new_path, current_path))
  os.rmdir(new_path)

def main(config_path):
  start_time = time.time()
  config = Config(config_path)
  output_path = config.output_path()

  prepare_output_dir(output_path)

  counters = {}

  platforms = []
  for platform, repository, arch, type in config.platforms():
    platform_name = platform['name']
    if platform_name not in platforms:
      platforms.append(platform_name)

    name = '%s-%s-%s_%s' % (platform_name, arch, repository, type)
    print('Processing %s' % name)
    result = run_repoclosure(platform, repository, arch, type)
    if platform_name not in counters:
      counters[platform_name] = {
        'types': [],
        'arches': [],
        'repositories': [],
        'counts': {}
      }
    counter = counters[platform_name]

    if type not in counter['types']:
      counter['types'].append(type)
    if arch not in counter['arches']:
      counter['arches'].append(arch)
    if repository not in counter['repositories']:
      counter['repositories'].append(repository)

    key = "%s#%s#%s" % (type, repository, arch)

    error = False
    if 'count' in result and result['count'] >= 0:
      counter['counts'][key] = result['count']
    else:
      error = True
      counter['counts'][key] = -1

    if result['return_code'] == 0 and result['count'] == 0:
      continue

    render_repoclosure(result, name, 'c' + name + '.html', output_path + '/new/' + name + '.html')
    if not error:
      render_compressed_repoclosure(
        generate_compressed_report(result['report']),
        name,
        name + '.html',
        output_path + '/new/c' + name + '.html'
      )

  render_index(platforms, counters, time.time() - start_time, output_path + '/new/index.html')
  copy_assets(output_path + '/new')
  replace_report(output_path, output_path + '/new')
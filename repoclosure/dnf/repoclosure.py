import os
import re
import subprocess
from ..utils import get_repo_list
from .package_to_srpm import get_srpm_for_platform

def process_repoclosure_output(output):
  if 'package:' not in output:
    return {}

  report = output.split("\n")
  result = {}
  cur_package = ''
  cur_unresolved_deps = []
  for line in report:
    sline = line.strip()
    if sline == '':
      continue
    if sline.startswith("package:"):
      if len(cur_unresolved_deps) > 0:
        result[cur_package] = cur_unresolved_deps
      cur_package = sline.split("package:")[1].split(" from")[0].strip()
      cur_unresolved_deps = []
    elif sline != "unresolved deps:":
      cur_unresolved_deps.append(sline)

  if len(cur_unresolved_deps) > 0:
    result[cur_package] = cur_unresolved_deps

  return result

def generate_repoclosure_command(platform, repository, arch, type):
  cmd_parts = ['/usr/bin/dnf -q --setopt=keepcache=False --setopt=reposdir=/dev/null']
  cmd_parts.append('--setopt=metadata_expire=0 --disablerepo=*')
  repo_list = get_repo_list(platform, repository, arch, type)
  cmd_parts += ["--repofrompath=%s,%s --enablerepo=%s" % (name, url, name) for name, url in repo_list]
  check_repo = '%s_%s-"%s"' % (repository, type, arch)
  cmd_parts.append('repoclosure --check %s --arch "%s" --arch noarch \
                    --forcearch "%s" --obsoletes --showduplicates -y' % (check_repo, arch, arch))

  return re.sub(r'\s+', ' ', ' '.join(cmd_parts))

def clear_repos():
  os.system("rm -rf /etc/yum.repos.d/*")

def run_repoclosure(platform, repository, arch, type):
  try:
    clear_repos()
    cmd = generate_repoclosure_command(platform, repository, arch, type)
    completed_process = subprocess.run(cmd, capture_output=True, shell=True)
    output = completed_process.stdout.decode("utf-8")
    stderr = completed_process.stderr.decode("utf-8")
    processed = process_repoclosure_output(output)
    srpm = get_srpm_for_platform(platform, repository, arch, type)
    if 'return_code' in srpm:
      empty_return = {
        'report': [],
        'count': 0,
        'total_count': 0,
        'percent': 0
      }
      return {**srpm, **empty_return}
    report = []
    for package in processed:
      srpm_col = "N/A"
      if package in srpm:
        srpm_col = srpm[package]
      report.append(
        (
          package,
          srpm_col,
          "\n".join(sorted(processed[package]))
        )
      )
    report.sort(key = lambda x: (x[1], x[0]))
    count = len(report)
    total_count = len(srpm)
    percent = 0
    if total_count > 0:
      percent = round(count / total_count * 100, 2)
    return {
      "report": report,
      "errors_raw": stderr.strip(),
      "return_code": completed_process.returncode,
      "count": count,
      "total_count": total_count,
      "percent": percent
    }
  except Exception as e:
    return {
      "errors_raw": "Exception %s: %s" % (e.__class__.__name__, str(e)),
      "return_code": -1
    }

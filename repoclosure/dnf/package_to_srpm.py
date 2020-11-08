import re
import subprocess
from ..utils import get_repo_list

def get_srpm_command(platform, repository, arch, type):
  cmd_parts = ["dnf -q --setopt=keepcache=False --setopt=reposdir=/dev/null",
               "--setopt=metadata_expire=0 --disablerepo=*"]
  repo_name, repo_url = get_repo_list(platform, repository, arch, type, srpm_list = True)[0]
  cmd_parts.append('--repofrompath=%s,%s --enablerepo=%s' % (repo_name, repo_url, repo_name))
  cmd_parts.append('repoquery --qf "%{name}-%{evr}.%{arch}#%{sourcerpm}" "*"')

  return re.sub(r'\s+', ' ', ' '.join(cmd_parts))

def get_srpm_for_platform(platform, repository, arch, type):
  cmd = get_srpm_command(platform, repository, arch, type)
  try:
    completed_process = subprocess.run(cmd, capture_output=True, shell=True)
    stderr = completed_process.stderr.decode("utf-8")
    if completed_process.returncode != 0:
      return {
        "errors_raw": stderr,
        "return_code": completed_process.returncode
      }
    res = {}
    stdout = completed_process.stdout.decode("utf-8").split("\n")
    for line in stdout:
      sline = line.strip()
      if sline == '':
        continue
      package, srpm = sline.split('#')
      res[package] = srpm
    return res
  except Exception as e:
    return {
      "errors_raw": "Exception %s: %s" % (e.__class__.__name__, str(e)),
      "return_code": -1
    }

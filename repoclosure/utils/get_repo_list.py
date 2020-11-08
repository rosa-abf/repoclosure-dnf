import re

def get_item(platform, repository, arch, type):
  platform_base_url = re.sub(r'\/+$', '', platform['url'])

  return (
    '%s_%s-"%s"' % (repository, type, arch),
    '%s/%s/%s/%s' % (platform_base_url, arch, repository, type)
  )

def get_repo_list(platform, repository, arch, type, srpm_list = False):
  repo_list = []

  if srpm_list:
    return [get_item(platform, repository, arch, type)]

  repo_list.append(get_item(platform, 'main', arch, 'release'))
  repo_list.append(get_item(platform, 'main', arch, 'updates'))

  if repository == 'main':
    return repo_list

  repo_list.append(get_item(platform, repository, arch, 'release'))
  repo_list.append(get_item(platform, repository, arch, 'updates'))

  return repo_list

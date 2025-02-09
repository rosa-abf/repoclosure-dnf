import re

def get_item(platform, repository, arch, type):
  platform_base_url = re.sub(r'\/+$', '', platform['url'])

  return (
    '%s_%s-"%s"' % (repository, type, arch),
    '%s/%s/%s/%s' % (platform_base_url, arch, repository, type)
  )

def get_repo_list(platform, repository, arch, type):
  repo_list = []

  srpms_mode = False
  if arch.startswith('SRPMS+'):
    arch = arch.split('+')[1]
    srpms_mode = True

  if srpms_mode:
    repo_list.append(get_item(platform, 'main', 'SRPMS', 'release'))
  repo_list.append(get_item(platform, 'main', arch, 'release'))
  if type == 'updates':
    if srpms_mode:
      repo_list.append(get_item(platform, 'main', 'SRPMS', 'updates'))
    repo_list.append(get_item(platform, 'main', arch, 'updates'))

  if type == 'testing':
    if srpms_mode:
      repo_list.append(get_item(platform, 'main', 'SRPMS', 'testing'))

    repo_list.append(get_item(platform, 'main', arch, 'testing'))

  if repository == 'main':
    return repo_list

  if srpms_mode:
    repo_list.append(get_item(platform, repository, 'SRPMS', 'release'))
  repo_list.append(get_item(platform, repository, arch, 'release'))
  if type == 'updates':
    if srpms_mode:
      repo_list.append(get_item(platform, repository, 'SRPMS', 'updates'))
    repo_list.append(get_item(platform, repository, arch, 'updates'))
  if type == 'testing':
    if srpms_mode:
      repo_list.append(get_item(platform, repository, 'SRPMS', 'testing'))
    repo_list.append(get_item(platform, repository, arch, 'testing'))

  return repo_list

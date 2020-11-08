def generate_compressed_report(report):
  h = {}
  for package, srpm, unresolved in report:
    if unresolved not in h:
      h[unresolved] = {}
    if srpm not in h[unresolved]:
      h[unresolved][srpm] = []
    
    h[unresolved][srpm].append(package)

  report = []
  for unresolved in h:
    srpms = list(h[unresolved].keys())
    srpms.sort(key = lambda x: len(h[unresolved][x]))
    packages = ''
    cnt = 0
    for srpm in srpms:
      cnt += len(h[unresolved][srpm])
      packages += 'SRPM: %s\n' % srpm
      packages += '\n'.join(h[unresolved][srpm]) + '\n'
    report.append((unresolved, packages.strip(), cnt))

  report.sort(key = lambda x: -x[2])

  return [(x[0], x[1]) for x in report]
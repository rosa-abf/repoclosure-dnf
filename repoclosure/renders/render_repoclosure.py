from ..templates import repoclosure

def render_repoclosure(result, title, compressed_report, path):
  t = repoclosure()
  if result['return_code'] == -1:
    t.code = -1
    t.title = title
    t.errors = result['errors_raw']
  else:
    t.bad_packages = result['report']
    t.code = result['return_code']
    t.errors = result['errors_raw']
    t.count = result['count']
    t.title = title
    t.total_count = result['total_count']
    t.percent = result['percent']
    t.compressed = compressed_report
  with open(path, "w") as f:
    f.write(t.respond())

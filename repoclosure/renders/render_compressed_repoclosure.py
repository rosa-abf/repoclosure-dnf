from ..templates import compressed_repoclosure

def render_compressed_repoclosure(bad_packages, title, normal_name, path):
  t = compressed_repoclosure()
  t.bad_packages = bad_packages
  t.normal = normal_name
  t.title = title
  with open(path, "w") as f:
    f.write(t.respond())
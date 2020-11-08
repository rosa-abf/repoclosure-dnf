from datetime import datetime
from ..templates import index

def render_index(platforms, counters, generated_in, path):
  t = index()
  t.platforms = platforms
  t.counters = counters
  t.title = "Index page"
  t.generated_on = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
  t.generated_in = "%.2fs" % round(generated_in, 3)

  with open(path, "w") as f:
    f.write(t.respond())
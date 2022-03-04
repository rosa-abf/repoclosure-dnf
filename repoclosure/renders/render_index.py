from datetime import datetime
from ..templates import index

def render_index(platforms, counters, generated_in, path):
  t = index()
  t.platforms = platforms
  t.counters = counters
  t.title = "Index page"
  generated_on = datetime.utcnow()
  t.generated_on_utc = generated_on.strftime("%Y-%m-%d %H:%M:%S UTC")
  t.generated_on_ts = round(generated_on.timestamp()) * 1000
  t.generated_in = "%.2fs" % round(generated_in, 3)

  with open(path, "w") as f:
    f.write(t.respond())

#!/usr/bin/env python3

import os
from repoclosure import main

if __name__ == "__main__":
  main("%s/config.json" % os.path.dirname(os.path.abspath(__file__)))

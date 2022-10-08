#!/usr/bin/env python

import os
import sys

from pathlib import Path


path = Path(os.path.abspath(__file__))
sys.path.append(path.parent.parent)

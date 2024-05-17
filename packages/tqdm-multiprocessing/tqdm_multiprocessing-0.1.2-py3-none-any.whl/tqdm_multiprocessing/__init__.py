#!/usr/bin/env python
# -*- coding: utf-8 -*-
import importlib.metadata

from .mapper import ConcurrentMapper


__all__ = ["ConcurrentMapper"]
__version__ = importlib.metadata.version("tqdm_multiprocessing")

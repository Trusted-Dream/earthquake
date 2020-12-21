#!/bin/env python
import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

URL = os.environ.get("URL")
UA = dict([os.environ.get("UA").split(':')])
TSUNAMI = os.environ.get("TSUNAMI")
HAZARD = os.environ.get("HAZARD")
TRAIN = os.environ.get("TRAIN")
TESTSRV = os.environ.get("TESTSRV")
YUNSRV = os.environ.get("YUNSRV")
MAMANSRV = os.environ.get("MAMANSRV")
FILE = os.environ.get("FILE")

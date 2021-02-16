# https://github.com/pywinauto/pywinauto/issues/472
import sys
sys.coinit_flags = 2
import warnings
warnings.simplefilter("ignore", UserWarning)
import pywinauto

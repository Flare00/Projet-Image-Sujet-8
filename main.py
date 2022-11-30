#!/usr/bin/env python3

import logging, os
logging.disable(logging.WARNING)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
print("[INFO] Loading TensorFlow...")

import src.interface as interface
print("[INFO] TensorFlow Loaded.")

def main():
    interface.initInterface()
    interface.startInterface()

if __name__== "__main__":
    main()
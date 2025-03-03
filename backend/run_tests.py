#!/usr/bin/env python
"""
Test runner for the Homework Marking System.
"""
import unittest
import sys
import os

if __name__ == "__main__":
    # Add the parent directory to sys.path to allow importing modules
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

    if len(sys.argv) > 1:
        # Run specific test module(s)
        test_modules = sys.argv[1:]
        for module in test_modules:
            suite = unittest.TestLoader().loadTestsFromName(module)
            result = unittest.TextTestRunner(verbosity=2).run(suite)
            if not result.wasSuccessful():
                sys.exit(1)
    else:
        # Run all tests
        test_suite = unittest.defaultTestLoader.discover('tests')
        result = unittest.TextTestRunner(verbosity=2).run(test_suite)
        if not result.wasSuccessful():
            sys.exit(1)

    sys.exit(0)

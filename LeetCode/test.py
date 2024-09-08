from script import minDistance
import unittest
import time

# Property: The minDistance between a word and itself is always zero

def benchify_test_minDistance_identity(word):
    assert minDistance(word, word) == 0


# The next test is failing.
def test_minDistance_identity_failure_0():
    word='vHTF'
    benchify_test_minDistance_identity(word)
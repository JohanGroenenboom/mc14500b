from mc14500b import MC14500B, OPCODE
import unittest

class TestMC14500B(unittest.TestCase):

    def test_load_true(self):
        mc = MC14500B()
        mc.opcode = OPCODE.LD
        mc.data = True
        mc.execute()
        self.assertEqual(mc.data, True)

    def test_load_false(self):
        mc = MC14500B()
        mc.opcode = OPCODE.LD
        mc.data = False
        mc.execute()
        self.assertEqual(mc.data, False)

    def test_load_complement(self):
        mc = MC14500B()
        mc.opcode = OPCODE.LDC
        mc.data = True
        mc.execute()
        self.assertEqual(mc.data, False)

        mc.data = False
        mc.execute()
        self.assertEqual(mc.data, True)

 
    def test_and(self):
        # GIVEN:
        # A 1 loaded into the RR
        mc = MC14500B()
        mc.opcode = OPCODE.LD
        mc.data = True
        mc.execute()

        # WHEN:
        # AND with data = 1
        mc.opcode = OPCODE.AND
        mc.data = True
        mc.execute()
        # THEN:
        # The result should be 1
        self.assertEqual(mc.data, True)

        mc.data = False
        mc.execute()
        self.assertEqual(mc.data, False)

    def test_or(self):
        # GIVEN:
        # An initial MC with RR = False
        mc = MC14500B()

        # WHEN:
        # OR with data = False
        mc.opcode = OPCODE.OR
        mc.data = False
        mc.execute()
        # THEN:
        # The result should be False
        self.assertEqual(mc.data, False)

        # WHEN:
        # OR with data = True
        mc.data = True
        mc.execute()
        # THEN:
        # The result should be True
        self.assertEqual(mc.data, True)

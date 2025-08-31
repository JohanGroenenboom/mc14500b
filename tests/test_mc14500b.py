from mc14500b import MC14500B, OPCODE
import unittest

class TestMC14500B(unittest.TestCase):

    def test_input_output_separation(self):
        # GIVEN:
        # An initial MC14500B with (input) data set to True
        # and opcode set to LD
        mc = MC14500B()
        mc.opcode = OPCODE.LD
        mc.data = True
        # WHEN: reading the (output) data
        # THEN: output data is still False
        self.assertEqual(mc.data, False)
        # WHEN: executing the Load instruction
        mc.execute()
        # THEN: output data is now True
        self.assertEqual(mc.data, True)

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
        # An initial mc14500b with RR = 0
        mc = MC14500B()

        # WHEN:
        # AND with data = 1
        mc.data = True
        mc.opcode = OPCODE.AND
        mc.execute()

        # THEN:
        # The result should be False
        self.assertEqual(mc.data, False)

        # WHEN:
        # A 1 loaded into the RR
        # AND with data = 1
        mc.opcode = OPCODE.LD
        mc.data = True
        mc.execute()
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

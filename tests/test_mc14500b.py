from mc14500b import MC14500B, OPCODE
import unittest

class TestMC14500B(unittest.TestCase):

    def setUp(self):
        self.mc = MC14500B()
        self.input_data = False
        self.mc.connect_data_input(lambda: self.input_data)
        self.opcode = OPCODE.NOP0
        self.mc.connect_instruction_input(lambda: self.opcode)

    def test_input_output_separation(self):
        # GIVEN:
        # An initial MC14500B with (input) data set to True
        # and opcode set to LD
        self.opcode = OPCODE.LD
        self.input_data = True
        # WHEN: reading the (output) data
        # THEN: output data is still False
        self.assertEqual(self.mc.data, False)
        # WHEN: executing the Load instruction
        self.mc.execute()
        # THEN: output data is now True
        self.assertEqual(self.mc.data, True)

    def test_load_true(self):
        self.opcode = OPCODE.LD
        self.input_data = True
        self.mc.execute()
        self.assertEqual(self.mc.data, True)

    def test_load_false(self):
        self.opcode = OPCODE.LD
        self.input_data = False
        self.mc.execute()
        self.assertEqual(self.mc.data, False)

    def test_load_complement(self):
        self.opcode = OPCODE.LDC
        self.input_data = True
        self.mc.execute()
        self.assertEqual(self.mc.data, False)

        self.input_data = False
        self.mc.execute()
        self.assertEqual(self.mc.data, True)

    def test_and(self):
        # GIVEN:
        # An initial mc14500b with RR = 0

        # WHEN:
        # AND with data = 1
        self.input_data = True
        self.opcode = OPCODE.AND
        self.mc.execute()

        # THEN:
        # The result should be False
        self.assertEqual(self.mc.data, False)

        # WHEN:
        # A 1 loaded into the RR
        # AND with data = 1
        self.opcode = OPCODE.LD
        self.input_data = True
        self.mc.execute()
        self.opcode = OPCODE.AND
        self.input_data = True
        self.mc.execute()
        # THEN:
        # The result should be 1
        self.assertEqual(self.mc.data, True)

        self.input_data = False
        self.mc.execute()
        self.assertEqual(self.mc.data, False)

    def test_or(self):
        # GIVEN:
        # An initial MC with RR = False

        # WHEN:
        # OR with data = False
        self.opcode = OPCODE.OR
        self.input_data = False
        self.mc.execute()
        # THEN:
        # The result should be False
        self.assertEqual(self.mc.data, False)

        # WHEN:
        # OR with data = True
        self.input_data = True
        self.mc.execute()
        # THEN:
        # The result should be True
        self.assertEqual(self.mc.data, True)

    def test_sto(self):
        self.input_data = True
        self.opcode = OPCODE.LD
        self.mc.execute()
        self.opcode = OPCODE.STO
        self.mc.execute()
        self.assertEqual(self.mc.data, True)

    def test_stoc(self):
        self.input_data = True
        self.opcode = OPCODE.LD
        self.mc.execute()
        self.opcode = OPCODE.STOC
        self.mc.execute()
        self.assertEqual(self.mc.data, False)
        self.input_data = False
        self.opcode = OPCODE.LD
        self.mc.execute()
        self.opcode = OPCODE.STOC
        self.mc.execute()
        self.assertEqual(self.mc.data, True)

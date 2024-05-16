import unittest

from libsrg.Config import Config

from Santa_IW.Status import Status
from Santa_IW.Subassembly import Subassembly

args_0 = Config({"source": "args_0", "a0": "vala0", "tree_name_separator": ".", "pull_up_child_annotation": True})

args_1 = Config({"source": "args_1", "a1": "vala1"})

args_2 = Config({"source": "args_2", "a2": "vala2"})


class MyTestCase(unittest.TestCase):
    def test_constructors(self):
        Subassembly.reset_class_for_unittest()

        sub_0 = Subassembly(instance_config=args_0, short_name="sub0", parent=None)
        sub_1 = Subassembly(instance_config=args_1, short_name="sub1", parent=sub_0)
        sub_2a = Subassembly(instance_config=args_2, short_name="sub2a", parent=sub_1)
        sub_2b = Subassembly(instance_config=args_2, short_name="sub2b", parent=sub_1)

        self.assertEqual("sub0", sub_0.name())
        self.assertEqual("sub1.sub0", sub_1.name())
        self.assertEqual("sub2a.sub1.sub0", sub_2a.name())
        self.assertEqual("sub2b.sub1.sub0", sub_2b.name())

        expc = {sub_2a, sub_2b}
        actc = set(sub_1.children())
        self.assertEqual(expc, actc)

    def test_status(self):
        Subassembly.reset_class_for_unittest()

        sub_0 = Subassembly(instance_config=args_0, short_name="sub0", parent=None)
        sub_1 = Subassembly(instance_config=args_1, short_name="sub1", parent=sub_0)
        sub_2a = Subassembly(instance_config=args_2, short_name="sub2a", parent=sub_1)

        exp = Status.OK
        act = sub_2a.latest_status()
        self.assertEqual(exp, act)

        cs = sub_1._child_summation.as_dict()
        self.assertEqual(0, len(cs))

        exp = Status.OK
        act = sub_2a.assess_overall_status()
        self.assertEqual(exp, act)

        cs = sub_1._child_summation.as_dict()
        print(cs)
        self.assertEqual(1, len(cs))
        self.assertEqual(exp, act)


if __name__ == '__main__':
    unittest.main()

import unittest
from gitbuilding.buildup.pageorder import PageOrderEntry, PageOrder

#pylint: disable=protected-access

class PageorderingTestCase(unittest.TestCase):

    def test_make_link_depth_and_parent(self):
        p1 = PageOrderEntry(path="index.md",depth=0,variables=None,parent=None)
        p2 = PageOrderEntry(path="p2.md",depth=1,variables=None,parent="index.md")
        p3 = PageOrderEntry(path="p3.md",depth=2,variables=None,parent="p2.md")
        p4 = PageOrderEntry(path="p4.md",depth=1,variables=None,parent="index.md")
        p5 = PageOrderEntry(path="p5.md",depth=2,variables=None,parent="p4.md")
        p6 = PageOrderEntry(path="p6.md",depth=2,variables=None,parent="p4.md")

        pagelist = [p1, p2, p3, p4, p5, p6]

        # cases are tuples of: list of link_used inputs and result
        # link_used is a list of booleans saying if the make link is used on that page

        cases = [([False, False, True, False, True, False], (1, 'index.md', 1)),
                 ([False, False, True, True, False, False], (1, 'index.md', 1)),
                 ([False, False, False, False, True, True], (2, 'p4.md', 4))]

        for link_used, expected_result in cases:
            result = PageOrder._get_make_link_depth_parent_and_pos(None, link_used, pagelist)
            self.assertEqual(result, expected_result)

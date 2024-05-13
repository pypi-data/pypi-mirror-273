import unittest
import sys
from unittest.mock import patch
import os
import logging
from gitbuilding.buildup import FileInfo, Documentation
from gitbuilding.buildup.page import Page, VariationPage


#pylint: disable=protected-access

class PageTestCase(unittest.TestCase):

    def setUp(self):
        self.doc = Documentation({},'')

    def _dummy_page(self, content, path="path.md"):
        file_obj = FileInfo(path, content=content, dynamic_content=True)
        page = Page(file_obj, self.doc)
        self.doc._pages.append(page)
        return page

    def _test_page(self, number, path="path.md"):
        directory = os.path.join(os.path.dirname(__file__),'TestPages')
        testpage_path = os.path.join(directory, f"testpage{number}.md")
        with open(testpage_path, 'r', encoding='utf-8') as testpage:
            content = testpage.read()
        return self._dummy_page(content, path)

    def test_summary(self):
        page = self._dummy_page("# blah", path="path.md")
        self.assertEqual(str(page), '<Page: path.md>')
        self.assertEqual(page.summary, 'blah')
        page = self._dummy_page("This is a short page")
        self.assertEqual(page.summary, "This is a shor...")
        page = self._dummy_page("Very short!")
        self.assertEqual(page.summary, "Very short!")

    def test_title(self):
        page = self._dummy_page("# blah")
        self.assertEqual(page.title, 'blah')

    def test_variations(self):
        page = self._dummy_page("This is a short page")

        variables = None
        varpage1 = page.get_variation(variables)
        self.assertNotIsInstance(varpage1, VariationPage)
        self.assertIs(page, varpage1)

        variables = {'good': 'yes'}
        varpage2 = page.get_variation(variables)
        self.assertNotIsInstance(varpage2, VariationPage)
        self.assertIs(page, varpage2)

        variables = {'var_good': 'yes'}
        varpage3 = page.get_variation(variables)
        self.assertIsInstance(varpage3, VariationPage)
        self.assertEqual(varpage3.variables, variables)

        varpage4 = page.get_variation(variables)
        self.assertIs(varpage3, varpage4)

        variables = {'var_good': 'no'}
        varpage5 = page.get_variation(variables)
        self.assertIsInstance(varpage5, VariationPage)
        self.assertIsNot(varpage3, varpage5)

    def test_preprocess(self):
        page = self._dummy_page("{{includetext: 'yes', if: var_good is yes}}")

        variables = {'var_good': 'yes'}
        varpage = page.get_variation(variables)

        self.assertFalse(page.preprocessed_md.endswith('yes'))
        self.assertTrue(varpage.preprocessed_md.endswith('yes'))

    def test_tags(self):
        page = self._test_page(1)
        self.assertEqual(len(page.tags), 1)
        page = self._dummy_page("blah blah")
        self.assertIsInstance(page.tags, list)
        self.assertEqual(len(page.tags), 0)
        page = self._dummy_page("---\nTags:\n  - great\n  - ok\n---\nBlah")
        self.assertEqual(len(page.tags), 2)

    def test_page_links(self):
        page = self._test_page(1)
        self.assertEqual(len(page.plain_links), 1)
        self.assertEqual(len(page.steps), 2)


    @patch.object(Documentation, 'get_page_list') 
    def test_page_lists(self, mock_page_list):

        page1 = self._dummy_page("# blah", path="path.md")
        page2 = self._dummy_page("# blah2", path="place/path2.md")
        mock_page_list.return_value = [page1, page2]

        contents = ["# blah\n\n{{listpages, tag:info}}", "# blah\n\n{{listpages}}"]
        calls = [['info'], []]
        for content, call_args in zip(contents, calls):
            thispage = self._dummy_page(content, path="place/this.md")
            text = thispage._replace_page_lists(content)
            self.assertTrue(len(text)>len(content), f"before:\n{content}\n\nafter:\n{text}")
            mock_page_list.assert_called_with(*call_args)
            self.assertTrue('* [blah](../path.md)' in text, f"Unexpected result in:\n{text}")
            self.assertTrue('* [blah2](path2.md)' in text, f"Unexpected result in:\n{text}")

    def test_get_empty_step_tree(self):
        page1 = self._dummy_page("# blah", path="path.md")
        tree = page1.get_step_tree()
        self.assertIsInstance(tree, dict)
        self.assertEqual(len(tree["path.md"]), 0)

    def test_step_tree_following(self):
        #These two pages are step linked in test page 1
        page1 = self._dummy_page("# blah", path="something.md")
        page2 = self._dummy_page("# blah2", path="somethingelse.md")
        testpage = self._test_page(1, path="path.md")

        self.assertIsNone(page1._step_tree)
        self.assertIsNone(page2._step_tree)

        tree = testpage.get_step_tree()
        #Step tree is now set for calling pages showing it is following
        self.assertIsNotNone(page1._step_tree)
        self.assertIsNotNone(page2._step_tree)
        self.assertEqual(len(tree["path.md"]), 2, str(tree))
        self.assertIn("something.md", tree["path.md"][0], str(tree["path.md"][0]))
        self.assertIn("somethingelse.md", tree["path.md"][1])

    def test_step_tree_circular(self):
        #These two pages are step linked in test page 1
        self._dummy_page("# blah\n\n[.](path.md){step}", path="something.md")
        self._dummy_page("# blah2", path="somethingelse.md")
        testpage = self._test_page(1, path="path.md")

        with self.assertLogs(logger='BuildUp', level=logging.WARN):
            testpage.get_step_tree()

    def test_no_page_order(self):
        self._dummy_page("# blah", path="something.md")
        self._dummy_page("# blah2", path="somethingelse.md")

        self.doc._set_page_order()
        order = self.doc.page_order
        self.assertEqual(order.number_of_paths, 0)
        self.assertEqual("<PageOrder: No page ordering>", str(order), str(order))

    def test_page_order(self):
        #These two pages are step linked in test page 1
        self._dummy_page("# blah", path="something.md")
        self._dummy_page("# blah2", path="somethingelse.md")
        self._test_page(1, path="path.md")

        self.doc._set_page_order()
        order = self.doc.page_order
        self.assertEqual(order.number_of_paths, 1)
        self.assertEqual(len(order.pagelists[0]), 3)
        self.assertEqual(order.pagelists[0][0], "path.md")
        self.assertEqual(order.pagelists[0][0].depth, 0)
        self.assertEqual(order.pagelists[0][1], "something.md")
        self.assertEqual(order.pagelists[0][1].depth, 1)
        self.assertEqual(order.pagelists[0][2].parent, "path.md")
        self.assertEqual(order.pagelists[0][2], "somethingelse.md")
        self.assertEqual(order.pagelists[0][2].depth, 1)
        self.assertEqual(order.pagelists[0][2].parent, "path.md")
        self.assertIn("<PageOrder", str(order), str(order))
        self.assertIn("<PageOrderEntry path: path.md, variables: None", str(order), str(order))
        self.assertIn("<PageOrderEntry path: something.md, variables: None", str(order), str(order))
        self.assertIn("<PageOrderEntry path: somethingelse.md, variables: None", str(order), str(order))


    def test_muliple_pagelists(self):
        #These two pages are step linked in test page 1
        self._dummy_page("# blah", path="something.md")
        self._dummy_page("# blah2", path="somethingelse.md")
        self._test_page(1, path="path.md")
        self._test_page(2, path="another.md")

        self.doc._set_page_order()
        order = self.doc.page_order

        self.assertEqual(len(order.trees), 2)

        self.assertEqual(order.number_of_paths, 2)
        self.assertEqual(len(order.pagelists[0]), 3)
        self.assertEqual(len(order.pagelists[1]), 3, order.pagelists[1])
        self.assertEqual(order.pagelists[0][0], "path.md")
        self.assertEqual(order.pagelists[0][1], "something.md")
        self.assertEqual(order.pagelists[0][2], "somethingelse.md")
        self.assertEqual(order.pagelists[1][0], "another.md")
        self.assertEqual(order.pagelists[1][1], "something.md")
        self.assertEqual(order.pagelists[1][2], "somethingelse.md")
        self.assertIn("<PageOrderEntry path: path.md, variables: None", str(order), str(order))
        self.assertIn("<PageOrderEntry path: something.md, variables: None", str(order), str(order))
        self.assertIn("<PageOrderEntry path: somethingelse.md, variables: None", str(order), str(order))
        self.assertIn("<PageOrderEntry path: another.md, variables: None", str(order), str(order))
        self.assertIn("<PageOrderEntry path: something.md, variables: {'var_great': 'yes'}", str(order), str(order))
        self.assertNotIn("<PageOrderEntry path: somethingelse.md, variables: {'var_great': 'yes'}", str(order), str(order))

        #check where the pages are moved to
        _, replace_links = order.get_pagelist_for_page("path.md")
        self.assertEqual(replace_links['something.md'], 'path/something.md')
        self.assertEqual(replace_links['somethingelse.md'], 'path/somethingelse.md')

        _, replace_links = order.get_pagelist_for_page("another.md")
        self.assertEqual(replace_links['something.md'], 'another/something.md')
        self.assertEqual(replace_links['somethingelse.md'], 'another/somethingelse.md')

    def test_page_order_with_make_link(self):
        #These two pages are step linked in test page 1
        self._dummy_page("# blah", path="something.md")
        md = ("# Blah2\n\n"
              "In this step you will use the [thing](thing.md){make, qty:1} you already made\n")
        self._dummy_page(md, path="somethingelse.md")
        self._dummy_page("# thingy", path="thing.md")
        self._test_page(1, path="path.md")

        self.doc._set_page_order()
        order = self.doc.page_order
        self.assertEqual(order.number_of_paths, 1)
        self.assertEqual(len(order.pagelists[0]), 4, str(order.pagelists[0]))
        self.assertEqual(order.pagelists[0][0], "path.md")
        self.assertEqual(order.pagelists[0][1], "something.md")
        self.assertEqual(order.pagelists[0][2], "thing.md")
        self.assertEqual(order.pagelists[0][3], "somethingelse.md")
        self.assertIn("<PageOrderEntry path: path.md, variables: None", str(order), str(order))
        self.assertIn("<PageOrderEntry path: something.md, variables: None", str(order), str(order))
        self.assertIn("<PageOrderEntry path: thing.md, variables: {'make_qty': 1, 'make_linktext': 'thing'}",
                      str(order), str(order))
        self.assertIn("<PageOrderEntry path: somethingelse.md, variables: None", str(order), str(order))

    def test_page_order_with_chained_make_link(self):
        #These two pages are step linked in test page 1
        self._dummy_page("# blah", path="something.md")
        md = ("# Blah2\n\n"
              "In this step you will use the [thing1](thing1.md){make, qty:2} you already made\n"
              "Also you need [thing2](thing2.md){make, qty:1}")
        self._dummy_page(md, path="somethingelse.md")
        self._dummy_page("# thing1\n This is made using a [thing2](thing2.md){make, qty:2}", path="thing1.md")
        self._dummy_page("# thing2", path="thing2.md")
        self._test_page(1, path="path.md")

        if sys.version_info.minor<10:
            self.doc._set_page_order()
            order = self.doc.page_order
        else:
            with self.assertNoLogs(logger='BuildUp', level=logging.WARN):
                self.doc._set_page_order()
                order = self.doc.page_order
        self.assertEqual(order.number_of_paths, 1)
        self.assertEqual(len(order.pagelists[0]), 5, str(order.pagelists[0]))
        self.assertEqual(order.pagelists[0][0], "path.md")
        self.assertEqual(order.pagelists[0][1], "something.md")
        self.assertEqual(order.pagelists[0][2], "thing2.md")
        self.assertEqual(order.pagelists[0][3], "thing1.md")
        self.assertEqual(order.pagelists[0][4], "somethingelse.md")
        self.assertIn("<PageOrderEntry path: path.md, variables: None", str(order), str(order))
        self.assertIn("<PageOrderEntry path: something.md, variables: None", str(order), str(order))
        self.assertIn("<PageOrderEntry path: thing2.md, variables: {'make_qty': 5, 'make_linktext': 'thing2'}",
                      str(order), str(order))
        self.assertIn("<PageOrderEntry path: thing1.md, variables: {'make_qty': 2, 'make_linktext': 'thing1'}",
                      str(order), str(order))
        self.assertIn("<PageOrderEntry path: somethingelse.md, variables: None", str(order), str(order))

    def test_page_order_with_chained_make_link2(self):
        #These two pages are step linked in test page 1
        self._dummy_page("# blah", path="something.md")
        md = ("# Blah2\n\n"
              "In this step you will use the [thing1](thing1.md){make, qty:1} you already made\n"
              "Also you need [thing2](thing2.md){make, qty:2}")
        self._dummy_page(md, path="somethingelse.md")
        self._dummy_page("# thing1", path="thing1.md")
        self._dummy_page("# thing2\n This is made using a [thing1](thing1.md){make, qty:1}", path="thing2.md")
        self._test_page(1, path="path.md")

        if sys.version_info.minor<10:
            self.doc._set_page_order()
            order = self.doc.page_order
        else:
            with self.assertNoLogs(logger='BuildUp', level=logging.WARN):
                self.doc._set_page_order()
                order = self.doc.page_order
        self.assertEqual(order.number_of_paths, 1)
        self.assertEqual(len(order.pagelists[0]), 5, str(order.pagelists[0]))
        self.assertEqual(order.pagelists[0][0], "path.md")
        self.assertEqual(order.pagelists[0][1], "something.md")
        self.assertEqual(order.pagelists[0][2], "thing1.md")
        self.assertEqual(order.pagelists[0][3], "thing2.md")
        self.assertEqual(order.pagelists[0][4], "somethingelse.md")
        self.assertIn("<PageOrderEntry path: path.md, variables: None", str(order), str(order))
        self.assertIn("<PageOrderEntry path: something.md, variables: None", str(order), str(order))
        self.assertIn("<PageOrderEntry path: thing2.md, variables: {'make_qty': 2, 'make_linktext': 'thing2'}",
                      str(order), str(order))
        self.assertIn("<PageOrderEntry path: thing1.md, variables: {'make_qty': 3, 'make_linktext': 'thing1'}",
                      str(order), str(order))
        self.assertIn("<PageOrderEntry path: somethingelse.md, variables: None", str(order), str(order))

    def test_page_order_with_looped_make_links(self):
        #These two pages are step linked in test page 1
        self._dummy_page("# blah", path="something.md")
        md = ("# Blah2\n\n"
              "In this step you will use the [thing1](thing1.md){make, qty:1} you already made\n"
              "Also you need [thing2](thing2.md){make, qty:1}")
        self._dummy_page(md, path="somethingelse.md")
        self._dummy_page("# thing1\n This is made using a [thing2](thing2.md){make, qty:1}", path="thing1.md")
        self._dummy_page("# thing2\n This is made using a [thing1](thing1.md){make, qty:1}", path="thing2.md")
        self._test_page(1, path="path.md")

        with self.assertLogs(logger='BuildUp', level=logging.WARN):
            self.doc._set_page_order()
            order = self.doc.page_order
        self.assertEqual(order.number_of_paths, 1)
        self.assertEqual(len(order.pagelists[0]), 3, str(order.pagelists[0]))
        self.assertEqual(order.pagelists[0][0], "path.md")
        self.assertEqual(order.pagelists[0][1], "something.md")
        self.assertEqual(order.pagelists[0][2], "somethingelse.md")

    def test_make_link_bom(self):
        #These two pages are step linked in test page 1
        self._dummy_page("# blah\nUse a [widget]{qty:1}", path="something.md")
        md = ("# Blah2\n\n"
              "In this step you will use the [thing](thing.md){make, qty:1} you already made\n")
        linking_page = self._dummy_page(md, path="somethingelse.md")
        self._dummy_page("# thingy\nUse a [widget]{qty:1}", path="thing.md")
        indexpage = self._test_page(1, path="path.md")
        self.doc._set_page_order()
        indexpage.count()

        self.assertEqual(len(linking_page.all_parts.used_parts), 1)
        self.assertIn('thing', linking_page.all_parts.used_parts)

        self.assertEqual(len(indexpage.all_parts.used_parts), 1)
        self.assertIn('widget', indexpage.all_parts.used_parts)

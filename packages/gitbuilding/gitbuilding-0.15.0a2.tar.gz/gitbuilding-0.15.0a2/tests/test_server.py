import unittest
import tempfile
import shutil
from time import sleep

from bs4 import BeautifulSoup

from gitbuilding.__main__ import set_handler
from gitbuilding import server, example
from gitbuilding.handler import GBHandler

handler = GBHandler()
set_handler(handler)

JAVASCRIPT_MSG = ("We're sorry but the GitBuilding webapp "
                  "doesn't work without JavaScript enabled. "
                  "Please enable it to continue.")

class TestLiveEditor(unittest.TestCase):

    def setUp(self):
        '''Note. All of these sleep statement peppered through this TestCase
        are due to intermittent errors experienced on the CI that cannot be
        replicated locally. Ideally these will be removed when the the
        source of the intermittent faults is fixed
        '''
        self.dirpath = tempfile.mkdtemp()
        example.output_example_project(self.dirpath)
        self.app =  server.GBServer(handler, editor_only=True, working_dir=self.dirpath)
        self.client = self.app.test_client()


    def tearDown(self):
        shutil.rmtree(self.dirpath)
        del self.app

# Each test is its own class due to issues running the tests on CI

class TestHome(TestLiveEditor):
    def test_home(self):
        # Use the client here
        # Example request to a route returning "hello world" (on a hypothetical app)
        ret = self.client.get("/")
        html = ret.data.decode()
        soup = BeautifulSoup(html, features="html5lib")
        navs = soup.find_all('nav')
        self.assertEqual(len(navs), 1)
        # Note can't search for Li or links inside nav as soup gets very confused by the
        # vue code for the search
        nav_classes = ["not-active", "active"]
        nav_links = []
        for nav_line in soup.find_all('li'):
            if nav_line.get('class') and nav_line.get('class')[0] in nav_classes:
                self.assertNotEqual(nav_line.get('class')[0], "active")
                nav_links.append(nav_line.find_all('a')[0])
        self.assertEqual(len(nav_links), 3)
        text_of_nav_links = [nav_link.get_text().strip() for nav_link in nav_links]
        self.assertIn('Bill of Materials', text_of_nav_links)

class TestRaw(TestLiveEditor):
    def test_raw(self):
        ret = self.client.get("/-/editor/raw")
        self.assertIn('md', ret.json)
        self.assertEqual(example.example_landing(), ret.json['md'])

        ret = self.client.get("/testpage1.md/-/editor/raw")
        self.assertIn('md', ret.json)
        self.assertEqual(example.testpage("Test Page 1"), ret.json['md'])

class TestPartList(TestLiveEditor):
    def test_part_list(self):
        ret = self.client.get("/-/editor/partlist")
        self.assertIn('partlist', ret.json)
        partlist = ret.json['partlist']
        self.assertTrue(len(partlist)>1)
        self.assertIn('name', partlist[0])
        names = [i['name'] for i in partlist]
        self.assertIn('widget', names)
        for part in partlist:
            self.assertFalse(part['onPage'])
        #Then get a page where the parts are on the page itself and check
        # onPage is True
        ret = self.client.get("/testpage1.md/-/editor/partlist")
        partlist = ret.json['partlist']
        self.assertTrue(len(partlist)>1)
        for part in partlist:
            self.assertTrue(part['onPage'])

class TestSave(TestLiveEditor):
    def test_save(self):
        ret = self.client.get("/testpage1.md/-/editor/raw")
        starting_md = ret.json['md']
        replace_md = starting_md.replace('Test', 'Best')
        self.assertNotEqual(starting_md, replace_md)
        ret = self.client.post("/testpage1.md/-/editor/save",
                               json={'md': replace_md,
                                     'uploadedFiles': []})
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.json['saved'], True)
        ret = self.client.get("/testpage1.md/-/editor/raw")

        final_md = ret.json.get('md', None) if ret.json else None
        if final_md != replace_md:
            sleep(1)
            ret = self.client.get("/testpage1.md/-/editor/raw")
            final_md = ret.json['md']
        self.assertEqual(final_md, replace_md)

class TestLiveRender(TestLiveEditor):
    def test_live_render(self):
        ret = self.client.post("/testpage1.md/-/editor/render_markdown",
                               json={'md': '# Yeah\n No',
                                     'page': 'testpage1.md'})
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.json['number'], 0)
        html = ret.json['html']
        soup = BeautifulSoup(html, features="html5lib")
        h1tags = soup.find_all('h1')
        self.assertEqual(len(h1tags), 2)
        self.assertEqual(h1tags[1].get_text(), 'Yeah')

        ret = self.client.post("/testpage1.md/-/editor/render_markdown",
                               json={'md': '# Yeah\n No'})
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.json['number'], 0)
        html = ret.json['html']
        soup = BeautifulSoup(html, features="html5lib")
        h1tags = soup.find_all('h1')
        # No page given, so this is rendered as the landing page and there
        # is only one title and it is overwritten from page.
        self.assertEqual(len(h1tags), 1)
        self.assertEqual(h1tags[0].get_text(), 'Yeah')
        self.assertEqual(h1tags[0].get('class')[0], 'site-title')

class TestNewPage(TestLiveEditor):
    def test_new_page(self):
        ret = self.client.get("/-/new-page/")
        self.assertIn(JAVASCRIPT_MSG, ret.data.decode())

class TestEditor(TestLiveEditor):
    def test_editor(self):
        ret = self.client.get("/-/editor/")
        self.assertIn(JAVASCRIPT_MSG, ret.data.decode())

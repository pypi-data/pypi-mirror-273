import jupyter_lab_notebook_toc_utils
from unittest import TestCase
import os


class test_jupyter_lab_toc_utils(TestCase):
    def test__notebook_1__success(self):
        tests_dir = os.path.dirname(os.path.abspath(__file__))
        notebooks_dir = os.path.join(tests_dir, "dummy_notebooks")
        notebook_path = os.path.join(notebooks_dir, "dummy_notebook_1.ipynb")
        toc_str = jupyter_lab_notebook_toc_utils.generate_toc(notebook_path)
        expected_toc_str = """**Table of Contents**<br/>
&nbsp;&nbsp;&nbsp;&nbsp;- [Item 1](#Item-1)<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- [Sub Item 1](#Sub-Item-1)<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- [Sub Sub Item 1](#Sub-Sub-Item-1)"""
        self.assertEqual(expected_toc_str.split("\n"), toc_str.split(os.linesep))
    
    def test__notebook_2__success(self):
        tests_dir = os.path.dirname(os.path.abspath(__file__))
        notebooks_dir = os.path.join(tests_dir, "dummy_notebooks")
        notebook_path = os.path.join(notebooks_dir, "dummy_notebook_1.ipynb")
        toc_str = jupyter_lab_notebook_toc_utils.generate_toc(notebook_path)
        expected_toc_str = """**Table of Contents**<br/>
&nbsp;&nbsp;&nbsp;&nbsp;- [Item 1](#Item-1)<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- [Sub Item 1](#Sub-Item-1)<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- [Sub Sub Item 1](#Sub-Sub-Item-1)"""
        self.assertEqual(expected_toc_str.split("\n"), toc_str.split(os.linesep))
    
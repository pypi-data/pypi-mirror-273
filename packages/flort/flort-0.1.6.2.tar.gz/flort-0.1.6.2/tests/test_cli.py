import pytest
from unittest.mock import patch, mock_open
from pathlib import Path
import os

# Ensure the project root is in the sys.path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flort.cli import clean_content, generate_tree, list_files

def test_clean_content():
    test_data = "line 1\n\nline 2\n\n\nline 3\n"
    expected_result = "line 1\nline 2\nline 3"
    with patch("builtins.open", mock_open(read_data=test_data)):
        assert clean_content("dummy_path") == expected_result

def test_generate_tree(tmp_path):
    d1 = tmp_path / "subdir1"
    d1.mkdir()
    (d1 / "file1.txt").write_text("content")
    (d1 / "file2.py").write_text("content")
    
    d2 = tmp_path / "subdir2"
    d2.mkdir()
    (d2 / "file3.txt").write_text("content")
    
    expected_result = (
        f"|-- {d1.name}/\n"
        f"|   |-- file2.py\n"
        f"|   |-- file1.txt\n"
        f"|-- {d2.name}/\n"
        f"|   |-- file3.txt\n"
    )
    assert generate_tree([d1, d2], extensions=['.txt', '.py']) == expected_result

def test_list_files(tmp_path):
    d1 = tmp_path / "subdir1"
    d1.mkdir()
    (d1 / "file1.txt").write_text("content")
    (d1 / "file2.py").write_text("content")
    
    d2 = tmp_path / "subdir2"
    d2.mkdir()
    (d2 / "file3.txt").write_text("content")
    
    expected_result = (
        f"Path: {d1 / 'file2.py'}\nFile: file2.py\n-------\ncontent\n"
        f"Path: {d1 / 'file1.txt'}\nFile: file1.txt\n-------\ncontent\n"
        f"Path: {d2 / 'file3.txt'}\nFile: file3.txt\n-------\ncontent"
    )
    assert list_files([d1, d2], extensions=['.txt', '.py']) == expected_result

def test_list_files_with_compress(tmp_path):
    d1 = tmp_path / "subdir1"
    d1.mkdir()
    (d1 / "file1.txt").write_text("line 1\n\nline 2\n\n\nline 3\n")
    
    expected_result = (
        f"Path: {d1 / 'file1.txt'}\nFile: file1.txt\n-------\nline 1\nline 2\nline 3"
    )
    assert list_files([d1], compress=True, extensions=['.txt']) == expected_result

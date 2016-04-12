﻿# coding: utf-8
from conftest import TOOL_FOLDER
from crosscompute.tests import run
from string import digits, letters
import re


def test_capture_standard_output():
    standard_output = run(TOOL_FOLDER, 'count-characters', {
        'phrase': letters + digits})[0]
    assert '62' in standard_output


def test_print_unicode():
    standard_output = run(TOOL_FOLDER, 'print-unicode')[0]
    assert 'standard_outputs.a = клубника' in standard_output
    assert 'standard_errors.b = малина' in standard_output

def test_accept_script_filename_with_spaces():
    standard_output = run(
        TOOL_FOLDER, 'accept-script-filename-with-spaces-in-single-quotes')[0]
    assert 'abc = xyz' in standard_output
    standard_output = run(
        TOOL_FOLDER, 'accept-script-filename-with-spaces-in-double-quotes')[0]
    assert 'abc = xyz' in standard_output

def test_correct_target_folder_path():
    standard_output = run(
        TOOL_FOLDER, 'show-correct-target_folder')[0]
    target_folder = re.search(r'\ntarget_folder\s=\s(.+?)\r',standard_output).group(1)
    """
    # how it is now, the test will pass
    check = 'standard_outputs.target folder = ' + 'tmpshow-correct-target_folderresults'
    """
    # should either this
    check = 'standard_outputs.target folder = ' + target_folder
    # or this
    check = 'standard_outputs.target folder = ' + target_folder + '/tmpshow-correct-target_folderresults'
    #assert re.match(r'target folder = tmpshow-correct-target_folderresults',standard_output) is not None  
    assert check in standard_output
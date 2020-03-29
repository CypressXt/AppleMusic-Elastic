#!/usr/bin/env python

import applemusic_to_es


def test_github_template_download():
    assert applemusic_to_es.get_template() != ""


def test_github_visualization_download():
    assert applemusic_to_es.get_visualizations() != ""

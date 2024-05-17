# This file is part of fm-actor, a library for interacting with fm-data files:
# https://gitlab.com/sosy-lab/software/fm-actor
#
# SPDX-FileCopyrightText: 2024 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: MIT

import shutil
from pathlib import Path

import requests
import yaml
from fm_tools.download import DownloadDelegate
from fm_tools.fmdata import FmData

YAML = """
name: Goblint
input_languages:
  - C
project_url: https://goblint.in.tum.de/
repository_url: https://github.com/goblint/analyzer
spdx_license_identifier: MIT
benchexec_toolinfo_module: "https://gitlab.com/sosy-lab/software/benchexec/-/raw/main/benchexec/tools/goblint.py"
fmtools_format_version: "2.0"
fmtools_entry_maintainers:
  - sim642

maintainers:
  - name: Simmo Saan
    institution: University of Tartu
    country: Estonia
    url: https://sim642.eu/
  - name: Michael Schwarz
    institution: Technische Universität München
    country: Germany
    url: https://www.cs.cit.tum.de/en/pl/personen/michael-schwarz/

versions:
  - version: "svcomp24"
    doi: 10.5281/zenodo.10202867
    benchexec_toolinfo_options: ["--conf", "conf/svcomp24.json"]
    required_ubuntu_packages: []

"""


def teardown_module():
    target = Path(__file__).parent / "output"
    if target.exists():
        shutil.rmtree(target)


def test_download_with_httpx():

    config = yaml.safe_load(YAML)
    fm_data = FmData(config, "svcomp24")

    target = Path(__file__).parent / "output" / "goblint-svcomp24"

    fm_data.download_and_install_into(target)


def test_download_with_requests():

    config = yaml.safe_load(YAML)
    fm_data = FmData(config, "svcomp24")

    target = Path(__file__).parent / "output" / "goblint-svcomp24"

    fm_data.download_and_install_into(
        target, delegate=DownloadDelegate(requests.Session())
    )


if __name__ == "__main__":
    test_download_with_httpx()

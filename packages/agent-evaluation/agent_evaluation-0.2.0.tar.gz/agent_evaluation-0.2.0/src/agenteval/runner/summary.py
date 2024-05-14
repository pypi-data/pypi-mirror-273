# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import logging
import os

from agenteval import jinja_env
from agenteval.test import Test
from agenteval.test_result import TestResult

logger = logging.getLogger(__name__)

_TEMPLATE_ROOT = "summary"
_TEMPLATE_FILE_NAME = "agenteval_summary.md.jinja"


def create_markdown_summary(
    work_dir: str, tests: list[Test], test_results: list[TestResult], verbose: bool
):
    template = jinja_env.get_template(os.path.join(_TEMPLATE_ROOT, _TEMPLATE_FILE_NAME))

    summary_path = os.path.join(work_dir, os.path.splitext(_TEMPLATE_FILE_NAME)[0])

    rendered = template.render(tests=tests, results=test_results, zip=zip)

    with open(summary_path, "w+") as f:
        f.write(rendered)

    if verbose:
        logger.info(f"Summary available at {summary_path}")

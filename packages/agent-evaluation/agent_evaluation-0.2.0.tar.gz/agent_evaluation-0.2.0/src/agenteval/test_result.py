# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from pydantic import BaseModel

from agenteval.conversation import Conversation


class TestResult(BaseModel, arbitrary_types_allowed=True):
    """The result of a test.

    Attributes:
        test_name: Name of the test.
        result: Description of the test result.
        reasoning: The rationale for the test result.
        success: `True` if the test passed, otherwise `False`.
        conversation: Captures the interaction between a user and an agent.
    """

    # do not collect as a test
    __test__ = False

    test_name: str
    result: str
    reasoning: str
    success: bool
    conversation: Conversation

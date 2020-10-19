# Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
from botocore.session import Session
import pytest


def _all_services():
    session = Session()
    service_names = session.get_available_services()
    for service_name in service_names:
        yield session.get_service_model(service_name)


def _all_error_shapes():
    for service_model in _all_services():
        for shape in service_model.error_shapes:
            yield shape


def _all_operations():
    for service_model in _all_services():
        for operation_name in service_model.operation_names:
            yield service_model.operation_model(operation_name)


def _assert_not_shadowed(key, shape):
    if not shape:
        return
    msg = (
        'Found shape "%s" that shadows the botocore response key "%s"'
    )
    assert key not in shape.members, msg % (shape.name, key)



@pytest.mark.parametrize('operation_model', _all_operations())
def test_response_metadata_is_not_shadowed(operation_model):
    shape = operation_model.output_shape
    _assert_not_shadowed('ResponseMetadata', shape)


@pytest.mark.parametrize('shape', _all_error_shapes())
def test_exceptions_do_not_shadow(shape):
    _assert_not_shadowed('ResponseMetadata', shape)
    _assert_not_shadowed('Error', shape)

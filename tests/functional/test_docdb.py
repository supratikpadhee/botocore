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
from tests import BaseSessionTest, ClientHTTPStubber


class TestDocDBPresignUrlInjection(BaseSessionTest):

    def setUp(self):
        super(TestDocDBPresignUrlInjection, self).setUp()
        self.client = self.session.create_client('docdb', 'us-west-2')
        self.http_stubber = ClientHTTPStubber(self.client)

    def assert_presigned_url_injected_in_request(self, body):
        assert 'PreSignedUrl' in body
        assert 'SourceRegion' not in body

    def test_copy_db_cluster_snapshot(self):
        params = {
            'SourceDBClusterSnapshotIdentifier': 'source-db',
            'TargetDBClusterSnapshotIdentifier': 'target-db',
            'SourceRegion': 'us-east-1'
        }
        response_body = (
            b'<CopyDBClusterSnapshotResponse>'
            b'<CopyDBClusterSnapshotResult>'
            b'</CopyDBClusterSnapshotResult>'
            b'</CopyDBClusterSnapshotResponse>'
        )
        self.http_stubber.add_response(body=response_body)
        with self.http_stubber:
            self.client.copy_db_cluster_snapshot(**params)
            sent_request = self.http_stubber.requests[0]
            self.assert_presigned_url_injected_in_request(sent_request.body)

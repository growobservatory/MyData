import pytest
from mydata.api_cloud import ApiCloud

def test_credentials():
  service = ApiCloud('api-key', 'api-secret')
  service.credentials('test-username')

  assert service._credentials == {
    'client_id': 'api-key', 
    'client_secret': 'api-secret',
    'username': 'test-username'
  }
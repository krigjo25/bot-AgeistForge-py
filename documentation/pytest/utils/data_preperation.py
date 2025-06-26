
from unittest.mock import patch, Mock
class TestCase(object):


    def _data_prepearation(self, target:str, status_code:int = 200, message:str = 'OK'):
        """Prepare data for testing."""
        with patch(target) as mock_data:
            mock_data.return_value = Mock(status_code=200, json=lambda: {'message':message, 'status':status_code})      # type: ignore
            return mock_data
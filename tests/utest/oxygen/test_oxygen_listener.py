from unittest import TestCase
from unittest.mock import Mock, patch

from oxygen import listener

class OxygenListenerBasicTests(TestCase):
    def setUp(self):
        self.listener = listener()

    def test_listener_api_version_is_not_changed_accidentally(self):
        self.assertEqual(self.listener.ROBOT_LISTENER_API_VERSION, 2)

    def mock_lib_instance(self, mock_builtin, return_value):
        m_builtin = Mock()
        m_get_context = Mock()
        m_builtin._get_context.return_value = m_get_context
        m_get_context.namespace.get_library_instance.return_value = \
            return_value
        mock_builtin.return_value = m_builtin
        return m_builtin

    @patch('oxygen.oxygen.BuiltIn')
    def test_end_test_when_library_was_not_used(self, mock_builtin):
        m = self.mock_lib_instance(mock_builtin, None)

        self.listener.end_test('foo', {})

        m._get_context().namespace.get_library_instance.assert_called_once_with('oxygen.OxygenLibrary')
        self.assertEqual(self.listener.run_time_data, {})

    @patch('oxygen.oxygen.BuiltIn')
    def test_end_test_when_library_was_used(self, mock_builtin):
        o = lambda: None
        o.data = 'I do not have a solution, but I do admire the problem'
        m = self.mock_lib_instance(mock_builtin, o)

        self.listener.end_test('oxygen.OxygenLibrary', {'longname': 'hello'})

        m._get_context().namespace.get_library_instance.assert_called_once_with('oxygen.OxygenLibrary')
        self.assertEqual(self.listener.run_time_data,
                         {'hello': ('I do not have a solution, but I do '
                                    'admire the problem')})

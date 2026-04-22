import tempfile
import unittest
from pathlib import Path

from assistant import PersonalAssistant


class AssistantTests(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tmp_dir.name) / "data.json"
        self.assistant = PersonalAssistant(str(self.db_path))

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_add_and_list_task(self):
        msg = self.assistant.handle("add task Buy milk")
        self.assertIn("Added task #1", msg)
        tasks = self.assistant.handle("list tasks")
        self.assertIn("Buy milk", tasks)

    def test_complete_task(self):
        self.assistant.handle("add task Buy milk")
        done = self.assistant.handle("complete task 1")
        self.assertEqual("Completed task #1.", done)

    def test_add_and_search_note(self):
        self.assistant.handle("add note Prepare for passport renewal")
        result = self.assistant.handle("search notes passport")
        self.assertIn("passport renewal", result)

    def test_daily_briefing(self):
        self.assistant.handle("add task One")
        self.assistant.handle("add task Two")
        self.assistant.handle("complete task 1")
        briefing = self.assistant.handle("briefing")
        self.assertIn("Pending tasks: 1", briefing)


if __name__ == "__main__":
    unittest.main()

import unittest
from pathlib import Path
from common.utils.nsfw_detector import nsfw_detect


class TestNSFWDetect(unittest.TestCase):
    def test_detect(self):
        img_path = Path(__file__).parent / "nsfw.jpg"
        detect_result = nsfw_detect(img_path)
        self.assertTrue(detect_result)


if __name__ == '__main__':
    unittest.main()

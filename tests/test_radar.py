import unittest
from scripts.radar_engine import generate_briefing

class TestRadarEngine(unittest.TestCase):
    def test_briefing_generation(self):
        items = [{
            "title": "Meaningful Human Control in Algorithmic Targeting",
            "url": "https://arxiv.org/abs/2601.12345",
            "summary": "This paper analyzes lethal autonomous weapons systems under IHL.",
            "date": "2026-10-22"
        }]
        md, date_str = generate_briefing(items)
        self.assertIn("Global LAWS & Defense AI Regulatory Radar", md)
        self.assertIn("Meaningful Human Control in Algorithmic Targeting", md)
        self.assertIn("https://aviperera.com", md)
        self.assertTrue(len(date_str) == 10)

if __name__ == "__main__":
    unittest.main()

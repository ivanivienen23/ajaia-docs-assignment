import json, os, unittest
class DeliveryTest(unittest.TestCase):
 def test_assets(self):
  self.assertTrue(os.path.exists("app.py")); self.assertTrue(os.path.exists("static/index.html")); self.assertTrue(os.path.exists("README.md"))
 def test_store_shape(self):
  if os.path.exists("data.json"):
   d=json.load(open("data.json")); self.assertIn("documents",d); self.assertIn("shares",d)
if __name__=="__main__": unittest.main()

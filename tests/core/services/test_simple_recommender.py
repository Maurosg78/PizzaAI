import unittest

from src.core.services.simple_recommender import SimpleRecommender


class TestSimpleRecommender(unittest.TestCase):
    def setUp(self):
        self.api_key = "Rntzc9HDaefGgZL0w3Sid120qfk4kdJD4YZuicE4"
        self.recommender = SimpleRecommender(self.api_key)

    def test_search_foods(self):
        """Prueba la búsqueda de alimentos."""
        foods = self.recommender.search_foods("tomato")
        self.assertIsInstance(foods, list)
        self.assertGreater(len(foods), 0)
        self.assertIn("description", foods[0])

    def test_get_food_details(self):
        """Prueba la obtención de detalles de un alimento."""
        # Primero buscar un alimento para obtener su ID
        foods = self.recommender.search_foods("tomato")
        if foods:
            food_id = foods[0]["fdcId"]
            details = self.recommender.get_food_details(food_id)
            self.assertIsNotNone(details)
            self.assertIn("foodNutrients", details)

    def test_get_recommendations(self):
        """Prueba la generación de recomendaciones."""
        recommendations = self.recommender.get_recommendations("tomato")
        self.assertIsInstance(recommendations, list)
        if recommendations:
            self.assertIn("description", recommendations[0])
            self.assertIn("nutrients", recommendations[0])


if __name__ == "__main__":
    unittest.main()

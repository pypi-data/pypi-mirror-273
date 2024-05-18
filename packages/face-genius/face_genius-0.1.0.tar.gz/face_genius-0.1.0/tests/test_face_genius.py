import unittest
from face_genius import load_image, get_face_encodings, compare_faces


class TestFaceGenius(unittest.TestCase):

    def test_face_recognition(self):
        image = load_image("test_image.jpg")

        encodings = get_face_encodings(image)

        self.assertEqual(len(encodings), 1)

        result = compare_faces(encodings, encodings[0])
        self.assertTrue(result[0])


if __name__ == "__main__":
    unittest.main()

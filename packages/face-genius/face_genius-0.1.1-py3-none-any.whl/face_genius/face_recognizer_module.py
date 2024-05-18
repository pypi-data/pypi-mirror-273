import face_recognition


def load_image(file_path):
    return face_recognition.load_image_file(file_path)


def get_face_encodings(image):
    return face_recognition.face_encodings(image)


def compare_faces(known_face_encodings, face_encoding_to_check, tolerance=0.6):
    return face_recognition.compare_faces(known_face_encodings, face_encoding_to_check, tolerance)

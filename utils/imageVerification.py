from google.cloud import vision
from google.cloud.vision_v1 import types
from google.cloud.vision_v1 import Image as VisionImage
import json
from google.protobuf.json_format import MessageToDict


def extract_text_from_image_file(image_instance):
    """
    Extracts text from an image file using Google Cloud Vision API.

    Args:
        file_path (str): The path to the image file.

    Returns:
        list of dict: Extracted text and bounding polygon for each detected text entity.
    """
    # Initialize the Google Cloud Vision client
    client = vision.ImageAnnotatorClient()

    content = image_instance.file.read()

    # Construct an Image object with the image data
    image = VisionImage(content=content)

    # Prepare the request for multiple features, including safe search
    features = [
        {"type_": vision.Feature.Type.LABEL_DETECTION},
        {"type_": vision.Feature.Type.FACE_DETECTION},
        {"type_": vision.Feature.Type.TEXT_DETECTION},
        {"type_": vision.Feature.Type.DOCUMENT_TEXT_DETECTION},
        {"type_": vision.Feature.Type.IMAGE_PROPERTIES},
        {"type_": vision.Feature.Type.CROP_HINTS},
        {"type_": vision.Feature.Type.WEB_DETECTION},
        {"type_": vision.Feature.Type.OBJECT_LOCALIZATION},
        # Include safe search detection
        {"type_": vision.Feature.Type.SAFE_SEARCH_DETECTION},
    ]

    # Perform the request
    response = client.annotate_image({'image': image, 'features': features})

    serialized_response = serialize_vision_response(response)
    # json_response = json.dumps(serialized_response)

    return serialized_response


def handle_protobuf_value(value):
    """
    Extracts the native Python value from protobuf wrapper types.
    """
    if hasattr(value, 'value'):  # Check if the field is a protobuf wrapper type
        return value.value
    else:
        return value


def serialize_vision_response(response):
    """
    Serializes a Google Cloud Vision API response into a JSON-serializable format.

    Args:
        response: The response object from the Google Cloud Vision API.

    Returns:
        A dictionary containing serialized vision API response.
    """
    def serialize_vertices(vertices):
        return [{'x': handle_protobuf_value(vertex.x), 'y': handle_protobuf_value(vertex.y)} for vertex in vertices]

    def serialize_color_info(color_info):
        return {
            'red': handle_protobuf_value(color_info.color.red),
            'green': handle_protobuf_value(color_info.color.green),
            'blue': handle_protobuf_value(color_info.color.blue),
            'alpha': handle_protobuf_value(color_info.color.alpha) if color_info.color.alpha else 0,
            'score': handle_protobuf_value(color_info.score),
            'pixel_fraction': handle_protobuf_value(color_info.pixel_fraction)
        }

    def serialize_web_detection(web_detection):
        return {
            'web_entities': [{'entity_id': entity.entity_id, 'score': handle_protobuf_value(entity.score), 'description': entity.description} for entity in web_detection.web_entities],
            'best_guess_labels': [{'label': label.label} for label in web_detection.best_guess_labels]
        }

    serialized_response = {
        'label_annotations': [
            {
                'description': label.description,
                'score': handle_protobuf_value(label.score),
                'topicality': handle_protobuf_value(label.topicality)
            } for label in response.label_annotations
        ],
        'text_annotations': [
            {
                'locale': text.locale,
                'description': text.description,
            } for text in response.text_annotations
        ],
        'document_text_annotation': {
            'text': response.full_text_annotation.text if response.full_text_annotation else ''
        },
        'image_properties_annotation': {
            'dominant_colors': [serialize_color_info(color) for color in response.image_properties_annotation.dominant_colors.colors]
        },
        'crop_hints_annotation': [
            {
                'confidence': handle_protobuf_value(crop_hint.confidence),
                'importance_fraction': handle_protobuf_value(crop_hint.importance_fraction)
            } for crop_hint in response.crop_hints_annotation.crop_hints
        ],
        'web_detection': serialize_web_detection(response.web_detection),
        'localized_object_annotations': [
            {
                'name': obj.name,
                'score': handle_protobuf_value(obj.score),
            } for obj in response.localized_object_annotations
        ],
        'safe_search_annotation': {
            'adult': handle_protobuf_value(response.safe_search_annotation.adult),
            'spoof': handle_protobuf_value(response.safe_search_annotation.spoof),
            'medical': handle_protobuf_value(response.safe_search_annotation.medical),
            'violence': handle_protobuf_value(response.safe_search_annotation.violence),
            'racy': handle_protobuf_value(response.safe_search_annotation.racy)
        }
    }

    return serialized_response


# old code

# def handle_protobuf_value(value):
#     """
#     Extracts the native Python value from protobuf wrapper types.
#     """
#     if hasattr(value, 'value'):  # Check if the field is a protobuf wrapper type
#         return value.value
#     else:
#         return value

# # Then, wherever you're serializing values that might be FloatValue, use this function:
# # Example: 'score': handle_protobuf_value(color_info.score),


# def serialize_vision_response(response):
#     """
#     Serializes a Google Cloud Vision API response into a JSON-serializable format.

#     Args:
#         response: The response object from the Google Cloud Vision API.

#     Returns:
#         A dictionary containing serialized vision API response.
#     """
#     def serialize_vertices(vertices):
#         return [{'x': handle_protobuf_value(vertex.x), 'y': handle_protobuf_value(vertex.y)} for vertex in vertices]

#     def serialize_color_info(color_info):
#         return {
#             'red': handle_protobuf_value(color_info.color.red),
#             'green': handle_protobuf_value(color_info.color.green),
#             'blue': handle_protobuf_value(color_info.color.blue),
#             'alpha': color_info.color.alpha if color_info.color.alpha else 0,
#             'score': handle_protobuf_value(color_info.score),
#             # 'pixel_fraction': handle_protobuf_value(color_info.pixel_fraction)
#         }

#     def serialize_web_detection(web_detection):
#         return {
#             'web_entities': [{'entity_id': entity.entity_id, 'score': entity.score, 'description': entity.description} for entity in web_detection.web_entities],
#             # 'full_matching_images': [{'url': image.url} for image in web_detection.full_matching_images],
#             # 'pages_with_matching_images': [{'url': page.url, 'page_title': page.page_title} for page in web_detection.pages_with_matching_images],
#             # 'visually_similar_images': [{'url': image.url} for image in web_detection.visually_similar_images],
#             'best_guess_labels': [{'label': label.label} for label in web_detection.best_guess_labels]
#         }

#     serialized_response = {
#         'label_annotations': [
#             {
#                 # 'mid': label.mid,
#                 'description': label.description,
#                 'score': handle_protobuf_value(label.score),
#                 'topicality': label.topicality
#             } for label in response.label_annotations
#         ],
#         # 'face_annotations': [
#         #     {
#         #         # 'bounding_poly': serialize_vertices(face.bounding_poly.vertices),
#         #         # 'fd_bounding_poly': serialize_vertices(face.fd_bounding_poly.vertices),
#         #         'landmarks': [
#         #             {
#         #                 'type': landmark.type_,
#         #                 'position': {'x': landmark.position.x, 'y': landmark.position.y, 'z': landmark.position.z}
#         #             } for landmark in face.landmarks
#         #         ],
#         #         'roll_angle': face.roll_angle,
#         #         'pan_angle': face.pan_angle,
#         #         'tilt_angle': face.tilt_angle,
#         #         'detection_confidence': face.detection_confidence,
#         #         'landmarking_confidence': face.landmarking_confidence,
#         #         'joy_likelihood': face.joy_likelihood,
#         #         'sorrow_likelihood': face.sorrow_likelihood,
#         #         'anger_likelihood': face.anger_likelihood,
#         #         'surprise_likelihood': face.surprise_likelihood,
#         #         'under_exposed_likelihood': face.under_exposed_likelihood,
#         #         'blurred_likelihood': face.blurred_likelihood,
#         #         'headwear_likelihood': face.headwear_likelihood
#         #     } for face in response.face_annotations
#         # ],
#         'text_annotations': [
#             {
#                 'locale': text.locale,
#                 'description': text.description,
#                 # 'bounding_poly': serialize_vertices(text.bounding_poly.vertices)
#             } for text in response.text_annotations
#         ],
#         'document_text_annotation': {
#             'text': response.full_text_annotation.text if response.full_text_annotation else ''
#             # Include further parsing of pages, blocks, paragraphs, etc., as needed.
#         },
#         'image_properties_annotation': {
#             'dominant_colors': [serialize_color_info(color) for color in response.image_properties_annotation.dominant_colors.colors]
#         },
#         'crop_hints_annotation': [
#             {
#                 # 'bounding_poly': serialize_vertices(crop_hint.bounding_poly.vertices),
#                 'confidence': handle_protobuf_value(crop_hint.confidence),
#                 'importance_fraction': crop_hint.importance_fraction
#             } for crop_hint in response.crop_hints_annotation.crop_hints
#         ],
#         'web_detection': serialize_web_detection(response.web_detection),
#         'localized_object_annotations': [
#             {
#                 # 'mid': obj.mid,
#                 'name': obj.name,
#                 'score': handle_protobuf_value(obj.score),
#                 # 'bounding_poly': {'normalized_vertices': [{'x': vertex.x, 'y': vertex.y} for vertex in obj.bounding_poly.normalized_vertices]}
#             } for obj in response.localized_object_annotations
#         ],
#         'safe_search_annotation': {
#             'adult': response.safe_search_annotation.adult,
#             'spoof': response.safe_search_annotation.spoof,
#             'medical': response.safe_search_annotation.medical,
#             'violence': response.safe_search_annotation.violence,
#             'racy': response.safe_search_annotation.racy
#         }
#     }

#     return serialized_response

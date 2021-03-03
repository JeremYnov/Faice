from matplotlib import pyplot
from numpy import asarray
from scipy.spatial.distance import cosine
from keras_vggface.vggface import VGGFace
from keras_vggface.utils import preprocess_input
import numpy as np

# extract a single face from a given photograph
def extract_face(filename, required_size=(224, 224)):
    # load image from file
    image = pyplot.imread(filename)
    
    # Transform our image in array 
    face_array = asarray(image)
    
    # get shape and type
    array_shape = face_array.shape
    array_data_type = face_array.dtype.name
    
    # converting to string
    face_array_str = face_array.tostring()
    # TODO => Push this str in database if the user doesn't exist
    
    # converting back to numpy array
    # TODO => Converting back our str in array
    new_arr = np.frombuffer(face_array_str, dtype=array_data_type).reshape(array_shape)
    # print(new_arr)
    return face_array


# extract faces and calculate face embeddings for a list of photo files
# Transform filenames in path
def get_embeddings(path):
    # extract faces
    faces = [extract_face(path)]  # faces[0] = user wanted to be identified

    #TODO => get all array data from BDD and append to faces
    # for array_data in array_datas:
    #     faces.append(array_data)

    # convert into an array of samples
    samples = asarray(faces, 'float32')

    # prepare the face for the model, e.g. center pixels
    samples = preprocess_input(samples, version=2)

    # create a vggface model
    model = VGGFace(model='resnet50', include_top=False,
                    input_shape=(224, 224, 3), pooling='avg')

    # perform prediction
    yhat = model.predict(samples)

    return yhat


# determine if a candidate face is a match for a known face
def is_match(known_embedding, candidate_embedding, thresh=0.5):
    # calculate distance between embeddings
    score = cosine(known_embedding, candidate_embedding)
    if score <= thresh:
        print('>face is a Match (%.3f <= %.3f)' % (score, thresh))
    else:
        print('>face is NOT a Match (%.3f > %.3f)' % (score, thresh))


# define filenames
filenames = ['Emmanuel_Macron.jpg', 'Emmanuel_Macron2.jpg',
             'Jean_Castex.jpg', 'Jean_Castex2.jpg']

# get embeddings file filenames
embeddings = get_embeddings(filenames)

# define face to verify if known in our database
faceToAnalysis = embeddings[0]

print(embeddings[0])

# verify known photos of sharon
print('Positive Tests')
is_match(embeddings[0], embeddings[1])
is_match(embeddings[0], embeddings[2])

# verify known photos of other people
# print('Negative Tests')
is_match(embeddings[0], embeddings[3])

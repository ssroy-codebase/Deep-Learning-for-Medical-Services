import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

MODEL_PATH_colon = os.path.join(os.getcwd(), 'models', 'colon.h5')
MODEL_PATH_bb = os.path.join(os.getcwd(), 'models', 'brain_binary.h5')
MODEL_PATH_bm = os.path.join(os.getcwd(), 'models', 'brain_multiclass.h5')


def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))
    # Preprocessing the image
    x = image.img_to_array(img) / 255
    # x = np.true_divide(x, 255)
    x = np.expand_dims(x, axis=0)
    # preds = model.predict(x)
    preds = model(x)
    return preds


def make_prediction(type, file_path):
    # print(type,file_path)
    if type == "ColonCancer":
        model = load_model(MODEL_PATH_colon)
        preds = model_predict(file_path, model)  # 'Colon Adenocarcinoma': 0, 'Colon Benign': 1
        result = predict_colon(preds)
        return result

    elif type == "BrainTumorType":
        model = load_model(MODEL_PATH_bm)
        preds = model_predict(file_path, model)  # {'glioma': 0,'meningioma': 1,'notumor': 2,'pituitary': 3}
        # pred_class = preds.argmax(axis=-1)
        pred_class = np.argmax(preds.numpy())
        result = predict_bm(pred_class)
        return result

    elif type == "BrainTumor":
        model = load_model(MODEL_PATH_bb)
        preds = model_predict(file_path, model)  # 'no': 0, 'yes': 1
        result = predict_bb(preds)
        return result


def predict_bb(pred_class):
    if pred_class > 0.5:
        return 'Tumor'
    else:
        return 'No tumor'


def predict_bm(pred_class):
    if pred_class == 0:
        return "Glioma"
    elif pred_class == 1:
        return "Meningioma"
    elif pred_class == 2:
        return "No Tumor"
    elif pred_class== 3:
        return "Pituitary"


def predict_colon(pred_class):
    if pred_class > 0.5:
        return 'Benign'
    else:
        return 'Adenocarcinoma'

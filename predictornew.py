from keras.preprocessing import sequence
from keras.models import load_model
from keras.models import Model
import joblib,sys
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from keras.models import load_model
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel


def TrainData(data):
    seq_line = []
    seq_soure = []

    # Convert the input data to bytes and decode using utf-8 encoding
    data_bytes = data.encode('utf-8')
    lines = data_bytes.decode('utf-8').split("\n")

    for seq in lines:
        seq = seq.strip()
        if len(seq) != 0 and not seq.startswith(">"):
            encode_seq = encode(seq)
            if encode_seq is None:
                return None, [seq]
            seq_line.append(encode_seq)
            seq_soure.append(seq)

    return seq_line, seq_soure



def encode(text):  # encoding

    encoded_text = [ord(char) for char in text]
    return encoded_text

def predict(data:str):
    results = []
    maxlen = 512
    X,seq = TrainData(data)

    if X is None and len(seq)>0:
        results.append(seq[0] + ": There are **ILLEGAL** characters in this sequence!!!")
        return results
    current_dir = sys.path[0]
    print(current_dir)
    print('Loading data...')
    print('Pad sequences (samples x time)')
    X_test = sequence.pad_sequences(X, maxlen=maxlen)
    feat_test=X_test
    base_model=load_model(current_dir + '/models/pretrainsentment/dcnnmodel.h5')
    model_feat = Model(inputs=base_model.input,outputs=base_model.get_layer('my_third_layer').output)
    feat_test=model_feat.predict(feat_test)

    print('X_test shape:', X_test.shape)
    print('Build model...')

    models = [
        'models/pretrainsentment/SVM_modeldataall.model',
        'models/pretrainsentment/BAG_modeldataall.model',
        'models/pretrainsentment/dtree_modeldataall.model',
        # 'models/pretrainsentment/ESEM_modeldataall.model',
        'models/pretrainsentment/GNB_modeldataall.model',
        'models/pretrainsentment/lgb_modeldataall.model',
        'models/pretrainsentment/RF_modeldataall.model',
        'models/pretrainsentment/XGB_modeldataall.model',
        'models/pretrainsentment/lgb_modeldataall.model',
        # 'models/pretrainsentment/KNN_modeldataall.model'
    ]

    y_test_pred_sum = None
    for model in models:
        svm_model=joblib.load(current_dir + '/' +model)
        print("加载成功，开始预测")
        y_test_pred = svm_model.predict(feat_test)
        print("svm", y_test_pred)
        if y_test_pred_sum is not None:
            y_test_pred_sum += y_test_pred
        else:
            y_test_pred_sum = y_test_pred

    print("seq",seq)
    print('X_test pre:', y_test_pred_sum)

    results = []
    for j, res in enumerate(y_test_pred_sum):
        if res >= 4:
            sentiment = "positive"
        else:
            sentiment = "negative"
        results.append(f"{seq[j]} : This comment is {sentiment} sentiment")

    return results


print(predict("我觉得刚刚好一点也不辣 [哈哈]\n"))

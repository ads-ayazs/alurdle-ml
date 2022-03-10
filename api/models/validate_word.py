import awswrangler as wr
import joblib
import os
import pandas as pd
import tempfile

# Constants
S3_BUCKET_ML_PATH="s3://ads-datasets/wordle-ml"
S3_FLD_MODEL="models"
FILENAME_VALIDWORDS_MODEL = "valid-words-model.pkl"
FILENAME_VALIDWORDSOHE_MODEL = "valid-words-ohe.pkl"
WORD_LENGTH = 5

# Helper dict to locate files in s3 ML bucket
_out_dir = {
  S3_FLD_MODEL: {
    'folder': S3_FLD_MODEL,
    'file': {
      'validwords': FILENAME_VALIDWORDS_MODEL,
      'validwords_ohe': FILENAME_VALIDWORDSOHE_MODEL,
    }
  },
}

_letter_cols = [f'l{n}' for n in range(WORD_LENGTH)]

def is_valid_word(try_word=''):
  if try_word is None:
    return False

  tw = str.upper(try_word.strip())
  if len(tw) != WORD_LENGTH:
    return False

  tw_list = [[w for w in tw]]
  df = pd.DataFrame(tw_list, columns=_letter_cols)

  model = _get_model()
  p = _predict_from_classifier(df, model)

  retval = (p[0] == 1)
  return retval

# Predict from a trained classifier
def _predict_from_classifier(X, clf):
  ohe = _get_ohe()
  X_ohe = ohe.transform(X[_letter_cols])

  return clf.predict(X_ohe)


def _get_model():
  global _model

  if _model == None:
    # Load the saved model from s3
    with tempfile.TemporaryFile() as tmp:
      bucket_path = S3_BUCKET_ML_PATH
      fld_format = _out_dir[S3_FLD_MODEL]['folder']
      file_name = _out_dir[S3_FLD_MODEL]['file']['validwords']
      path = os.path.join(bucket_path, fld_format, file_name)

      wr.s3.download(path, tmp)
      tmp.seek(0)
      _model = joblib.load(tmp)
  
  return _model

def _get_ohe():
  global _ohe 

  if _ohe is None:
    # Load the saved model from s3
    with tempfile.TemporaryFile() as tmp:
      bucket_path = S3_BUCKET_ML_PATH
      fld_format = _out_dir[S3_FLD_MODEL]['folder']
      file_name = _out_dir[S3_FLD_MODEL]['file']['validwords_ohe']
      path = os.path.join(bucket_path, fld_format, file_name)

      wr.s3.download(path, tmp)
      tmp.seek(0)
      _ohe = joblib.load(tmp)
  
  return _ohe

_model = None
_ohe = None
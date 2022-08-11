import ramdom
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import Sequential
from tensorflor.keras.layers import Dense,Activation,Dropout
from tensorflow.keras.optimizer import SGD
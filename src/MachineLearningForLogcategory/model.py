# !/usr/bin/env python
# coding: utf-8
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from data import DataSet
import numpy as np
import click

class BaseModel(object):
    def __init__(self):
        pass

class SVC_Model(BaseModel):
    
    def __init__(self, data, category_index, category_names):
        self._data = data
        self._category = category_index
        self._category_names = category_names
        self.text_clf = Pipeline([('vect', CountVectorizer(stop_words='english', token_pattern='\w+', max_df=0.7, min_df=2)),
                         ('tfidf', TfidfTransformer(norm ='l2')),
                         ('clf', SVC(kernel='linear', C=5, class_weight='balanced', probability=True)),
                         ])

    def build(self, module_file_name):
        self.text_clf.fit(self._data, self._category)
        joblib.dump(self.text_clf,  module_file_name)

    def build_with_category_names(self, module_file_name):
        self.text_clf.fit(self._data, np.array(self._category_names)[self._category])
        joblib.dump(self.text_clf,  module_file_name)


@click.command()
@click.option('--train_path', default="./", help='the train resource datas full path.')
@click.option('--model_save_path', default="train.ml", help='the train model save path.')
def build_model(train_path, model_save_path):
    train_datas = DataSet(train_path)
    train_model = SVC_Model(train_datas.data, train_datas.target, train_datas.category_names)
    train_model.build_with_category_names(model_save_path)


if __name__ == "__main__":
    build_model()
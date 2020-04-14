from __future__ import print_function

import os
import sys

import numpy as np
import tensorflow as tf

from modl.cnn_model import TCNNConfig, TextCNN, process_str

save_dir = './modl/checkpoints/'
save_path = os.path.join(save_dir, 'best_validation')  # 最佳验证结果保存路径

class QuestionClassify():
    def __init__(self):
        print('Loading cnn config and model')
        self.config = TCNNConfig()
        self.model = TextCNN(self.config)
        self.words, self.word_to_id = self.read_vocab('./modl/vocab.txt')
        self.config.vocab_size = len(self.words)
        cfg = tf.ConfigProto()
        cfg.gpu_options.allow_growth = True
        self.session = tf.Session(config=cfg)
        self.session.run(tf.global_variables_initializer())
        print('Loading checkpoints')
        self.saver = tf.train.Saver()
        self.saver.restore(sess=self.session, save_path=save_path)  # 读取保存的模型
    
    def read_vocab(self, vocab_dir):
        """读取词汇表"""
        with open(vocab_dir,'r',encoding='utf8') as fp:
            # 如果是py2 则每个值都转化为unicode
            words = [_.strip() for _ in fp.readlines()]
            word_to_id = dict(zip(words, range(len(words))))
        return words, word_to_id

    def get_question_type( self, question ):
        if question[-1]=='？' or question[-1]=='?':#去掉问号
            question = question[:-1]

        if len(question)>20:
            print('这个问题太长了，我搞不懂！')
            return -1

        x_test = process_str( question, self.word_to_id, self.config.seq_length)
        return self._predict( x_test )

    def _predict( self, x_test ):
        #完成预测
        feed_dict = {
            self.model.input_x: x_test,
            self.model.keep_prob: 1.0
        }
        y_pred_cls = np.zeros(1, dtype=np.int32)  # 保存预测结果
        y_pred_cls[0] = self.session.run(self.model.y_pred_cls, feed_dict=feed_dict)
        return y_pred_cls[0]
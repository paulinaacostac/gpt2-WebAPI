# -*- coding: utf-8 -*-

import json
import os
import numpy as np
import tensorflow.compat.v1 as tf

from src import model, sample, encoder
from flask import Flask
from flask import request, jsonify
import time

######model

def interact_model(
    model_name='run1',
    seed=None,
    nsamples=1,
    batch_size=1,
    length=None,
    temperature=1,
    top_k=0, 
    top_p=1,
    models_dir='checkpoint',
):
   
    models_dir = os.path.expanduser(os.path.expandvars(models_dir))
    if batch_size is None:
        batch_size = 1
    assert nsamples % batch_size == 0

    enc = encoder.get_encoder(model_name, models_dir)
    hparams = model.default_hparams()
    with open(os.path.join(models_dir, model_name, 'hparams.json')) as f:
        hparams.override_from_dict(json.load(f))

    if length is None:
        length = hparams.n_ctx // 2
    elif length > hparams.n_ctx:
        raise ValueError("Can't get samples longer than window size: %s" % hparams.n_ctx)

    with tf.Session(graph=tf.Graph()) as sess:
        context = tf.placeholder(tf.int32, [batch_size, None])
        np.random.seed(seed)
        tf.set_random_seed(seed)
        output = sample.sample_sequence(
            hparams=hparams, length=length,
            context=context,
            batch_size=batch_size,
            temperature=temperature, top_k=top_k, top_p=top_p
        )

        saver = tf.train.Saver()
        ckpt = tf.train.latest_checkpoint(os.path.join(models_dir, "run1"))
        saver.restore(sess, ckpt)
        yield sess, context, output, enc
        
def output_something(bio, sess, context, output, enc):
    raw_text = bio#input("Model prompt >>> ")
    
    
    context_tokens = enc.encode(raw_text)
    generated = 0
    
    out = sess.run(output, feed_dict={
        context: [context_tokens for _ in range(1)]
    })[:, len(context_tokens):] #Get samples
        
            
    text = enc.decode(out[0]) #decodes samples
    
    print(text)
    return text





########API
gen = interact_model()
sess, context, output, enc = next(gen)
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def welcome():
    start_time = time.time()
    bio  = request.args.get('bio')
    
    res = output_something(bio, sess, context, output, enc)
    sentences = res.split("\n")[:3]
    print("----------------------------------------------------------- %s seconds ----------------------------------------------" % (time.time() - start_time))
    return jsonify(sentences=sentences)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)
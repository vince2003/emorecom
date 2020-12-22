"""
train.py - training module
"""

# import dependencies
import os
import glob
import argparse
import tensorflow as tf

from tensorflow.keras import optimizers, callbacks, losses, metrics

# import local packages
from emorecom.data import Dataset
from emorecom.model import create_model

def train(args):
	# path variables
	LOG_DIR = os.path.join(os.getcwd(), 'logs')
	CHECKPOINT_PATH = os.path.join(os.getcwd(), 'checkpoints')

	# initialize experiment-name
	experiment = 'model-0'

	# initialize train dataset
	train_path = args.data_path
	
	# initialize train-dataset
	print("Creating Data Loading")
	dataset = Dataset(
		data_path = train_path,
		batch_size = 4)
	train_data = dataset(training = True)

	# test train-dataset
	#sample = next(iter(train_data))
	#print(sample)

	# initialize model
	print("Initialize and compile model")
	MODEL_CONFIGS= {
		'img_shape' : [224, 224, 3],
		'text_shape' : [50],
		'vocab_size' : 100,
		'vocabs' : None,
		'max_len' : None,
		'embed_dim' : 100,
		'pretrained_embed' : None}
	model = create_model(configs = MODEL_CONFIGS)
	print(model.summary())

	# set hyperparameters
	# compile model
	LR = 0.0001
	OPTIMIZER = optimizers.Adam(learning_rate = LR)
	LOSS = losses.CategoricalCrossentropy(from_logits = True)
	METRICS = [metrics.CategoricalAccuracy()]
	#model.compile(optimizer = OPTIMZER, loss = LOSS, metrics = METRICS)

	# set hyperparameters
	print("Start training")
	LOG_DIR = os.path.join(LOG_DIR, experiment)
	CHECKPOINT_PATH = os.path.join(CHECKPOINT_PATH, experiment)
	CALLBACKS = [
		callbacks.TensorBoard(log_dir = LOG_DIR, write_images = True),
		callbacks.ModelCheckpoint(filepath = CHECKPOINT_PATH, monitor = 'val_loss', verbose = 1, save_best_only = True, mode = 'min')]
	EPOCHS = 50
	STEPS_PER_EPOCH = None
	#model.fit(train_data, verbose = 1, callbacks = CALLBACKS, epochs = EPOCHS,
	#	steps_per_epoch = STEPS_PER_EPOCH)

	# save model
	#model_path = experiment
	#tf.saved_model.save(model, model_path)

if __name__ == '__main__':
	parser = argparse.ArgumentParser('Argument Parser')
	parser.add_argument('--data-path',
		type = str, default = os.path.join(os.getcwd(), 'dataset', 'train.tfrecords'))
	train(parser.parse_args())

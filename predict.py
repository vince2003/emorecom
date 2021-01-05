"""
predict.py - prediction module
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

# get directory path
DIR_PATH = os.getcwd()

def main(args):

	"""------parser-arugments------"""
	# initialize dataset
	assert args.train_data
	TRAIN_DATA = os.path.join(DIR_PATH, args.train_data)
	if args.test_data:
		TEST_DATA = os.path.join(DIR_PATH, args.test_data)
	
	# initialize train-dataset
	print("Creating Data Loading")
	VOCABS = os.path.join(DIR_PATH, args.vocabs)
	dataset = Dataset(data = TRAIN_DATA, vocabs = VOCABS, image_size = [args.image_height, args.image_width],
		text_len = args.text_len, batch_size = args.batch_size)
	train_data = dataset(training = True)

	# test train-dataset
	#images, transcripts, labels = next(iter(train_data))
	#print(labels)
	#print(images.shape, transcripts.shape, labels.shape)
	for sample in train_data.take(1):
		features, labels = sample
		print(features['image'].shape, features['transcripts'].shape, labels)

	# initialize model
	print("Initialize and compile model")
	MODEL_CONFIGS= {'img_shape' : [args.image_height, args.image_width, 3],
		'text_len' : args.text_len,
		'vocabs' : VOCABS,
		'vocab_size' : args.vocab_size,
		'embed_dim' : args.embedding_dim,
		'pretrained_embed' : os.path.join(DIR_PATH, args.pretrained_embedding),
		'num_class' : args.num_class}
	model = create_model(configs = MODEL_CONFIGS)
	print(model.summary())

	# set hyperparameters
	OPTIMIZER = optimizers.Adam(learning_rate = args.learning_rate)
	LOSS = losses.BinaryCrossentropy(from_logits = False)
	METRICS = [metrics.BinaryAccuracy(),
		metrics.Precision(),
		metrics.Recall(),
		metrics.AUC(multi_label = True, thresholds = [0.5])]

	# compile model
	model.compile(optimizer = OPTIMIZER, loss = LOSS, metrics = METRICS)

	# make predictions

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	
	# add arguments
	parser.add_argument('--experiment-name', type = str, default = 'model')
	parser.add_argument('--num-class', type = int, default = 8)
	parser.add_argument('--text-len', type = int, default = 128)
	parser.add_argument('--image-height', type = int, default = 224)
	parser.add_argument('--image-width', type = int, default = 224)
	parser.add_argument('--embedding-dim', default = None) 
	parser.add_argument('--batch-size', type = int, default = 1)
	parser.add_argument('--vocab-size', default = None)
	parser.add_argument('--vocabs', type = str, default = 'dataset/vocabs.txt')
	parser.add_argument('--test-data', type = str, default = 'dataset/test.tfrecords')
	parser.add_argument('--pretrained-embedding', type = str, default = 'glove.twitter.27B/glove.twitter.27B.100d.txt')
	parser.add_argument('--saved-models', type = str, default = 'saved_models')
	main(parser.parse_args())
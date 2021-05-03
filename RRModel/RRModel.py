import time
import numpy as np
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.models.callbacks import CallbackAny2Vec
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import data_utils


class EpochLogger(CallbackAny2Vec):
    """Callback functions to log information about training"""

    def __init__(self):
        self.epoch = 0
        self.start_time = time.time()
        self.curr_time = time.time()

    def on_epoch_begin(self, model):
        # self.curr_time = time.time()
        # print("Epoch #{} start {}".format(self.epoch,round(self.curr_time - self.start_time,3)))
        return

    def on_epoch_end(self, model):
        self.curr_time = time.time()
        print("Epoch #{} end at {}sec with current loss {}".format(
            self.epoch,
            round(self.curr_time - self.start_time, 3),
            'NaN'  # model.get_latest_training_loss()
        ))
        self.epoch += 1


class RRModel:
    """ Doc2Vec model wrapper """

    def __init__(self, load_from = None):

        if load_from:
            try:
                self.model = Doc2Vec.load(load_from)

            except:
                print('Failed to load model from', str(load_from))

        else:
            self.model = Doc2Vec(dm = 1, workers = 4, compute_loss = True, max_vocab_size = None)
        self.epoch_logger = EpochLogger()

    def set_data(self, paperdf):
        """ sets class names for training data, creates TaggedDocuments """
        self.paperdf = paperdf
        abstracts_cleaned = list(map(lambda abstract: abstract.split(' '), paperdf['abstract']))
        self.tagged_docs = [TaggedDocument(words = doc, tags = [doi])
                            for doc, doi in zip(abstracts_cleaned, paperdf['doi'])]

    def _get_tagged_doc(self, doi):
        """ Given a doi, returns the corresponding TaggedDocument object. """

        return self.tagged_docs[list(map(lambda x: x.tags[0], self.tagged_docs)).index(doi)]

    def train(self,
              max_epochs = 10,  # number of max possible training iterations
              min_count = 5,  # min frequency of usage to enter vocab
              vec_size = 100,  # size of feature vectors
              max_alpha = 0.025,  # starting learning rate
              min_alpha = 0.00025,  # lowest learning rate
              save_name = None):
        """ Trains model on corpus of tagged_docs. If a value is passed to save_name, the model will be saved."""

        if not self.tagged_docs and not (self.paperdf and self.authordf):
            print('no data to train.')
            return

        self.model.epochs = max_epochs
        self.model.vocabulary.min_count = min_count
        self.model.vector_size = vec_size
        self.model.alpha = max_alpha
        self.model.min_alpha = min_alpha

        print('Training model.')
        print('Building Vocabulary.')
        self.model.build_vocab(self.tagged_docs)

        print('Training for', max_epochs, 'epochs.')
        self.epoch_logger = EpochLogger()
        self.model.train(self.tagged_docs, total_examples = self.model.corpus_count,
                         epochs = self.model.epochs, callbacks = [self.epoch_logger])
        print("Finished in {} seconds.".format(round(time.time() - self.epoch_logger.start_time, 3)))

        if save_name:
            filename = str(save_name) + '.model'
            self.model.save(filename)
            print("Model Saved as", filename)

        # self._compute_util_data()

    def _compute_util_data(self):
        """ Computes various data for other analysis (PCA, kmeans, etc.) """

        print("Computing PCA of document vectors.")
        self.pca = PCA(n_components = 3)

        print("Computing document clusters in PCA basis.")
        inferred_vecs = np.array([self.model.infer_vector(doc.words) for doc in self.tagged_docs])
        self.pca_reduced_vecs = self.pca.fit_transform(inferred_vecs)
        n_clusters = 25  # TODO find way to determine approx cluster size
        self.kmeans = KMeans(init = 'k-means++', n_clusters = n_clusters, random_state = 0)
        self.kmeans_preds = self.kmeans.fit_predict(self.pca_reduced_vecs)

    def embed_abstract(self, abstract_string):
        """ Computes and returns the embedded vector for abstract_string """

        cleaned_abstract = data_utils.clean_abstract(abstract_string).split(' ')
        return self.model.infer_vector(cleaned_abstract)


from brummlearn.glm import GeneralizedLinearSparseModel
import climin
from scipy.sparse import csr_matrix
import climin.stops
import numpy as np
import time
import os

class LogisticTrainer(object):

    def __init__(self, fit_data, eval_data, feature_size, class_num):
        self.fit_data = fit_data
        self.eval_data = eval_data
        self.feature_size = feature_size
        self.class_num = class_num

    def get_validation_data(self):
        indices_VX = []
        data_VX = []
        indptr_VX = []
        VZ = []
        first = True
        for (new_data, new_indices, new_indptr), vz in self.eval_data:
            if len(vz) != 0:
                indices_VX.append(new_indices)
                data_VX.append(new_data)
                if first:
                    indptr_VX.append(new_indptr)
                    first = False
                else:
                    indptr_VX.append(indptr_VX[-1][-1]+new_indptr[1:])
                VZ.append(vz)
        indptr_VX = np.concatenate(indptr_VX)
        data_VX = np.concatenate(data_VX)
        indices_VX = np.concatenate(indices_VX)
        VZ = np.concatenate(VZ, axis=0)
        VX = csr_matrix((data_VX, indices_VX, indptr_VX),
                        shape=(len(VZ), self.feature_size),
                        dtype=np.float64)
        return VX, VZ

    def run(self):
        models_folder = 'models'
        num_examples = 1000
        batch_size = num_examples
        max_iter = 700
        actual_time = time.time()
        new_time = time.time()
        print "Time spent in transforming the training dataset: "+str(new_time-actual_time)
        actual_time = new_time
        VX, VZ = self.get_validation_data()
        new_time = time.time()
        print "Time spent in transforming the validation dataset: "+str(new_time-actual_time)
        stop = climin.stops.any_([
            climin.stops.after_n_iterations(max_iter),
            ])
        pause = climin.stops.modulo_n_iterations(10)
        optimizer = 'rmsprop', {'steprate': 0.01, 'momentum': 0.9, 'decay': 0.9, 'step_adapt': 0.001}
        m = GeneralizedLinearSparseModel(self.feature_size, 1, out_transfer='sigmoid', loss='fmeasure',
                                         optimizer=optimizer, batch_size=batch_size, max_iter=max_iter,
                                         num_examples=num_examples)
        v_losses = []
        weight_decay = ((m.parameters.in_to_out ** 2).sum())
        weight_decay /= m.exprs['inpt'].shape[0]
        m.exprs['true_loss'] = m.exprs['loss']
        c_wd = 0.001
        m.exprs['loss'] = m.exprs['loss'] + c_wd * weight_decay

        # Set up a nice printout.
        keys = '#', 'val loss'
        max_len = max(len(i) for i in keys)
        header = '   '.join(i.ljust(max_len) for i in keys)
        print header
        print '-' * len(header)
        bp = None
        for i, info in enumerate(m.powerfit(self.fit_data, (VX, VZ), stop, pause)):
            v_losses.append(info['val_loss'])
            bp = info['best_pars']
            row = '%i' % i, '%.6f' % (1-info['val_loss'])
            print '   '.join(i.ljust(max_len) for i in row)
        np.save(os.path.join(models_folder, 'class%d' % self.class_num), bp)

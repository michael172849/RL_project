import numpy as np

import tensorflow as tf

class NN_model():
    def __init__(self, state_dims, output_dim, scope="model"):
        self.state_dims = state_dims
        self.out_dim = output_dim
        self.scope = scope

    def output(self, x):
        with tf.variable_scope(self.scope):
            layer_1 = tf.contrib.layers.fully_connected(
                inputs = x,
                num_outputs = 32,
                activation_fn = tf.nn.relu,
            )
            layer_2 = tf.contrib.layers.fully_connected(
                inputs = layer_1,
                num_outputs = 32,
                activation_fn = tf.nn.relu,
            )
            out_layer = tf.contrib.layers.fully_connected(
                inputs = layer_1,
                num_outputs = self.out_dim,
                activation_fn = None,
            )
            return out_layer

class QModelWithNN():
    def __init__(self,
                 state_dims):
        """
        state_dims: the number of dimensions of state space
        """
        self.input_dims = state_dims + 1

        self.nn_model = NN_model(self.input_dims, 1, "pi")
        self.X = tf.placeholder("float32", [None, self.input_dims])
        self.Y = tf.placeholder("float32", [None, 1])
        self.Y_hat = self.nn_model.output(self.X)
        self.loss_op=0.5 * tf.losses.mean_squared_error(self.Y,self.Y_hat)#loss function
        self.alpha = tf.placeholder("float32",[])
        optimizer = tf.train.AdamOptimizer(
                learning_rate = self.alpha,
                beta1=0.9,
                beta2=0.999,    
            )
        self.train_op = optimizer.minimize(self.loss_op)
        if tf.get_default_session() == None:
            self.sess = tf.Session()
        else:
            self.sess = tf.get_default_session()
        self.sess.run(tf.global_variables_initializer())


    def __call__(self, s_cont, s_cate, a):
        # TODO: implement this method
        s = np.append(s_cont, s_cate)
        X = np.reshape(np.append(s,[a]), (1,self.input_dims))
        pred = self.sess.run(self.Y_hat, feed_dict = {self.X:X})
        return pred[0,0]
    
    def compute_value(self, s_cont, s_cate, a, done=False):
        return self.__call__(s_cont, s_cate, a)

    def update(self,alpha,G,s_cont, s_cate, a_tau):
        s_tau = np.append(s_cont, s_cate)
        print(s_tau)
        X = np.reshape(np.append(s_tau,[a_tau]), (1,self.input_dims))
        Y = np.reshape(np.array([G]), (1,1,))
        self.sess.run(self.train_op, feed_dict = {self.X:X, self.Y:Y, self.alpha:alpha})



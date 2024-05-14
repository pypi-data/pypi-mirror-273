
import os
import numpy as np


class DataGenerator:
    
    """
    A class for reading and preprocessing text data.
    """

    def __init__(self, path: str, sequence_length: int) -> None:
        """
        Initializes a DataReader object with the path to a text file and the desired sequence length.

        Args:
            path (str): The path to the text file.
            sequence_length (int): The length of the sequences that will be fed to the self.
        """
        with open(path) as f:
            # Read the contents of the file
            self.data = f.read()

        # Find all unique characters in the text
        chars = list(set(self.data))

        # Create dictionaries to map characters to indices and vice versa
        self.char_to_idx = {ch: i for (i, ch) in enumerate(chars)}
        self.idx_to_char = {i: ch for (i, ch) in enumerate(chars)}

        # Store the size of the text data and the size of the vocabulary
        self.data_size = len(self.data)
        self.vocab_size = len(chars)

        # Initialize the pointer that will be used to generate sequences
        self.pointer = 0

        # Store the desired sequence length
        self.sequence_length = sequence_length


    def next_batch(self) -> (np.ndarray, list):
        
        """
        Generates a batch of input and target sequences.

        Returns:
            inputs_one_hot (np.ndarray): A numpy array with shape `(batch_size, vocab_size)` where each row is a one-hot encoded representation of a character in the input sequence.
            targets (list): A list of integers that correspond to the indices of the characters in the target sequence, which is the same as the input sequence shifted by one position to the right.
        """
        
        input_start = self.pointer
        input_end = self.pointer + self.sequence_length

        # Get the input sequence as a list of integers
        inputs = [self.char_to_idx[ch] for ch in self.data[input_start:input_end]]

        # One-hot encode the input sequence
        inputs_one_hot = np.zeros((len(inputs), self.vocab_size))
        inputs_one_hot[np.arange(len(inputs)), inputs] = 1

        # Get the target sequence as a list of integers
        targets = [self.char_to_idx[ch] for ch in self.data[input_start + 1:input_end + 1]]

        # Update the pointer
        self.pointer += self.sequence_length

        # Reset the pointer if the next batch would exceed the length of the text data
        if self.pointer + self.sequence_length + 1 >= self.data_size:
            self.pointer = 0

        return inputs_one_hot, targets


class LSTM:
    
    """
    A class used to represent a Recurrent Neural Network (LSTM).

    Attributes
    ----------
    hidden_size : int
        The number of hidden units in the LSTM.
    vocab_size : int
        The size of the vocabulary used by the LSTM.
    sequence_length : int
        The length of the input sequences fed to the LSTM.
    self.learning_rate : float
        The learning rate used during training.

    Methods
    -------
    __init__(hidden_size, vocab_size, sequence_length, self.learning_rate)
        Initializes an instance of the LSTM class.
    """

    def __init__(self, hidden_size:int, vocab_size:int, sequence_length:int, 
                 learning_rate:float) -> None:
        
        """
        Initializes an instance of the LSTM class.

        Parameters
        ----------
        hidden_size : int
            The number of hidden units in the LSTM.
        vocab_size : int
            The size of the vocabulary used by the LSTM.
        sequence_length : int
            The length of the input sequences fed to the LSTM.
        learning_rate : float
            The learning rate used during training.
        """
        
        # hyper parameters
        self.mby = None
        self.hidden_size = hidden_size
        self.vocab_size = vocab_size
        self.sequence_length = sequence_length
        self.learning_rate = learning_rate
        
        # model parameters
        self.Wf = np.random.uniform(-np.sqrt(1. / hidden_size), np.sqrt(1. / hidden_size),
                                    (hidden_size, hidden_size + vocab_size))
        self.bf = np.zeros((hidden_size, 1))
        
        self.Wi = np.random.uniform(-np.sqrt(1. / hidden_size), np.sqrt(1. / hidden_size),
                                    (hidden_size, hidden_size + vocab_size))
        self.bi = np.zeros((hidden_size, 1))

        self.Wc = np.random.uniform(-np.sqrt(1. / hidden_size), np.sqrt(1. / hidden_size),
                                    (hidden_size, hidden_size + vocab_size))
        self.bc = np.zeros((hidden_size, 1))
            
        self.Wo = np.random.uniform(-np.sqrt(1. / hidden_size), np.sqrt(1. / hidden_size),
                                    (hidden_size, hidden_size + vocab_size))
        self.bo = np.zeros((hidden_size, 1))
        
        self.Wy = np.random.uniform(-np.sqrt(1. / hidden_size), np.sqrt(1. / hidden_size),
                                    (vocab_size, hidden_size))
        self.by = np.zeros((vocab_size, 1))

        # initialize parameters for adamw optimizer
        self.mWf = np.zeros_like(self.Wf)
        self.vWf = np.zeros_like(self.Wf)
        self.mWi = np.zeros_like(self.Wi)
        self.vWi = np.zeros_like(self.Wi)
        self.mWc = np.zeros_like(self.Wc)
        self.vWc = np.zeros_like(self.Wc)
        self.mWo = np.zeros_like(self.Wo)
        self.vWo = np.zeros_like(self.Wo)
        self.mWy = np.zeros_like(self.Wy)
        self.vWy = np.zeros_like(self.Wy)
        self.mbf = np.zeros_like(self.bf)
        self.vbf = np.zeros_like(self.bf)
        self.mbi = np.zeros_like(self.bi)
        self.vbi = np.zeros_like(self.bi)
        self.mbc = np.zeros_like(self.bc)
        self.vbc = np.zeros_like(self.bc)
        self.mbo = np.zeros_like(self.bo)
        self.vbo = np.zeros_like(self.bo)
        self.mby = np.zeros_like(self.by)
        self.vby = np.zeros_like(self.by)

    def sigmoid(self, x:np.ndarray) -> np.ndarray:
        
        """
        Computes the sigmoid activation function for a given input array.

        Parameters:
            x (ndarray): Input array.

        Returns:
            ndarray: Array of the same shape as `x`, containing the sigmoid activation values.
        """
        
        return 1 / (1 + np.exp(-x))

    def loss(self, y_preds:np.ndarray, targets:np.ndarray) -> np.ndarray:
        
        """
        Computes the cross-entropy loss for a given sequence of predicted probabilities and true targets.

        Parameters:
            y_preds (ndarray): Array of shape (sequence_length, vocab_size) containing the predicted probabilities for each time step.
            targets (ndarray): Array of shape (sequence_length, 1) containing the true targets for each time step.

        Returns:
            float: Cross-entropy loss.
        """
        
        # calculate cross-entropy loss
        return sum(-np.log(y_preds[t][targets[t], 0]) for t in range(self.sequence_length))
    
    def adamw(self, beta1:float=0.9, beta2:float=0.999, epsilon:float=1e-8, 
              L2_reg:float=1e-4) -> None:
        
        """
        Updates the LSTM's parameters using the AdamW optimization algorithm.
        """
        
        # AdamW update for Wf
        self.mWf = beta1 * self.mWf + (1 - beta1) * self.dWf
        self.vWf = beta2 * self.vWf + (1 - beta2) * np.square(self.dWf)
        m_hat = self.mWf / (1 - beta1)
        v_hat = self.vWf / (1 - beta2)
        self.Wf -= self.learning_rate * (m_hat / (np.sqrt(v_hat) + epsilon) + L2_reg * self.Wf)

        # AdamW update for bf
        self.mbf = beta1 * self.mbf + (1 - beta1) * self.dbf
        self.vbf = beta2 * self.vbf + (1 - beta2) * np.square(self.dbf)
        m_hat = self.mbf / (1 - beta1)
        v_hat = self.vbf / (1 - beta2)
        self.bf -= self.learning_rate * (m_hat / (np.sqrt(v_hat) + epsilon) + L2_reg * self.bf)

        # AdamW update for Wi
        self.mWi = beta1 * self.mWi + (1 - beta1) * self.dWi
        self.vWi = beta2 * self.vWi + (1 - beta2) * np.square(self.dWi)
        m_hat = self.mWi / (1 - beta1)
        v_hat = self.vWi / (1 - beta2)
        self.Wi -= self.learning_rate * (m_hat / (np.sqrt(v_hat) + epsilon) + L2_reg * self.Wi)

        # AdamW update for bi
        self.mbi = beta1 * self.mbi + (1 - beta1) * self.dbi
        self.vbi = beta2 * self.vbi + (1 - beta2) * np.square(self.dbi)
        m_hat = self.mbi / (1 - beta1)
        v_hat = self.vbi / (1 - beta2)
        self.bi -= self.learning_rate * (m_hat / (np.sqrt(v_hat) + epsilon) + L2_reg * self.bi)

        # AdamW update for Wc
        self.mWc = beta1 * self.mWc + (1 - beta1) * self.dWc
        self.vWc = beta2 * self.vWc + (1 - beta2) * np.square(self.dWc)
        m_hat = self.mWc / (1 - beta1)
        v_hat = self.vWc / (1 - beta2)
        self.Wc -= self.learning_rate * (m_hat / (np.sqrt(v_hat) + epsilon) + L2_reg * self.Wc)

        # AdamW update for bc
        self.mbc = beta1 * self.mbc + (1 - beta1) * self.dbc
        self.vbc = beta2 * self.vbc + (1 - beta2) * np.square(self.dbc)
        m_hat = self.mbc / (1 - beta1)
        v_hat = self.vbc / (1 - beta2)
        self.bc -= self.learning_rate * (m_hat / (np.sqrt(v_hat) + epsilon) + L2_reg * self.bc)

        # AdamW update for Wy
        self.mWy = beta1 * self.mWy + (1 - beta1) * self.dWy
        self.vWy = beta2 * self.vWy + (1 - beta2) * np.square(self.dWy)
        m_hat = self.mWy / (1 - beta1)
        v_hat = self.vWy / (1 - beta2)
        self.Wy -= self.learning_rate * (m_hat / (np.sqrt(v_hat) + epsilon) + L2_reg * self.Wy)
        # AdamW update for by
        self.mby = beta1 * self.mby + (1 - beta1) * self.dby
        self.vby = beta2 * self.vby + (1 - beta2) * np.square(self.dby)
        m_hat = self.mby / (1 - beta1)
        v_hat = self.vby / (1 - beta2)
        self.by -= self.learning_rate * (m_hat / (np.sqrt(v_hat) + epsilon) + L2_reg * self.by)

    def forward(self, X:np.ndarray, c_prev:np.ndarray, a_prev:np.ndarray
                ) -> (np.ndarray, dict, dict, dict, dict, dict, dict, dict):
        
        """
        Performs forward propagation for a simple LSTM model.

        Args:
            X (numpy array): Input sequence, shape (sequence_length, input_size)
            c_prev (numpy array): Previous cell state, shape (hidden_size, 1)
            a_prev (numpy array): Previous hidden state, shape (hidden_size, 1)

        Returns:
            X (numpy array): Input sequence, shape (sequence_length, input_size)
            c (dictionary): Cell state for each time step, keys = time step, values = numpy array shape (hidden_size, 1)
            f (dictionary): Forget gate for each time step, keys = time step, values = numpy array shape (hidden_size, 1)
            i (dictionary): Input gate for each time step, keys = time step, values = numpy array shape (hidden_size, 1)
            o (dictionary): Output gate for each time step, keys = time step, values = numpy array shape (hidden_size, 1)
            cc (dictionary): Candidate cell state for each time step, keys = time step, values = numpy array shape (hidden_size, 1)
            a (dictionary): Hidden state for each time step, keys = time step, values = numpy array shape (hidden_size, 1)
            y_pred (dictionary): Output probability vector for each time step, keys = time step, values = numpy array shape (output_size, 1)
        """
        
        # initialize dictionaries for backpropagation 
        c, f, i, o, cc, a, y_pred = {}, {}, {}, {}, {}, {}, {}
        c[-1] = np.copy(c_prev)  # store the initial cell state in the dictionary
        a[-1] = np.copy(a_prev)  # store the initial hidden state in the dictionary

        # iterate over each time step in the input sequence
        for t in range(X.shape[0]):
            # concatenate the input and hidden state
            xt = X[t, :].reshape(-1, 1)
            concat = np.vstack((a[t - 1], xt))

            # compute the forget gate
            f[t] = self.sigmoid(np.dot(self.Wf, concat) + self.bf)

            # compute the input gate
            i[t] = self.sigmoid(np.dot(self.Wi, concat) + self.bi)

            # compute the candidate cell state
            cc[t] = np.tanh(np.dot(self.Wc, concat) + self.bc)

            # compute the cell state
            c[t] = f[t] * c[t - 1] + i[t] * cc[t]

            # compute the output gate
            o[t] = self.sigmoid(np.dot(self.Wo, concat) + self.bo)

            # compute the hidden state
            a[t] = o[t] * np.tanh(c[t])

            # compute the output probability vector
            y_pred[t] = self.softmax(np.dot(self.Wy, a[t]) + self.by)

        # return the output probability vectors, cell state, hidden state and gate vectors
        return X, y_pred, c, f, i, o, cc, a 
    
    def backward(self, X:np.ndarray, targets, y_pred, c_prev, a_prev, c, f, i, o, cc, a) -> None:
        
        """
        Performs backward propagation through time for an LSTM network.

        Args:
        - X: input data for each time step, with shape (sequence_length, input_size)
        - targets: target outputs for each time step, with shape (sequence_length, output_size)
        - y_pred: predicted outputs for each time step, with shape (sequence_length, output_size)
        - c_prev: previous cell state, with shape (hidden_size, 1)
        - a_prev: previous hidden state, with shape (hidden_size, 1)
        - c: cell state for each time step, with shape (sequence_length, hidden_size)
        - f: forget gate output for each time step, with shape (sequence_length, hidden_size)
        - i: input gate output for each time step, with shape (sequence_length, hidden_size)
        - o: output gate output for each time step, with shape (sequence_length, hidden_size)
        - cc: candidate cell state for each time step, with shape (sequence_length, hidden_size)
        - a: hidden state output for each time step, with shape (sequence_length, hidden_size)
        Returns:
            None
        """
        
        # initialize gradients for each parameter
        self.dWf, self.dWi, self.dWc, self.dWo, self.dWy = np.zeros_like(self.Wf), np.zeros_like(self.Wi), np.zeros_like(self.Wc), np.zeros_like(self.Wo), np.zeros_like(self.Wy)
        self.dbf, self.dbi, self.dbc, self.dbo, self.dby = np.zeros_like(self.bf), np.zeros_like(self.bi), np.zeros_like(self.bc), np.zeros_like(self.bo), np.zeros_like(self.by)
        dc_next = np.zeros_like(c_prev)
        da_next = np.zeros_like(a_prev)

        # iterate backwards through time steps
        for t in reversed(range(X.shape[0])):
            # compute the gradient of the output probability vector
            dy = np.copy(y_pred[t])
            dy[targets[t]] -= 1

            # compute the gradient of the output layer weights and biases
            self.dWy += np.dot(dy, a[t].T)
            self.dby += dy

            # compute the gradient of the hidden state
            da = np.dot(self.Wy.T, dy) + da_next
            dc = dc_next + (1 - np.tanh(c[t])**2) * o[t] * da
            
            # compute the gradient of the output gate
            xt = X[t, :].reshape(-1, 1)
            concat = np.vstack((a[t - 1], xt))
            do = o[t] * (1 - o[t]) * np.tanh(c[t]) * da
            self.dWo += np.dot(do, concat.T)
            self.dbo += do

            # compute the gradient of the candidate cell state
            dcc = dc * i[t] * (1 - np.tanh(cc[t])**2)
            self.dWc += np.dot(dcc, concat.T)
            self.dbc += dcc

            # compute the gradient of the input gate
            di = i[t] * (1 - i[t]) * cc[t] * dc
            self.dWi += np.dot(di, concat.T)
            self.dbi += di

            # compute the gradient of the forget gate
            df = f[t] * (1 - f[t]) * c[t - 1] * dc
            self.dWf += np.dot(df, concat.T)
            self.dbf += df

            # compute the gradient of the input to the current hidden state and cell state
            da_next = np.dot(self.Wf[:, :self.hidden_size].T, df)\
            + np.dot(self.Wi[:, :self.hidden_size].T, di)\
            + np.dot(self.Wc[:, :self.hidden_size].T, dcc)\
            + np.dot(self.Wo[:, :self.hidden_size].T, do)
            dc_next = dc * f[t]

        # clip gradients to avoid exploding gradients
        for grad in [self.dWf, self.dWi, self.dWc, self.dWo, self.dWy, self.dbf, self.dbi, self.dbc, self.dbo, self.dby]:
            np.clip(grad, -1, 1, out=grad)
            
    def train(self, data_generator:DataGenerator) -> None:
        
        """
        Train the LSTM on a dataset using backpropagation through time.

        Args:
            data_generator: An instance of DataGenerator containing the training data.

        Returns:
            None
        """
        
        iter_num = 0
        # stopping criterion for training
        threshold = 46
        smooth_loss = -np.log(1.0 / data_generator.vocab_size) * self.sequence_length  # initialize loss
        while (smooth_loss > threshold):
            # initialize hidden state at the beginning of each sequence
            if data_generator.pointer == 0:
                c_prev = np.zeros((self.hidden_size, 1))
                a_prev = np.zeros((self.hidden_size, 1))

            # get a batch of inputs and targets
            inputs, targets = data_generator.next_batch()

            # forward pass
            X, y_pred, c, f, i, o, cc, a   = self.forward(inputs, c_prev, a_prev)
        
            # backward pass
            self.backward( X, targets, y_pred, c_prev, a_prev, c, f, i, o, cc, a)

            # calculate and update loss
            loss = self.loss(y_pred, targets)
            self.adamw()
            smooth_loss = smooth_loss * 0.999 + loss * 0.001
            # update previous hidden state for the next batch
            a_prev = a[self.sequence_length - 1]
            c_prev = c[self.sequence_length - 1]
            # print progress every 1000 iterations
            if iter_num % 1000 == 0:
                self.learning_rate *= 0.99
                sample_idx = self.sample(c_prev, a_prev, inputs[0, :], 200)
                print(''.join(data_generator.idx_to_char[idx] for idx in sample_idx))
                print("\n\niter :%d, loss:%f" % (iter_num, smooth_loss))
            iter_num += 1
             
    def sample(self, c_prev:np.ndarray, a_prev:np.ndarray, seed_idx:np.ndarray, 
               n:int) -> list:
        
        """
        Sample a sequence of integers from the model.

        Args:
            c_prev (numpy.ndarray): Previous cell state, a numpy array of shape (hidden_size, 1).
            a_prev (numpy.ndarray): Previous hidden state, a numpy array of shape (hidden_size, 1).
            seed_idx (numpy.ndarray): Seed letter from the first time step, a numpy array of shape (vocab_size, 1).
            n (int): Number of characters to generate.

        Returns:
            list: A list of integers representing the generated sequence.

        """
        
        # initialize input and seed_idx
        x = np.zeros((self.vocab_size, 1))
        # convert one-hot encoding to integer index
        seed_idx = np.argmax(seed_idx, axis=-1)

        # set the seed letter as the input for the first time step
        x[seed_idx] = 1

        # generate sequence of characters
        idxes = []
        c = np.copy(c_prev)
        a = np.copy(a_prev)
        for t in range(n):
            # compute the hidden state and cell state
            concat = np.vstack((a, x))
            i = self.sigmoid(np.dot(self.Wi, concat) + self.bi)
            f = self.sigmoid(np.dot(self.Wf, concat) + self.bf)
            cc = np.tanh(np.dot(self.Wc, concat) + self.bc)
            c = f * c + i * cc
            o = self.sigmoid(np.dot(self.Wo, concat) + self.bo)
            a = o * np.tanh(c)

            # compute the output probabilities
            y = self.softmax(np.dot(self.Wy, a) + self.by)

            # sample the next character from the output probabilities
            idx = np.random.choice(range(self.vocab_size), p=y.ravel())

            # set the input for the next time step
            x = np.zeros((self.vocab_size, 1))
            x[idx] = 1

            # append the sampled character to the sequence
            idxes.append(idx)

        # return the generated sequence
        return idxes

    def predict(self, data_generator:DataGenerator, start:str, n:int) -> str:
        
        """
        Generate a sequence of n characters using the trained LSTM model, starting from the given start sequence.

        Args:
        - data_generator: an instance of DataGenerator
        - start: a string containing the start sequence
        - n: an integer indicating the length of the generated sequence

        Returns:
        - txt: a string containing the generated sequence
        """
        
        # initialize input sequence
        x = np.zeros((self.vocab_size, 1))
        chars = [ch for ch in start]
        idxes = []
        for i in range(len(chars)):
            idx = data_generator.char_to_idx[chars[i]]
            x[idx] = 1
            idxes.append(idx)
        # initialize cell state and hidden state
        a = np.zeros((self.hidden_size, 1))
        c = np.zeros((self.hidden_size, 1))
            
        # generate new sequence of characters
        for t in range(n):
            # compute the hidden state and cell state
            concat = np.vstack((a, x))
            i = self.sigmoid(np.dot(self.Wi, concat) + self.bi)
            f = self.sigmoid(np.dot(self.Wf, concat) + self.bf)
            cc = np.tanh(np.dot(self.Wc, concat) + self.bc)
            c = f * c + i * cc
            o = self.sigmoid(np.dot(self.Wo, concat) + self.bo)
            a = o * np.tanh(c)
            # compute the output probabilities
            y_pred = self.softmax(np.dot(self.Wy, a) + self.by)
            # sample the next character from the output probabilities
            idx = np.random.choice(range(self.vocab_size), p=y_pred.ravel())
            x = np.zeros((self.vocab_size, 1))
            x[idx] = 1
            idxes.append(idx)
        
        txt = ''.join(data_generator.idx_to_char[i] for i in idxes)
        txt.replace('\n',"")
        
        return txt
    
    
if __name__ == '__main__':
    
    sequence_length = 28
    #read text from the "input.txt" file
    data_generator = DataGenerator('/kaggle/input/shakespeare-text/text.txt', sequence_length)
    lstm =  LSTM(hidden_size=1000, vocab_size=data_generator.vocab_size,sequence_length=sequence_length,learning_rate=1e-3)
    lstm.train(data_generator)
    
    lstm.predict(data_generator, "c", 150)
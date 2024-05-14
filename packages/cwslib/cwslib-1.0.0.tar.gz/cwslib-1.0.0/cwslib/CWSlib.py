#!/usr/bin/env python
"""Toolbox for Consistent Weighted Sampling Algorithms

This module contains the following algorithms: the standard MinHash algorithm for binary sets and
weighted MinHash algorithms for weighted sets.

This module contains the following algorithms: the standard MinHash algorithm for binary sets and
several Consistent Weighted Sampling algorithms(CWS、ICWS、I2CWS、PCWS、CCWS、0-bit CWS、SCWS).

Each algorithm converts a data instance (i.e., vector) into the hash code of the specified length,
and computes the time of encoding.


Usage
---------
    >>>import cwslib
    >>>from cwslib.CWSlib import ConsistentWeightedSampling
    >>> from CWSlib import ConsistentWeightedSampling
    >>> cws = cwslib.CWSlib.ConsistentWeightedSampling(data, dimension_num)
    >>> fingerprints_k, fingerprints_y, elapsed = cws.algorithm_name(...)
      or
    >>> fingerprints, elapsed = cws.algorithm_name(...)

Parameters
----------
data: {array-like, sparse matrix}, shape (n_features, n_instances), format='csc'
    a data matrix where row represents feature and column is data instance

dimension_num: int
    the length of hash code

seed: int, default: 1
    part of the seed of the random number generator

Returns
-----------
fingerprints_k: ndarray, shape (n_instances, dimension_num)
    one component of hash code from some algorithms, and each row is the hash code for a data instance

fingerprints_y: ndarray, shape (n_instances, dimension_num)
    one component of hash code from some algorithms, and each row is the hash code for a data instance

fingerprints: ndarray, shape (n_instances, dimension_num)
    only one component of hash code from some algorithms, and each row is the hash code for a data instance

elapsed: float
    time of hashing data matrix

"""

import numpy as np  # Import numpy for numerical computations
import numpy.matlib  # Import numpy.matlib for matrix operations
import scipy as sp  # Import scipy for scientific computing
import scipy.sparse as sparse  # Import scipy.sparse for sparse matrix operations
import time  # Import time for measuring execution time
from ctypes import *  # Import ctypes for calling C functions from Python


class ConsistentWeightedSampling:
    """Main class contains 13 algorithms

    Attributes:
    -----------
    PRIME_RANGE: int
        the range of prime numbers

    PRIMES: ndarray
        a 1-d array to save all prime numbers within PRIME_RANGE, which is used to produce hash functions
                 $\pi = (a*i+b) mod c$, $a, b, c \in PRIMES$
        The two constants are used for minhash(self), haveliwala(self, scale), haeupler(self, scale)

    weighted_set: {array-like, sparse matrix}, shape (n_features, n_instances)
        a data matrix where row represents feature and column is data instance

    dimension_num: int
        the length of hash code

    seed: int, default: 1
        part of the seed of the random number generator. Note that the random seed consists of seed and repeat.

    instance_num: int
        the number of data instances

    feature_num: int
        the number of features
    """

    C_PRIME = 10000000000037  # Prime number used in the algorithm

    def __init__(self, weighted_set, dimension_num, seed=1):

        self.weighted_set = weighted_set
        self.dimension_num = dimension_num
        self.seed = seed
        self.instance_num = self.weighted_set.shape[1]
        self.feature_num = self.weighted_set.shape[0]

    def minhash(self, repeat=1):
        """The standard MinHash algorithm for binary sets
           A. Z. Broder, M. Charikar, A. M. Frieze, and M. Mitzenmacher, "Min-wise Independent Permutations",
           in STOC, 1998, pp. 518-529

        Parameters
        ----------
        repeat: int, default: 1
            the number of repeating the algorithm as the part of the seed of the random number generator

        Returns
        ---------
        fingerprints: ndarray, shape (n_instances, dimension_num)
            hash codes for data matrix, where row represents a data instance

        elapsed: float
            time of hashing data matrix
        """
        fingerprints = np.zeros((self.instance_num, self.dimension_num))

        np.random.seed(self.seed * np.power(2, repeat - 1))

        start = time.time()
        hash_parameters = np.random.randint(1, self.C_PRIME, (self.dimension_num, 2))

        for j_sample in range(0, self.instance_num):
            feature_id = sparse.find(self.weighted_set[:, j_sample] > 0)[0]
            feature_id_num = feature_id.shape[0]

            k_hash = np.mod(
                np.dot(np.transpose(np.array([feature_id])), np.array([np.transpose(hash_parameters[:, 1])])) +
                np.dot(np.ones((feature_id_num, 1)), np.array([np.transpose(hash_parameters[:, 1])])),
                self.C_PRIME)

            min_position = np.argmin(k_hash, axis=0)
            fingerprints[j_sample, :] = feature_id[min_position]

        elapsed = time.time() - start

        return fingerprints, elapsed

    def cws(self, repeat=1):
        """The Consistent Weighted Sampling (CWS) algorithm, as the first of the Consistent Weighted Sampling scheme,
           extends "active indices" from $[0, S]$ in [Gollapudi et. al., 2006](1) to $[0, +\infty]$.
           M. Manasse, F. McSherry, and K. Talwar, "Consistent Weighted Sampling", Unpublished technical report, 2010.

        Parameters
        -----------
        repeat: int, default: 1
            the number of repeating the algorithm as the part of the seed of the random number generator

        Returns
        -----------
        fingerprints_k: ndarray, shape (n_instances, dimension_num)
            one component of hash codes $(k, y_k)$ for data matrix, where row represents a data instance

        fingerprints_y: ndarray, shape (n_instances, dimension_num)
            one component of hash codes $(k, y_k)$ for data matrix, where row represents a data instance

        elapsed: float
            time of hashing data matrix

        Notes
        ----------
        For the algorithm, dynamic link library files corresponding to the operating system should be selected.
        该算法使用了动态链接库，请对应操作系统选择相应的动态链接库文件。
            Windows：./cpluspluslib/cws_fingerprints.dll
            Linux：./cpluspluslib/cws_fingerprints.so

        The operations of seeking "active indices" and computing hashing values are implemented by C++
        due to low efficiency of Python. The operations cannot be vectorized in Python so that it would be
        very slow.
        由于Python效率较低，"活跃索引"的搜索和哈希值的计算操作由C++实现。这些操作在Python中无法进行向量化，因此速度会非常慢。
        """

        fingerprints_k = np.zeros((self.instance_num, self.dimension_num))
        fingerprints_y = np.zeros((self.instance_num, self.dimension_num))

        start = time.time()

        for j_sample in range(0, self.instance_num):

            feature_id = sparse.find(self.weighted_set[:, j_sample] > 0)[0]
            feature_id_num = feature_id.shape[0]
            """Windows"""
            fingerprints = CDLL('./cpluspluslib/cws_fingerprints.dll')

            """
            Linux
            fingerprints = CDLL('./cpluspluslib/cws_fingerprints.so')
            """

            fingerprints.GenerateFingerprintOfInstance.argtypes = [c_int,
                                                                   np.ctypeslib.ndpointer(dtype=c_double, ndim=1,
                                                                                          flags="C_CONTIGUOUS"),
                                                                   np.ctypeslib.ndpointer(dtype=c_int, ndim=1,
                                                                                          flags="C_CONTIGUOUS"),
                                                                   c_int, c_int,
                                                                   np.ctypeslib.ndpointer(dtype=c_double, ndim=1,
                                                                                          flags="C_CONTIGUOUS"),
                                                                   np.ctypeslib.ndpointer(dtype=c_double, ndim=1,
                                                                                          flags="C_CONTIGUOUS")]
            fingerprints.GenerateFingerprintOfInstance.restype = None
            weights = np.array(self.weighted_set[feature_id, j_sample].todense())[:, 0]
            fingerprint_k = np.zeros((1, self.dimension_num))[0]
            fingerprint_y = np.zeros((1, self.dimension_num))[0]

            fingerprints.GenerateFingerprintOfInstance(self.dimension_num,
                                                       weights, feature_id, feature_id_num, self.seed * repeat,
                                                       fingerprint_k, fingerprint_y)

            fingerprints_k[j_sample, :] = fingerprint_k
            fingerprints_y[j_sample, :] = fingerprint_y

        elapsed = time.time() - start

        return fingerprints_k, fingerprints_y, elapsed

    def icws(self, repeat=1):
        """The Improved Consistent Weighted Sampling (ICWS) algorithm, directly samples the two special "active indices",
           $y_k$ and $z_k$.
           S. Ioffe, "Improved Consistent Weighted Sampling, Weighted Minhash and L1 Sketching",
           in ICDM, 2010, pp. 246-255.

        Parameters
        ----------
        repeat: int, default: 1
            the number of repeating the algorithm as the part of the seed of the random number generator

        Returns
        -----------
        fingerprints_k: ndarray, shape (n_instances, dimension_num)
            one component of hash codes $(k, y_k)$ for data matrix, where row represents a data instance

        fingerprints_y: ndarray, shape (n_instances, dimension_num)
            one component of hash codes $(k, y_k)$ for data matrix, where row represents a data instance

        elapsed: float
            time of hashing data matrix
        """

        fingerprints_k = np.zeros((self.instance_num, self.dimension_num))
        fingerprints_y = np.zeros((self.instance_num, self.dimension_num))

        np.random.seed(self.seed * np.power(2, repeat - 1))
        start = time.time()

        beta = np.random.uniform(0, 1, (self.feature_num, self.dimension_num))
        v1 = np.random.uniform(0, 1, (self.feature_num, self.dimension_num))
        v2 = np.random.uniform(0, 1, (self.feature_num, self.dimension_num))
        u1 = np.random.uniform(0, 1, (self.feature_num, self.dimension_num))
        u2 = np.random.uniform(0, 1, (self.feature_num, self.dimension_num))

        for j_sample in range(0, self.instance_num):
            feature_id = sparse.find(self.weighted_set[:, j_sample] > 0)[0]
            gamma = - np.log(np.multiply(u1[feature_id, :], u2[feature_id, :]))
            t_matrix = np.floor(np.divide(
                np.matlib.repmat(np.log(self.weighted_set[feature_id, j_sample].todense()), 1, self.dimension_num),
                gamma) + beta[feature_id, :])
            y_matrix = np.exp(np.multiply(gamma, t_matrix - beta[feature_id, :]))
            a_matrix = np.divide(np.multiply(-np.log(np.multiply(v1[feature_id, :], v2[feature_id, :])),
                                             np.multiply(u1[feature_id, :], u2[feature_id, :])), y_matrix)

            min_position = np.argmin(a_matrix, axis=0)
            fingerprints_k[j_sample, :] = feature_id[min_position]
            fingerprints_y[j_sample, :] = y_matrix[min_position, np.arange(a_matrix.shape[1])]

        elapsed = time.time() - start

        return fingerprints_k, fingerprints_y, elapsed

    def licws(self, repeat=1):
        """The 0-bit Consistent Weighted Sampling (0-bit CWS) algorithm generates the original hash code $(k, y_k)$
           by running ICWS, but finally adopts only $k$ to constitute the fingerprint.
           P. Li, "0-bit Consistent Weighted Sampling", in KDD, 2015, pp. 665-674.

        Parameters
        ----------
        repeat: int, default: 1
            the number of repeating the algorithm as the part of the seed of the random number generator

        Returns
        ----------
        fingerprints: ndarray, shape (n_instances, dimension_num)
            hash codes for data matrix, where row represents a data instance

        elapsed: float
            time of hashing data matrix
        """

        fingerprints = np.zeros((self.instance_num, self.dimension_num))

        np.random.seed(self.seed * np.power(2, repeat - 1))
        start = time.time()

        beta = np.random.uniform(0, 1, (self.feature_num, self.dimension_num))
        v1 = np.random.uniform(0, 1, (self.feature_num, self.dimension_num))
        v2 = np.random.uniform(0, 1, (self.feature_num, self.dimension_num))
        u1 = np.random.uniform(0, 1, (self.feature_num, self.dimension_num))
        u2 = np.random.uniform(0, 1, (self.feature_num, self.dimension_num))

        for j_sample in range(0, self.instance_num):
            feature_id = sparse.find(self.weighted_set[:, j_sample] > 0)[0]
            gamma = - np.log(np.multiply(u1[feature_id, :], u2[feature_id, :]))
            t_matrix = np.floor(np.divide(
                np.matlib.repmat(np.log(self.weighted_set[feature_id, j_sample].todense()), 1, self.dimension_num),
                gamma) + beta[feature_id, :])
            y_matrix = np.exp(np.multiply(gamma, t_matrix - beta[feature_id, :]))
            a_matrix = np.divide(np.multiply(-np.log(np.multiply(v1[feature_id, :], v2[feature_id, :])),
                                             np.multiply(u1[feature_id, :], u2[feature_id, :])), y_matrix)

            min_position = np.argmin(a_matrix, axis=0)
            fingerprints[j_sample, :] = feature_id[min_position]

        elapsed = time.time() - start

        return fingerprints, elapsed

    def pcws(self, repeat=1):
        """The Practical Consistent Weighted Sampling (PCWS) algorithm improves the efficiency of ICWS
           by simplifying the mathematical expressions.
           W. Wu, B. Li, L. Chen, and C. Zhang, "Consistent Weighted Sampling Made More Practical",
           in WWW, 2017, pp. 1035-1043.

        Parameters
        ----------
        repeat: int, default: 1
            the number of repeating the algorithm as the part of the seed of the random number generator

        Returns
        -----------
        fingerprints_k: ndarray, shape (n_instances, dimension_num)
            one component of hash codes $(k, y_k)$ for data matrix, where row represents a data instance

        fingerprints_y: ndarray, shape (n_instances, dimension_num)
            one component of hash codes $(k, y_k)$ for data matrix, where row represents a data instance

        elapsed: float
            time of hashing data matrix
        """

        fingerprints_k = np.zeros((self.instance_num, self.dimension_num))
        fingerprints_y = np.zeros((self.instance_num, self.dimension_num))

        np.random.seed(self.seed * np.power(2, repeat - 1))
        start = time.time()

        beta = np.random.uniform(0, 1, (self.feature_num, self.dimension_num))
        x = np.random.uniform(0, 1, (self.feature_num, self.dimension_num))
        u1 = np.random.uniform(0, 1, (self.feature_num, self.dimension_num))
        u2 = np.random.uniform(0, 1, (self.feature_num, self.dimension_num))

        for j_sample in range(0, self.instance_num):
            feature_id = sparse.find(self.weighted_set[:, j_sample] > 0)[0]
            gamma = - np.log(np.multiply(u1[feature_id, :], u2[feature_id, :]))
            t_matrix = np.floor(np.divide(
                np.matlib.repmat(np.log(self.weighted_set[feature_id, j_sample].todense()), 1, self.dimension_num),
                gamma) + beta[feature_id, :])
            y_matrix = np.exp(np.multiply(gamma, t_matrix - beta[feature_id, :]))
            a_matrix = np.divide(-np.log(x[feature_id, :]), np.divide(y_matrix, u1[feature_id, :]))

            min_position = np.argmin(a_matrix, axis=0)
            fingerprints_k[j_sample, :] = feature_id[min_position]
            fingerprints_y[j_sample, :] = y_matrix[min_position, np.arange(a_matrix.shape[1])]

        elapsed = time.time() - start

        return fingerprints_k, fingerprints_y, elapsed

    def ccws(self, repeat=1, scale=1):
        """The Canonical Consistent Weighted Sampling (CCWS) algorithm directly uniformly discretizes the original weight
           instead of uniformly discretizing the logarithm of the weight as ICWS.
           W. Wu, B. Li, L. Chen, and C. Zhang, "Canonical Consistent Weighted Sampling for Real-Value Weighetd Min-Hash",
           in ICDM, 2016, pp. 1287-1292.

        Parameters
        ----------
        repeat: int, default: 1
            the number of repeating the algorithm as the part of the seed of the random number generator

        scale: int
            a constant to adapt the weight

        Returns
        -----------
        fingerprints_k: ndarray, shape (n_instances, dimension_num)
            one component of hash codes $(k, y_k)$ for data matrix, where row represents a data instance

        fingerprints_y: ndarray, shape (n_instances, dimension_num)
            one component of hash codes $(k, y_k)$ for data matrix, where row represents a data instance

        elapsed: float
            time of hashing data matrix
        """

        fingerprints_k = np.zeros((self.instance_num, self.dimension_num))
        fingerprints_y = np.zeros((self.instance_num, self.dimension_num))

        np.random.seed(self.seed * np.power(2, repeat - 1))
        start = time.time()

        beta = np.random.uniform(0, 1, (self.feature_num, self.dimension_num))
        gamma = np.random.beta(2, 1, (self.feature_num, self.dimension_num))
        c = np.random.gamma(2, 1, (self.feature_num, self.dimension_num))

        for j_sample in range(0, self.instance_num):
            feature_id = sparse.find(self.weighted_set[:, j_sample] > 0)[0]
            t_matrix = np.floor(scale * np.divide(np.matlib.repmat(self.weighted_set[feature_id, j_sample].todense(), 1,
                                                                   self.dimension_num),
                                                  gamma[feature_id, :]) + beta[feature_id, :])
            y_matrix = np.multiply(gamma[feature_id, :], (t_matrix - beta[feature_id, :]))
            a_matrix = np.divide(c[feature_id, :], y_matrix) - 2 * np.multiply(gamma[feature_id, :], c[feature_id, :])

            min_position = np.argmin(a_matrix, axis=0)
            fingerprints_k[j_sample, :] = feature_id[min_position]
            fingerprints_y[j_sample, :] = y_matrix[min_position, np.arange(a_matrix.shape[1])]

        elapsed = time.time() - start

        return fingerprints_k, fingerprints_y, elapsed

    def i2cws(self, repeat=1):
        """The Improved Improved Consistent Weighted Sampling (I$^2$CWS) algorithm, samples the two special
           "active indices", $y_k$ and $z_k$, independently by avoiding the equation of $y_k$ and $z_k$ in ICWS.
           W. Wu, B. Li, L. Chen, C. Zhang and P. S. Yu, "Improved Consistent Weighted Sampling Revisited",
           DOI: 10.1109/TKDE.2018.2876250, 2018.

        Parameters
        ----------
        repeat: int, default: 1
            the number of repeating the algorithm as the part of the seed of the random number generator

        Returns
        -----------
        fingerprints_k: ndarray, shape (n_instances, dimension_num)
            one component of hash codes $(k, y_k)$ for data matrix, where row represents a data instance

        fingerprints_y: ndarray, shape (n_instances, dimension_num)
            one component of hash codes $(k, y_k)$ for data matrix, where row represents a data instance

        elapsed: float
            time of hashing data matrix
        """

        fingerprints_k = np.zeros((self.instance_num, self.dimension_num))
        fingerprints_y = np.zeros((self.instance_num, self.dimension_num))

        np.random.seed(self.seed * np.power(2, repeat - 1))
        start = time.time()

        beta1 = np.random.uniform(0, 1, (self.feature_num, self.dimension_num))
        beta2 = np.random.uniform(0, 1, (self.feature_num, self.dimension_num))
        u1 = np.random.uniform(0, 1, (self.feature_num, self.dimension_num))
        u2 = np.random.uniform(0, 1, (self.feature_num, self.dimension_num))
        u3 = np.random.uniform(0, 1, (self.feature_num, self.dimension_num))
        u4 = np.random.uniform(0, 1, (self.feature_num, self.dimension_num))
        v1 = np.random.uniform(0, 1, (self.feature_num, self.dimension_num))
        v2 = np.random.uniform(0, 1, (self.feature_num, self.dimension_num))

        for j_sample in range(0, self.instance_num):
            feature_id = sparse.find(self.weighted_set[:, j_sample] > 0)[0]

            r2 = - np.log(np.multiply(u3[feature_id, :], u4[feature_id, :]))
            t_matrix = np.floor(np.divide(np.matlib.repmat(np.log(self.weighted_set[feature_id, j_sample].todense()), 1,
                                                           self.dimension_num), r2) + beta2[feature_id, :])
            z_matrix = np.exp(np.multiply(r2, (t_matrix - beta2[feature_id, :] + 1)))
            a_matrix = np.divide(- np.log(np.multiply(v1[feature_id, :], v2[feature_id, :])), z_matrix)

            min_position = np.argmin(a_matrix, axis=0)
            fingerprints_k[j_sample, :] = feature_id[min_position]

            r1 = - np.log(np.multiply(u1[feature_id[min_position], :], u2[feature_id[min_position], :]))
            gamma1 = np.array([-np.log(np.diag(r1[0]))])

            b = np.array([np.diag(beta1[feature_id[min_position], :][0])])
            t_matrix = np.floor(np.divide(np.log(np.transpose(self.weighted_set[feature_id[min_position], j_sample]
                                                              .todense())), gamma1) + b)
            fingerprints_y[j_sample, :] = np.exp(np.multiply(gamma1, (t_matrix - b)))

        elapsed = time.time() - start

        return fingerprints_k, fingerprints_y, elapsed

    def scws(self, repeat=1, scale=1):
        """[Shrivastava, 2016] uniformly samples the area which is composed of the upper bound of each element
           in the universal set by simulating rejection sampling.
           A. Shrivastava, "Simple and Efficient Weighted Minwise Hashing", in NIPS, 2016, pp. 1498-1506.

        Parameters
        ----------
        scale: int
            a constant to adapt the weight

        repeat: int, default: 1
            the number of repeating the algorithm as the part of the seed of the random number generator

        Returns
        ----------
        fingerprints: ndarray, shape (n_instances, dimension_num)
            hash codes for data matrix, where row represents a data instance

        elapsed: float
            time of hashing data matrix
        """
        fingerprints = np.zeros((self.instance_num, self.dimension_num))

        start = time.time()

        bound = np.ceil(np.max(self.weighted_set * scale, 1).todense()).astype(int)
        m_max = np.sum(bound)
        seed = np.arange(1, self.dimension_num+1)

        comp_to_m = np.zeros((1, self.feature_num), dtype=int)
        int_to_comp = np.zeros((1, m_max), dtype=int)
        i_dimension = 0
        for i in range(0, m_max):
            if i == comp_to_m[0, i_dimension] and i_dimension < self.feature_num-1:
                i_dimension = i_dimension + 1
                comp_to_m[0, i_dimension] = comp_to_m[0, i_dimension - 1] + bound[i_dimension - 1, 0]
            int_to_comp[0, i] = i_dimension - 1

        for j_sample in range(0, self.instance_num):
            instance = (scale * self.weighted_set[:, j_sample]).todense()

            for d_id in range(0, self.dimension_num):
                np.random.seed(seed[d_id] * np.power(2, repeat - 1))
                while True:
                    rand_num = np.random.uniform(1, m_max)
                    rand_floor = np.floor(rand_num).astype(int)
                    comp = int_to_comp[0, rand_floor]
                    if rand_num <= comp_to_m[0, comp] + instance[comp]:
                        break
                    fingerprints[j_sample, d_id] = fingerprints[j_sample, d_id] + 1

        elapsed = time.time() - start

        return fingerprints, elapsed

"""

***CWSlib.py使用函数注释***

*numpy.dot(a, b)
   - 功能：计算两个数组的点积。
   - 参数：
     - a：数组，第一个参数。
     - b：数组，第二个参数。
   - 返回值：
     - 输出：数组，a和b的点积结果。
   - 异常：
     - ValueError：如果a的最后一个维度的大小与b的倒数第二个维度的大小不相同。

*numpy.ones(shape, dtype=None, order='C')
   - 功能：返回一个给定形状和类型的新数组，并用1填充。
   - 参数：
     - shape：int或int序列，新数组的形状。
     - dtype：数据类型，可选，默认为numpy.float64。
     - order：{‘C’, ‘F’}，可选，默认为‘C’，指定在内存中存储多维数据的顺序。
   - 返回值：
     - out：ndarray，形状为shape，类型为dtype的全1数组。

*numpy.mod(x1, x2[, out])
   - 功能：按元素返回除法的余数。
   - 参数：
     - x1：数组，被除数数组。
     - x2：数组，除数数组。
     - out：ndarray，可选，将输出放入其中的数组。
   - 返回值：
     - Y：ndarray，商的余数部分x1/x2，按元素划分。
   
*numpy.zeros(shape, dtype=float, order='C')
   - 功能：返回一个给定形状和类型的新数组，并用0填充。
   - 参数：
     - shape：int或int序列，新数组的形状。
     - dtype：数据类型，可选，默认为numpy.float64。
     - order：{‘C’, ‘F’}，可选，默认为‘C’，指定在内存中存储多维数据的顺序。
   - 返回值：
     - out：ndarray，形状为shape，类型为dtype的全0数组。

*numpy.ctypeslib.ndpointer(dtype=None, ndim=None, shape=None, flags=None)
   - 功能：数组检查restype/argtypes。
   - 参数：
     - dtype：数据类型，可选，数组的数据类型。
     - ndim：int，可选，数组的维度数。
     - shape：int序列，可选，数组的形状。
     - flags：str或str元组，可选，数组的标志。
   - 返回值：
     - klass：ndpointer类型对象，包含dtype、ndim、shape和flags信息。

*numpy.array(object, dtype=None, copy=True, order=None, subok=False, ndmin=True)
   - 功能：创建一个数组。
   - 参数：
     - object：数组、可暴露数组接口的任何对象、其__array__方法返回数组的对象，或任何（嵌套的）序列。
     - dtype：数据类型，可选，数组的数据类型。
     - copy：bool，可选，默认为True，如果为True，则复制对象。否则，仅在必要时进行复制。
     - order：{‘C’, ‘F’, ‘A’}，可选，指定数组的顺序。
     - subok：bool，可选，默认为False，如果为True，则子类将被传递，否则返回的数组将被强制为基类数组。
     - ndmin：int，可选，默认为True，指定结果数组应具有的最小维数。
   - 返回值：
     - 返回创建的数组对象。

*numpy.random.seed(seed=None)
   - 功能：为随机数生成器设置种子。
   - 参数：
     - seed：int或array_like，可选，生成器的种子。
   
*numpy.random.uniform(low=0.0, high=1.0, size=1)
   - 功能：从均匀分布中抽取样本。
   - 参数：
     - low：float，可选，默认为0.0，输出间隔的下限。
     - high：float，输出间隔的上限。
     - size：int或int元组，可选，输出的形状。
   - 返回值：
     - out：ndarray，抽取的样本。

*numpy.random.beta(a, b, size=None)
   - 功能：从Beta分布中抽取样本。
   - 参数：
     - a：float，Alpha参数，非负。
     - b：float，Beta参数，非负。
     - size：int或int元组，可选，要抽取的样本数。
   - 返回值：
     - out：ndarray，抽取的样本数组。

*numpy.random.gamma(shape, scale=1.0, size=None)
    - 功能：从Gamma分布中抽取样本。
    - 参数：
      - shape：scalar > 0，Gamma分布的形状参数。
      - scale：scalar > 0，可选，默认为1.0，Gamma分布的尺度参数。
      - size：shape_tuple，可选，输出形状。
    - 返回值：
      - out：ndarray，抽取的样本。

*numpy.power(x1, x2[, out])
    - 功能：返回从第二个数组提升到电源的元素基数组。
    - 参数：
      - x1：array_like，底数。
      - x2：array_like，指数。
      - out：ndarray，可选，输出数组。
    - 返回值：
      - y：ndarray，x1中的每个底数提高到x2中指数的幂。

*numpy.log(x[, out])
    - 功能：自然对数，元素方面。
    - 参数：
      - x：array_like，输入值。
      - out：ndarray，可选，输出数组。
    - 返回值：
      - y：ndarray，x的自然对数，逐元素计算。

*numpy.floor(x[, out])
    - 功能：逐个元素返回输入的下限。
    - 参数：
      - x：array_like，输入数据。
      - out：ndarray，可选，输出数组。
    - 返回值：
      - y：ndarray，x中每个元素的下限值。

*numpy.divide(x1, x2[, out])
    - 功能：按元素进行除法。
    - 参数：
      - x1：array_like，被除数数组。
      - x2：array_like，除数数组。
      - out：ndarray，可选，输出数组。
    - 返回值：
      - y：ndarray，x1除以x2的商，按元素计算。

*numpy.exp(x[, out])
    - 功能：计算输入数组中所有元素的指数。
    - 参数：
      - x：array_like，输入值。
      - out：ndarray，可选，输出数组。
    - 返回值：
      - out：ndarray，x的元素指数，逐元素计算。

*numpy.multiply(x1, x2[, out])
    - 功能：按元素相乘。
    - 参数：
      - x1, x2：array_like，输入数组。
      - out：ndarray，可选，输出数组。
    - 返回值：
      - y：ndarray，x1和x2的乘积，按元素计算。

*numpy.argmin(a, axis=None)
    - 功能：沿指定轴返回最小值的索引。
    - 参数：
      - a：array_like，输入数据。
      - axis：int或元组，可选，默认为None，在哪个轴上查找最小值。
    - 返回值：
      - indices：ndarray，最小值的索引。

*numpy.arange([start,] stop[, step,], dtype=None)
    - 功能：返回在给定的时间间隔内的均匀分布的值。
    - 参数：
      - start：number，可选，默认为0，间隔的起始值。
      - stop：number，间隔的结束值。
      - step：number，可选，默认为1，值之间的间隔。
      - dtype：dtype，返回数组的数据类型。
    - 返回值：
      - out：ndarray，均匀分布的值。

*numpy.diag(v, k=0)
    - 功能：提取对角线或构造对角线数组。
    - 参数：
      - v：array_like，如果v是2-D数组，则返回其第k个对角线的副本。如果v是1-D数组，则返回具有v在第k个对角线上的2-D数组。
      - k：int，可选，默认为0，对角线的偏移量。
    - 返回值：
      - out：ndarray，提取的对角线或构造的对角线数组。

*numpy.transpose(a, axes=None)
    - 功能：置换数组的维度。
    - 参数：
      - a：array_like，输入数组。
      - axes：int列表，可选，默认为None，指定要置换的轴。
    - 返回值：
      - p：ndarray，a的轴被置换后的数组。

*numpy.ceil(x[, out])
    - 功能：逐个元素返回输入的上限。
    - 参数：
      - x：array_like，输入数据。
      - out：ndarray，可选，输出数组。
    - 返回值：
      - y：ndarray，x中每个元素的上限值。

*numpy.max(a, axis=None, out=None, keepdims=False, initial=<no value>, where=<no value>)
    - 功能：返回数组或沿轴的最大值。
    - 参数：
      - a：array_like，输入数据。
      - axis：int或元组，可选，默认为None，沿着哪个轴计算最大值。
      - out：ndarray，可选，输出数组。
      - keepdims：bool，可选，默认为False，如果为True，则保持沿着轴被减少的维度。
      - initial：scalar，可选，最小输出元素的值。
      - where：array_like，可选，用于比较最大值的元素。
    - 返回值：
      - max：ndarray或scalar，a的最大值。

*numpy.sum(a, axis=None, dtype=None, out=None)
    - 功能：计算给定轴上数组元素的总和。
    - 参数：
      - a：array_like，要求和的元素。
      - axis：int，可选，默认为None，沿着哪个轴计算总和。
      - dtype：dtype，可选，返回数组和累加器的数据类型。
      - out：ndarray，可选，用于放置输出的数组。
    - 返回值：
      - sum_along_axis：ndarray，a的指定轴被移除后的数组，如果a是0维数组或axis为None，则返回标量。

*time.time
    - 功能：函数返回当前时间的时间戳，即从1970年1月1日午夜（UTC/GMT的时间）到当前时间的秒数，浮点数形式。

*CDLL
    - 功能：CDLL是Python中用于加载共享库（动态链接库）的模块。它通常与Ctypes模块一起使用，用于调用C函数库中的函数。CDLL是Ctypes模块中的一种加
    载共享库的方式，它是一种使用标准C函数调用约定（C函数调用约定）的方式加载共享库


***测试程序使用函数注释***

*scipy.sparse.find(A)
    - 功能：返回矩阵的非零元素索引和值。
    - 参数：
      - A：稠密或稀疏数组或矩阵，要查找其非零元素的矩阵。
    - 返回值：
      - (I, J, V)：元组，包含非零元素的行索引、列索引和值。
      
*os.path.basename(path)
    - 功能：返回文件名。
    - 参数：
      - path：需要获取文件名或文件夹名的路径字符串。
    - 返回值：
      - 返回路径中最后一个文件或文件夹的名称，如果路径为空则返回 '.'。

*scipy.io.loadmat(file_name, mdict=None, appendmat=True,kwargs)
    - 功能：加载MATLAB文件。
    - 参数：
      - file_name: 文件名。
      - mdict: 可选，用于存储数据的字典。
      - appendmat: 可选，是否在文件名末尾追加 '.mat' 扩展名。
      - mat_dtype: 可选，如果为 True，则返回与保存到 MATLAB 中相同的 dtype。
    - 返回值：
      - mat_dict: 字典，变量名作为键，加载的矩阵作为值。
      
*scipy.io.savemat(file_name, mdict, appendmat=True, format='5', long_field_names=False, do_compression=False, oned_as='row')
    - 功能：将名称和数组的字典保存到 MATLAB 格式的 .mat 文件中。
    - 参数：
      - file_name: 字符串或类文件对象，.mat 文件的名称。
      - mdict: 要保存到 mat 文件的字典。
      - appendmat: 可选，如果为 True，则在给定的文件名末尾追加 '.mat' 扩展名。
      - format: 可选，'5' 表示 MATLAB 5 及更高版本，'4' 表示 MATLAB 4 .mat 文件。
      - long_field_names: 可选，如果为 True，则结构中的最大字段名长度为 63 个字符。
      - do_compression: 可选，是否压缩写入的矩阵。
      - oned_as: 可选，如果为 'column'，则将 1-D NumPy 数组写为列向量，如果为 'row'，则写为行向量。

*os.makedirs
    - 功能：用于递归创建目录。
    - 参数：
      - path: 需要递归创建的目录，可以是相对或绝对路径。
      - mode: 权限模式，默认为 0o777。

*os.path.join
    - 功能：将目录和文件名合成为一个路径。

*csr_matrix
    - 功能：压缩稀疏行矩阵。
    - 参数：
      - arg1: 可以通过多种方式实例化。
    - 返回值：
      - csr_matrix 对象。

"""

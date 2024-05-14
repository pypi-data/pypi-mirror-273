#cwslib

**Introduction**

This module contains the following algorithms: the standard MinHash algorithm for binary sets andseveral Consistent 
Weighted Sampling algorithms(CWS、ICWS、I2CWS、PCWS、CCWS、0-bit CWS、SCWS).

Each algorithm converts a data instance (i.e., vector) into the hash code of the specified length,and computes the 
time of encoding.

**Installation**

    pip install cwslib
    
The homepage of the toolbox is [here](https://github.com/jiangli0618/cwslib).

**Usage**

    # Input data: {array-like, sparse matrix}, shape (n_features, n_instances), format='csc'
    # a data matrix where row represents feature and column is data instance
    # Import necessary libraries/modules

    from os.path import basename
    import cwslib
    import scipy.io as scio
    from cwslib.CWSlib import ConsistentWeightedSampling
    from scipy.io import savemat
    import os
    from scipy.sparse import csr_matrix
    
    # List of MATLAB file paths containing data
    mat_files = [···]
    
    # Iterate over each MATLAB file
    for mat_file in mat_files:
        # Load data from MATLAB file
        mat_data = scio.loadmat(mat_file)
        # Extract the 'jaccard' array from loaded data
        arr = mat_data['jaccard']
        # Convert the array data into a Compressed Sparse Row matrix
        data = csr_matrix(arr)
        # Iterate over a range of dimension numbers
        for dimension_num in range(10, 100, 10):
            # Apply the Weighted MinHash algorithm to generate fingerprints
            cws = cwslib.CWSlib.ConsistentWeightedSampling(data, dimension_num)
            fingerprints_k, fingerprints_y, elapsed = cws.algorithms-name()
            # Print information about the current process
            print(str(basename(mat_file)), 'dimension_num =', dimension_num, 'algorithms-name-elapsed = ', elapsed, '秒')
            # Define the path to save the generated MATLAB files
            save_path = "D:\\desktop\\mat\\"
            # Create the directory if it doesn't exist
            os.makedirs(save_path, exist_ok=True)
            # Construct the file name for the saved MATLAB file
            file_name = str(basename(mat_file)) + '-cws-' + str(dimension_num) + '.mat'
            # Combine the directory path and file name
            file_path = os.path.join(save_path, file_name)
            # Save the fingerprints into a new MATLAB file
            savemat(file_path, {'fingerprints_k': fingerprints_k, 'fingerprints_y': fingerprints_y})



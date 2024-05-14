# Bird-Eye-View
The Bird's Eye View (BEV) technique is a cutting-edge approach for feature selection (FS), particularly effective in dealing with high-dimensional data. The method's core objective is to identify and eliminate irrelevant features that could hinder machine learning models' accuracy. Removing unimportant features contributes significantly to the models' optimal fit and improve predictive power. The BEV approach has been extensively evaluated against other advanced feature selection methods, with consistently superior results in terms of model accuracy and selected numbers of features. The BEV methodology employs a combination of modern techniques, including evolutionary algorithms, Markov chain, reinforcement learning, and genetic algorithms, that synergistically improve its effectiveness. 

# Requirements
The following libraries are required to use the BEV methodology
* scikit_learn
* pandas
* numpy
* matplotlib

# Instructions to use BEVFS

*	Import bevfs_algorithm function from bevfs.
*	Specify the full data file path.
*	It will start feature selection process.
*	Upon completion of the feature selection process, the selected feature file will be automatically saved in the "best features" folder, located in the root directory of the project.
*	The detailed statistics for each selected features file, including the experiment number, stage number, accuracy, and number of features, will be embedded in the data file name.

# Example
```
from bevfs import bevfs_algorithm

bevfs_algorithm("/data.txt") # It should be comma seperated file.
```

# Data preparation Guidance
*	The data must be in CSV format.
*	There should be one header row.
*	The output column should be placed as the first column (i.e., zero index) in the file.
*	There can be any number of input columns as needed.

It is recommended to perform some basic data exploration and cleaning to ensure the data is accurate, consistent, and free from errors.

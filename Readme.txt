************* Model **********

To classify the given log entry into correct class: either books, music, videos or rest.
For this purpose an ANN with 1 hidden layer is built. The rational behind going for a NN is that the volume of data is large enough to fully consume my RAM. Hence, wanted to use some model where training can be done using mini-batchs. Hence, ANNs were used. The hidden layer consists of 128 nodes and the output layer consists of 4 nodes (depends on number of classes). Relu activation was used for the hidden layer whereas softmax was used on the output layer since we wanted to get the ouput probabilities for each class. 

*********** Training & Testing **********

The entire dataset was split into 61 small chunks of size 10000. 5 models were built for the experiment and the data for training each model were these chunks which were randomly sampled. The training data for each model had 50 such chunks whereas rest 11 chunks were used for testing out the model. While training to induce more randomness in the training, from each chunk, batches of size 64 were randomly sampled and were fed as input to the model. So actually the model was trained on batches of size 64.
All the 5 models performed well with very little difference in performance. The 5th model was taken as the final one since its accuracy score was marginally better than the others.
Training data can be found in folder "instances" and inside "train".
Testing data can be found in folder "instances" and inside "test".

The final evaluation data can be found in folder submission.
Submission model: "model"
Submission output file: "submissions.csv"

******** Observations **************

It was noted that the given dataset suffers class imbalance slightly. File: Class_count.png The "rest" class dominates over the other 3 classes. So, inorder to tackle class imbalance, additional cost/weights were given to the other 3 classes, i.e., if the model makes an error the minority 3 classes the model is penalized double than what it would have got for making a mistake on the majority class. In such cases actually a better metric would have been check for the precision and recall and then calculate F-scores.

********* Pre-processing ***********

For the purpose of training only the "additional attributes" and "breadcrumbs" were used. The vector representation created for "additional attributes" was a binary representation i.e., if the "publisher" attributes exist or not, "release date" is present or not. In case of "breadcrumbs" a term frequency representation was used. Both these were concatenated to get the final representation.

Actually the breadcrumbs could have been treated as a sentence (sequential data) and better features such as n-grams could have been used. But due to time constraints, I have just taken frequency counts.

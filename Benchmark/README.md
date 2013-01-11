Benchmarks
==========

This folder contains a couple very basic benchmarks to provide examples of reading in the data and creating a submission.

Executing these benchmarks requires python along with the pandas package.

To run them,

1. [Download the data](https://www.kaggle.com/c/event-recommendation-engine-challenge/data)
2. Modify the get_paths function in util.py to point to the data path and the submission output path on your system
3. Run the benchmarks by executing the corresponding script (e.g. `python event_popularity_benchmark.py`)
4. [Make a submission](https://www.kaggle.com/c/event-recommendation-engine-challenge/submissions/attach) with the output file

The benchmarks are:

 - **event_popularity_benchmark.py**: recommends events according to the popularity of the event
 - **random_order_benchmark.py**: recommend events in a random order
 - **given_order_benchmark.py**: recommend events in the order in which they are provided
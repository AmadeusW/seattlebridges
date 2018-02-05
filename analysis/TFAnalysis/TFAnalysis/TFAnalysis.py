import tensorflow as tf
from sklearn.model_selection import train_test_split
from DataProcessor import processTweets
from tfutils import tfutils

'''
# Uncomment this section to create data and labels based on human readable data
fullLabels, fullData = processTweets(r'C:\src\seattlebridges\collector\tweets.csv')
tfutils.storeData(fullLabels, r'analysis\TweetData\fullLabels.txt')
tfutils.storeData(fullData, r'analysis\TweetData\fullData.txt')
'''

loadedLabels = tfutils.loadData(r'analysis\TweetData\fullLabels.txt')
loadedData = tfutils.loadData(r'analysis\TweetData\fullData.txt')
trainData, testData, trainLabels, testLabels= train_test_split(
    loadedData, loadedLabels, test_size=0.33, random_state=42)

graph = tf.Graph()
with graph.as_default():
    input = tf.placeholder(tf.float32, shape=(None, 115))
    labels = tf.placeholder(tf.float32, shape=(None, 7))

    layer1_weights = tf.Variable(tf.random_normal([115, 7]))
    layer1_bias = tf.Variable(tf.zeros([7]))

    logits = tf.matmul(input, layer1_weights) + layer1_bias
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=labels))

    learning_rate = 0.01
    optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

    with tf.Session(graph=graph) as session:
        tf.global_variables_initializer().run()

        num_steps = 1000
        batch_size = 100
        for step in range(num_steps):
            offset = (step * batch_size) % (trainLabels.shape[0] - batch_size) # todo: what is shape[0]?
            batch_images = trainData[offset:(offset + batch_size), :]
            batch_labels = trainLabels[offset:(offset + batch_size), :]
            feed_dict = {input: batch_images, labels: batch_labels}

            o, c, = session.run([optimizer, cost], feed_dict=feed_dict)
            print("Cost: ", c)
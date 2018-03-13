
#import input data
import input_data
mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)

#gets rid of some stupid warning about CPU extensions
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

#import tensorflow
import tensorflow as tf

#set parameters
learning_rate = 0.01
training_iteration = 30
batch_size = 100
display_step = 2

#tf graph input
x = tf.placeholder("float", [None, 784]) #mnist data image of shape 28*28=784
y = tf.placeholder("float", [None, 10]) #0-9 digits --> 10 possible outputs, 10 classes

#Create Model

#set model weights
W = tf.Variable(tf.zeros([784,10]))
b = tf.Variable(tf.zeros([10]))

with tf.name_scope("Wx_b") as scope:
    #construct a linear model
    model = tf.nn.softmax(tf.matmul(x,W) + b)

#add summary of operations to collect data
w_h = tf.summary.histogram("weights", W)
b_h = tf.summary.histogram("biases", b)

#more name scopes will clean up graph representation
with tf.name_scope("cost_function") as scope:
    #minimize error using cross entropy
    #Cross entropy
    cost_function = -tf.reduce_sum(y*tf.log(model)) #this is us setting the cost function
    #create a summary to moniter the cost function
    tf.summary.scalar("cost_function", cost_function)

with tf.name_scope("train") as scope:
    #Gradient descent
    optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost_function)

#initializing the variables
init = tf.global_variables_initializer()

#merge all summaries into a single operator because we are very lazy
merged_summary_op = tf.summary.merge_all()

#Launch the graph Baby!
with tf.Session() as sess:
    sess.run(init)

#set the logs writer to the folder /tmp/tensorflow_logs
    summary_writer = tf.summary.FileWriter("/Users/scarere/Documents/PycharmProjects/TensorFlowTest", graph=sess.graph)

    #Training Cycle
    for iteration in range(training_iteration):
        avg_cost = 0.
        total_batch = int(mnist.train.num_examples/batch_size)
        #Loop over all batches
        for i in range(total_batch):
            batch_xs, batch_ys = mnist.train.next_batch(batch_size)
            #fit training using batch data
            sess.run(optimizer, feed_dict={x: batch_xs, y: batch_ys}) #uses batch data and gradient operation for back propagation
            #compute the average loss
            avg_cost += sess.run(cost_function, feed_dict={x: batch_xs, y: batch_ys})/total_batch
            #write logs for each iteration so we can keep track of whats going on
            summary_str = sess.run(merged_summary_op, feed_dict={x: batch_xs, y: batch_ys})
            summary_writer.add_summary(summary_str, iteration*total_batch + i)
        #display logs per iteration step
        if iteration % display_step == 0:
            print("Iteration:", "%04d" % (iteration+1), "cost =", "{:.9f}".format(avg_cost))

    print("Training Complete!")

    #Now lets test model
    predictions = tf.equal(tf.argmax(model, 1), tf.argmax(y, 1)) #compares model values to output values y
    #calculate accuracy
    accuracy = tf.reduce_mean(tf.cast(predictions, "float"))

    print("Accuracy:", sess.run(accuracy, {x: mnist.test.images, y: mnist.test.labels}))


#print("Accuracy: ", tf.metrics.accuracy())


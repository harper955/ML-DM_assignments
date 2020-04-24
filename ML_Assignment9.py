#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# ## 1

# In[ ]:


def load_data(filepath):
  df = pd.read_csv(filepath)
  df.head()
  Y = df['5'].to_numpy()
  del df['5']
  X=df.to_numpy()
  return X, Y


# In[ ]:


X, y = load_data("mnist_train.csv")
X_train, X_test, y_train, y_test = train_test_split(                X, y, test_size=0.3, random_state=42)
#One hot encoding of training labels 
Labels=pd.get_dummies(y_train)


# ## 2

# In[ ]:


class Perceptron():
    def __init__(self,x,y):
        """
        x is 2d array of input images
        y are one hot encoded labels 
        """
        self.x=x/255   # Divide by 255 to normalise the pixel values (0-255)
        self.y=y
        self.weights=[]
        self.bias=[]
        self.outputs=[]
        self.derivatives=[]
        self.activations=[]
        
    def connect(self,layer1,layer2):
        """layer 2 of shape 1xn"""
        #Initialise weights,derivatives and activation lists
        self.derivatives.append(np.random.uniform(0,0.1,size=(layer1.shape[1]+1,layer2.shape[1])))
        self.weights.append(np.random.uniform(-1,1,size=(layer1.shape[1]+1,layer2.shape[1])))
        self.bias.append(np.random.uniform(-1,1,size=(layer1.shape[1]+1,layer2.shape[1])))


    def softmax(self,z):
        e=np.exp(z)
        return e/np.sum(e,axis=1).reshape(-1,1) 
    
    def max_log_likelihood(self,y_pred,y):
        """cross entropy"""
        return y*np.log(y_pred)
    
    def delta_mll(self,y,y_pred):
        """derivative of cross entropy"""
        #return y*(y_pred-1)
        return y_pred-y
    
    def forward_pass(self,x,y,weights,bias):
        cost=0
        self.outputs=[]
        for i in range(len(weights)):
            samples=len(x)
            ones_array=np.ones(samples).reshape(samples,1)
            self.outputs.append(x) #append without adding ones array
            z=np.dot(np.append(ones_array,x,axis=1),weights[i]+bias[i])
            x=self.softmax(z)
        self.outputs.append(x)
        self.y_pred=x
        temp=-self.max_log_likelihood(self.y_pred,y)
        cost=np.mean(np.sum(temp,axis=1))
        return cost
    
    
    def backward_pass(self,y,lr):
        for i in range(len(self.weights)-1,-1,-1):
            ones_array=np.ones(len(n.outputs[i])).reshape(len(n.outputs[i]),1)
            prev_term=self.delta_mll(y,self.y_pred)  
            # derivatives follow specific order,last three terms added new,rest from previous term  
            self.derivatives[i]=np.dot(prev_term.T,np.append(ones_array,self.outputs[i],axis=1))   
            self.weights[i]=self.weights[i]-lr*((self.derivatives[i].T)/len(y))
            self.bias[i]=self.bias[i]-lr*((self.derivatives[i].T)/len(y))
    
    def train(self,batches,lr=1e-3,epoch=10):
        """number of batches to split data in,Learning rate and epochs"""
        for epochs in range(epoch):
            samples=len(self.x)
            c=0
            for i in range(batches):
              x_batch=self.x[int((samples/batches)*i):int((samples/batches)*(i+1))]
              y_batch=self.y.loc[int((samples/batches)*i):int((samples/batches)*(i+1))-1]
              
              c=self.forward_pass(x_batch,y_batch,self.weights,self.bias)
              self.backward_pass(y_batch,lr)
            print(epochs,c/batches)
    
    def predict(self,x):
        """input: x_test values"""
        x=x/255
        for i in range(len(self.weights)):
            samples=len(x)
            ones_array=np.ones(samples).reshape(samples,1)
            z=np.dot(np.append(ones_array,x,axis=1),self.weights[i]+self.bias[i])
            x=self.softmax(z) 
        return np.argmax(x,axis=1)


# In[5]:


n=Perceptron(X_train,Labels)
n.connect(X_train,Labels)
n.train(batches=1000,lr=0.2,epoch=30)


# In[6]:


pred=n.predict(X_test)
np.bincount(n.predict(X_test)),np.bincount(y_test)


# In[7]:


print(f"accuracy is {np.bincount(np.abs(y_test-pred))[0]*100/len(y_test)} %")


# ## 3

# In[ ]:


class Layer():
    """
    size: Number of nodes in the hidden layer 
    activation: name of activation function for the layer
    """
    def __init__(self,size,activation='sigmoid'): 
        self.shape=(1,size)
        self.activation=activation
                
class SingleLayerNeuralNetwork():
    def __init__(self,x,y):
        """
        x is 2d array of input images
        y are one hot encoded labels 
        """
        self.x=x/255   # Divide by 255 to normalise the pixel values (0-255)
        self.y=y
        self.weights=[]
        self.bias=[]
        self.outputs=[]
        self.derivatives=[]
        self.activations=[]
        
    def connect(self,layer1,layer2):
        """layer 2 of shape 1xn"""
        #Initialise weights,derivatives and activation lists
        self.derivatives.append(np.random.uniform(0,0.1,size=(layer1.shape[1]+1,layer2.shape[1])))
        self.weights.append(np.random.uniform(-1,1,size=(layer1.shape[1]+1,layer2.shape[1])))
        self.bias.append(np.random.uniform(-1,1,size=(layer1.shape[1]+1,layer2.shape[1])))
        if isinstance(layer2,Layer):
            self.activations.append(layer2.activation)
            
    def activation(self,name,z,derivative=False):
        
        #implementation of various activation functions and their derivatives
        if name=='sigmoid':
            if derivative==False:
                return 1/(1+np.exp(-z))
            else:
                return z*(1-z)
        
    def softmax(self,z):
        e=np.exp(z)
        return e/np.sum(e,axis=1).reshape(-1,1) 
    
    def max_log_likelihood(self,y_pred,y):
        """cross entropy"""
        return y*np.log(y_pred)
    
    def delta_mll(self,y,y_pred):
        """derivative of cross entropy"""
        #return y*(y_pred-1)
        return y_pred-y
    
    def forward_pass(self,x,y,weights,bias):
        cost=0
        self.outputs=[]
        for i in range(len(weights)):
            samples=len(x)
            ones_array=np.ones(samples).reshape(samples,1)
            self.outputs.append(x) #append without adding ones array
            z=np.dot(np.append(ones_array,x,axis=1),weights[i]+bias[i])
            if i==len(weights)-1:
                x=self.softmax(z)
            else:
                x=self.activation(self.activations[i],z)
        self.outputs.append(x)
        self.y_pred=x
        
        temp=-self.max_log_likelihood(self.y_pred,y)
        cost=np.mean(np.sum(temp,axis=1))
        return cost
    
    
    def backward_pass(self,y,lr):
        for i in range(len(self.weights)-1,-1,-1):
            ones_array=np.ones(len(n.outputs[i])).reshape(len(n.outputs[i]),1)
            if i==len(self.weights)-1:
                prev_term=self.delta_mll(y,self.y_pred)  
                # derivatives follow specific order,last three terms added new,rest from previous term  
                self.derivatives[i]=np.dot(prev_term.T,np.append(ones_array,self.outputs[i],axis=1))   
            else:
                prev_term=np.dot(prev_term,self.weights[i+1][1:].T)*self.activation(self.activations[i],self.outputs[i+1],derivative=True)
                self.derivatives[i]=np.dot(prev_term.T,np.append(ones_array,self.outputs[i],axis=1))
            self.weights[i]=self.weights[i]-lr*((self.derivatives[i].T)/len(y))
            self.bias[i]=self.bias[i]-lr*((self.derivatives[i].T)/len(y))
                
    
    def train(self,batches,lr=1e-3,epoch=10):
        """number of batches to split data in,Learning rate and epochs"""
        for epochs in range(epoch):
            samples=len(self.x)
            c=0
            for i in range(batches):
              x_batch=self.x[int((samples/batches)*i):int((samples/batches)*(i+1))]
              y_batch=self.y.loc[int((samples/batches)*i):int((samples/batches)*(i+1))-1]
              
              c=self.forward_pass(x_batch,y_batch,self.weights,self.bias)
              self.backward_pass(y_batch,lr)
            print(epochs,c/batches)
    
    def predict(self,x):
        """input: x_test values"""
        x=x/255
        for i in range(len(self.weights)):
            samples=len(x)
            ones_array=np.ones(samples).reshape(samples,1)
            z=np.dot(np.append(ones_array,x,axis=1),self.weights[i]+self.bias[i])
            if i==len(self.weights)-1:
                x=self.softmax(z)
            else:
                x=self.activation(self.activations[i],z)

        return np.argmax(x,axis=1)


# In[9]:


n=SingleLayerNeuralNetwork(X_train,Labels)
l1=Layer(100)
n.connect(X_train,l1)
n.connect(l1,Labels)
n.train(batches=1000,lr=0.1,epoch=50)


# In[10]:


pred=n.predict(X_test)
np.bincount(n.predict(X_test)),np.bincount(y_test)


# In[11]:


print(f"accuracy is {np.bincount(np.abs(y_test-pred))[0]*100/len(y_test)} %")


# ## 4

# In[ ]:


class Layer():
    """
    size: Number of nodes in the hidden layer 
    activation: name of activation function for the layer
    """
    def __init__(self,size,activation='sigmoid'): 
        self.shape=(1,size)
        self.activation=activation
                
class DoubleLayerNeuralNetwork():
    def __init__(self,x,y):
        """
        x is 2d array of input images
        y are one hot encoded labels 
        """
        self.x=x/255   # Divide by 255 to normalise the pixel values (0-255)
        self.y=y
        self.weights=[]
        self.bias=[]
        self.outputs=[]
        self.derivatives=[]
        self.activations=[]
        
    def connect(self,layer1,layer2):
        """layer 2 of shape 1xn"""
        #Initialise weights,derivatives and activation lists
        self.derivatives.append(np.random.uniform(0,0.1,size=(layer1.shape[1]+1,layer2.shape[1])))
        self.weights.append(np.random.uniform(-1,1,size=(layer1.shape[1]+1,layer2.shape[1])))
        self.bias.append(np.random.uniform(-1,1,size=(layer1.shape[1]+1,layer2.shape[1])))
        if isinstance(layer2,Layer):
            self.activations.append(layer2.activation)
            
    def activation(self,name,z,derivative=False):
        
        #implementation of various activation functions and their derivatives
        if name=='sigmoid':
            if derivative==False:
                return 1/(1+np.exp(-z))
            else:
                return z*(1-z)
        
    def softmax(self,z):
        e=np.exp(z)
        return e/np.sum(e,axis=1).reshape(-1,1) 
    
    def max_log_likelihood(self,y_pred,y):
        """cross entropy"""
        return y*np.log(y_pred)
    
    def delta_mll(self,y,y_pred):
        """derivative of cross entropy"""
        #return y*(y_pred-1)
        return y_pred-y
    
    def forward_pass(self,x,y,weights,bias):
        cost=0
        self.outputs=[]
        for i in range(len(weights)):
            samples=len(x)
            ones_array=np.ones(samples).reshape(samples,1)
            self.outputs.append(x) #append without adding ones array
            z=np.dot(np.append(ones_array,x,axis=1),weights[i]+bias[i])
            if i==len(weights)-1:
                x=self.softmax(z)
            else:
                x=self.activation(self.activations[i],z)
        self.outputs.append(x)
        self.y_pred=x
        
        temp=-self.max_log_likelihood(self.y_pred,y)
        cost=np.mean(np.sum(temp,axis=1))
        return cost
    
    
    def backward_pass(self,y,lr):
        for i in range(len(self.weights)-1,-1,-1):
            ones_array=np.ones(len(n.outputs[i])).reshape(len(n.outputs[i]),1)
            if i==len(self.weights)-1:
                prev_term=self.delta_mll(y,self.y_pred)  
                # derivatives follow specific order,last three terms added new,rest from previous term  
                self.derivatives[i]=np.dot(prev_term.T,np.append(ones_array,self.outputs[i],axis=1))   
            else:
                prev_term=np.dot(prev_term,self.weights[i+1][1:].T)*self.activation(self.activations[i],self.outputs[i+1],derivative=True)
                self.derivatives[i]=np.dot(prev_term.T,np.append(ones_array,self.outputs[i],axis=1))
            self.weights[i]=self.weights[i]-lr*((self.derivatives[i].T)/len(y))
            self.bias[i]=self.bias[i]-lr*((self.derivatives[i].T)/len(y))
                
    
    def train(self,batches,lr=1e-3,epoch=10):
        """number of batches to split data in,Learning rate and epochs"""
        for epochs in range(epoch):
            samples=len(self.x)
            c=0
            for i in range(batches):
              x_batch=self.x[int((samples/batches)*i):int((samples/batches)*(i+1))]
              y_batch=self.y.loc[int((samples/batches)*i):int((samples/batches)*(i+1))-1]
              
              c=self.forward_pass(x_batch,y_batch,self.weights,self.bias)
              self.backward_pass(y_batch,lr)
            print(epochs,c/batches)
    
    def predict(self,x):
        """input: x_test values"""
        x=x/255
        for i in range(len(self.weights)):
            samples=len(x)
            ones_array=np.ones(samples).reshape(samples,1)
            z=np.dot(np.append(ones_array,x,axis=1),self.weights[i]+self.bias[i])
            if i==len(self.weights)-1:
                x=self.softmax(z)
            else:
                x=self.activation(self.activations[i],z)
        return np.argmax(x,axis=1)


# In[13]:


n=DoubleLayerNeuralNetwork(X_train,Labels)
l1=Layer(100)
l2=Layer(100)
n.connect(X_train,l1)
n.connect(l1,l2)
n.connect(l2,Labels)
n.train(batches=1000,lr=0.1,epoch=20)


# In[14]:


pred=n.predict(X_test)
np.bincount(n.predict(X_test)),np.bincount(y_test)


# In[15]:


print(f"accuracy is {np.bincount(np.abs(y_test-pred))[0]*100/len(y_test)} %")


# ## 5

# In[ ]:


class Layer():
    """
    size: Number of nodes in the hidden layer 
    activation: name of activation function for the layer
    """
    def __init__(self,size,activation='sigmoid'): 
        self.shape=(1,size)
        self.activation=activation
                
class NeuralNetworkActivations():
    def __init__(self,x,y):
        """
        x is 2d array of input images
        y are one hot encoded labels 
        """
        self.x=x/255   # Divide by 255 to normalise the pixel values (0-255)
        self.y=y
        self.weights=[]
        self.bias=[]
        self.outputs=[]
        self.derivatives=[]
        self.activations=[]
        
    def connect(self,layer1,layer2):
        """layer 2 of shape 1xn"""
        #Initialise weights,derivatives and activation lists
        self.derivatives.append(np.random.uniform(0,0.1,size=(layer1.shape[1]+1,layer2.shape[1])))
        self.weights.append(np.random.uniform(-1,1,size=(layer1.shape[1]+1,layer2.shape[1])))
        self.bias.append(np.random.uniform(-1,1,size=(layer1.shape[1]+1,layer2.shape[1])))
        if isinstance(layer2,Layer):
            self.activations.append(layer2.activation)
            
    def activation(self,name,z,derivative=False):
        
        #implementation of various activation functions and their derivatives
        if name=='sigmoid':
            if derivative==False:
                return 1/(1+np.exp(-z))
            else:
                return z*(1-z)
        elif name=='relu':
            if derivative==False:
                return np.maximum(0.0,z)
            else:
              z[z<=0] = 0.0
              z[z>0] = 1.0
              return z
        elif name=='tanh':
          if derivative==False:
                return np.tanh(z)
          else:
                return 1.0 - (np.tanh(z)) ** 2
        
    def softmax(self,z):
        e=np.exp(z)
        return e/np.sum(e,axis=1).reshape(-1,1) 
    
    def max_log_likelihood(self,y_pred,y):
        """cross entropy"""
        return y*np.log(y_pred)
    
    def delta_mll(self,y,y_pred):
        """derivative of cross entropy"""
        #return y*(y_pred-1)
        return y_pred-y
    
    def forward_pass(self,x,y,weights,bias):
        cost=0
        self.outputs=[]
        for i in range(len(weights)):
            samples=len(x)
            ones_array=np.ones(samples).reshape(samples,1)
            self.outputs.append(x) #append without adding ones array
            z=np.dot(np.append(ones_array,x,axis=1),weights[i]+bias[i])
            if i==len(weights)-1:
                x=self.softmax(z)
            else:
                x=self.activation(self.activations[i],z)
        self.outputs.append(x)
        self.y_pred=x
        
        temp=-self.max_log_likelihood(self.y_pred,y)
        cost=np.mean(np.sum(temp,axis=1))
        return cost
    
    
    def backward_pass(self,y,lr):
        for i in range(len(self.weights)-1,-1,-1):
            ones_array=np.ones(len(n.outputs[i])).reshape(len(n.outputs[i]),1)
            if i==len(self.weights)-1:
                prev_term=self.delta_mll(y,self.y_pred)  
                # derivatives follow specific order,last three terms added new,rest from previous term  
                self.derivatives[i]=np.dot(prev_term.T,np.append(ones_array,self.outputs[i],axis=1))   
            else:
                prev_term=np.dot(prev_term,self.weights[i+1][1:].T)*self.activation(self.activations[i],self.outputs[i+1],derivative=True)
                self.derivatives[i]=np.dot(prev_term.T,np.append(ones_array,self.outputs[i],axis=1))
            self.weights[i]=self.weights[i]-lr*((self.derivatives[i].T)/len(y))
            self.bias[i]=self.bias[i]-lr*((self.derivatives[i].T)/len(y))
    
    def train(self,batches,lr=1e-3,epoch=10):
        """number of batches to split data in,Learning rate and epochs"""
        for epochs in range(epoch):
            samples=len(self.x)
            c=0
            for i in range(batches):
              x_batch=self.x[int((samples/batches)*i):int((samples/batches)*(i+1))]
              y_batch=self.y.loc[int((samples/batches)*i):int((samples/batches)*(i+1))-1]
              
              c=self.forward_pass(x_batch,y_batch,self.weights,self.bias)
              self.backward_pass(y_batch,lr)
            print(epochs,c/batches)
    
    def predict(self,x):
        """input: x_test values"""
        x=x/255
        for i in range(len(self.weights)):
            samples=len(x)
            ones_array=np.ones(samples).reshape(samples,1)
            z=np.dot(np.append(ones_array,x,axis=1),self.weights[i]+self.bias[i])
            if i==len(self.weights)-1:
                x=self.softmax(z)
            else:
                x=self.activation(self.activations[i],z)
        return np.argmax(x,axis=1)


# In[17]:


n=NeuralNetworkActivations(X_train,Labels)
l1=Layer(100,'sigmoid')
l2=Layer(50, 'tanh')
n.connect(X_train,l1)
n.connect(l1,l2)
n.connect(l2,Labels)
n.train(batches=1000,lr=0.1,epoch=20)


# In[18]:


pred=n.predict(X_test)
np.bincount(n.predict(X_test)),np.bincount(y_test)


# In[19]:


print(f"accuracy is {np.bincount(np.abs(y_test-pred))[0]*100/len(y_test)} %")


# ## 6

# In[ ]:


class Layer():
    """
    size: Number of nodes in the hidden layer 
    activation: name of activation function for the layer
    """
    def __init__(self,size,activation='sigmoid'): 
        self.shape=(1,size)
        self.activation=activation
                
class NeuralNetworkMomentum():
    def __init__(self,x,y):
        """
        x is 2d array of input images
        y are one hot encoded labels 
        """
        self.x=x/255   # Divide by 255 to normalise the pixel values (0-255)
        self.y=y
        self.weights=[]
        self.bias=[]
        self.outputs=[]
        self.derivatives=[]
        self.activations=[]
        self.delta_weights=[]
        self.delta_bias=[]
        
    def connect(self,layer1,layer2):
        """layer 2 of shape 1xn"""
        #Initialise weights,derivatives and activation lists
        self.derivatives.append(np.random.uniform(0,0.1,size=(layer1.shape[1]+1,layer2.shape[1])))
        self.weights.append(np.random.uniform(-1,1,size=(layer1.shape[1]+1,layer2.shape[1])))
        self.bias.append(np.random.uniform(-1,1,size=(layer1.shape[1]+1,layer2.shape[1])))
        self.delta_weights.append(np.zeros((layer1.shape[1]+1,layer2.shape[1])))
        self.delta_bias.append(np.zeros((layer1.shape[1]+1,layer2.shape[1])))
        if isinstance(layer2,Layer):
            self.activations.append(layer2.activation)
            
    def activation(self,name,z,derivative=False):
        
        #implementation of various activation functions and their derivatives
        if name=='sigmoid':
            if derivative==False:
                return 1/(1+np.exp(-z))
            else:
                return z*(1-z)
        elif name=='relu':
            if derivative==False:
                return np.maximum(0.0,z)
            else:
              z[z<=0] = 0.0
              z[z>0] = 1.0
              return z
        elif name=='tanh':
          if derivative==False:
                return np.tanh(z)
          else:
                return 1.0 - (np.tanh(z)) ** 2
        
    def softmax(self,z):
        e=np.exp(z)
        return e/np.sum(e,axis=1).reshape(-1,1) 
    
    def max_log_likelihood(self,y_pred,y):
        """cross entropy"""
        return y*np.log(y_pred)
    
    def delta_mll(self,y,y_pred):
        """derivative of cross entropy"""
        #return y*(y_pred-1)
        return y_pred-y
    
    def forward_pass(self,x,y,weights,bias):
        cost=0
        self.outputs=[]
        for i in range(len(weights)):
            samples=len(x)
            ones_array=np.ones(samples).reshape(samples,1)
            self.outputs.append(x) #append without adding ones array
            z=np.dot(np.append(ones_array,x,axis=1),weights[i]+bias[i])
            if i==len(weights)-1:
                x=self.softmax(z)
            else:
                x=self.activation(self.activations[i],z)
        self.outputs.append(x)
        self.y_pred=x
        
        temp=-self.max_log_likelihood(self.y_pred,y)
        cost=np.mean(np.sum(temp,axis=1))
        return cost
    
    
    def backward_pass(self,y,lr,momentum=False,beta=0.9):
        for i in range(len(self.weights)-1,-1,-1):
            ones_array=np.ones(len(n.outputs[i])).reshape(len(n.outputs[i]),1)
            if i==len(self.weights)-1:
                prev_term=self.delta_mll(y,self.y_pred)  
                # derivatives follow specific order,last three terms added new,rest from previous term  
                self.derivatives[i]=np.dot(prev_term.T,np.append(ones_array,self.outputs[i],axis=1))   
            else:
                prev_term=np.dot(prev_term,self.weights[i+1][1:].T)*self.activation(self.activations[i],self.outputs[i+1],derivative=True)
                self.derivatives[i]=np.dot(prev_term.T,np.append(ones_array,self.outputs[i],axis=1))
            if momentum:
                self.delta_weights[i]=beta*self.delta_weights[i]-lr*((self.derivatives[i].T)/len(y))
                self.delta_bias[i]=beta*self.delta_bias[i]-lr*((self.derivatives[i].T)/len(y))
                self.weights[i]=self.weights[i]+self.delta_weights[i]
                self.bias[i]=self.bias[i]+self.delta_bias[i]
            else:
                self.weights[i]=self.weights[i]-lr*((self.derivatives[i].T)/len(y))
                self.bias[i]=self.bias[i]-lr*((self.derivatives[i].T)/len(y))
    
    def train(self,batches,lr=1e-3,epoch=10,beta):
        """number of batches to split data in,Learning rate and epochs"""
        for epochs in range(epoch):
            samples=len(self.x)
            c=0
            for i in range(batches):
              x_batch=self.x[int((samples/batches)*i):int((samples/batches)*(i+1))]
              y_batch=self.y.loc[int((samples/batches)*i):int((samples/batches)*(i+1))-1]
              
              c=self.forward_pass(x_batch,y_batch,self.weights,self.bias)
              self.backward_pass(y_batch,lr,momentum=True,beta)
            print(epochs,c/batches)
    
    def predict(self,x):
        """input: x_test values"""
        x=x/255
        for i in range(len(self.weights)):
            samples=len(x)
            ones_array=np.ones(samples).reshape(samples,1)
            z=np.dot(np.append(ones_array,x,axis=1),self.weights[i]+self.bias[i])
            if i==len(self.weights)-1:
                x=self.softmax(z)
            else:
                x=self.activation(self.activations[i],z)
        return np.argmax(x,axis=1)


# In[21]:


n=NeuralNetworkMomentum(X_train,Labels)
l1=Layer(100,'sigmoid')
l2=Layer(50, 'tanh')
n.connect(X_train,l1)
n.connect(l1,l2)
n.connect(l2,Labels)
n.train(batches=500,lr=0.1,epoch=20,beta=0.5)


# In[22]:


pred=n.predict(X_test)
np.bincount(n.predict(X_test)),np.bincount(y_test)


# In[23]:


print(f"accuracy is {np.bincount(np.abs(y_test-pred))[0]*100/len(y_test)} %")


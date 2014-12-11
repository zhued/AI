#!/usr/bin/env python 

# from assignment5 import * 
from numpy import *
from math import log
import sys, time


# If PRODUCTION is false, don't do smoothing 

PRODUCTION = True

# Pretty printing for 1D/2D numpy arrays
MAX_PRINTING_SIZE = 30

def print_timing(func):
    def wrapper(*arg):
        t1 = time.time()
        res = func(*arg)
        t2 = time.time()
        print '%s took %0.3f ms' % (func.func_name, (t2-t1)*1000.0)
        return res
    return wrapper

def array_to_string(a):
    return [str(x) for x in a]

def custom_flatten(xs):
    """flatten a list that looks like [a,[b,[c,[d,[e]]]]]
    needed because the list can be hundreds of thousands of elements long,
    and the recursion in regular flatten can't handle it."""
    result = []
    while len(xs) != 1:
        result.append(xs[0])
        xs = xs[1]
    if len(xs) == 1:
        result.append(xs[0])
    return result

def flatten(x):
    """flatten(sequence) -> list

    Returns a single, flat list which contains all elements retrieved
    from the sequence and all recursively contained sub-sequences
    (iterables).

    Examples:
    >>> [1, 2, [3,4], (5,6)]
    [1, 2, [3, 4], (5, 6)]
    >>> flatten([[[1,2,3], (42,None)], [4,5], [6], 7, MyVector(8,9,10)])
    [1, 2, 3, 42, None, 4, 5, 6, 7, 8, 9, 10]"""

    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result




def format_array(arr):
    s = shape(arr)
    if s[0] > MAX_PRINTING_SIZE or (len(s) == 2 and s[1] > MAX_PRINTING_SIZE):
        return "[  too many values (%s)   ]" % s

    if len(s) == 1:
        return  "[  " + (
            " ".join(["%.6f" % float(arr[i]) for i in range(s[0])])) + "  ]"
    else:
        lines = []
        for i in range(s[0]):
            lines.append("[  " + "  ".join(["%.6f" % float(arr[i,j]) for j in range(s[1])]) + "  ]")
        return "\n".join(lines)

def format_array_print(arr):
    print format_array(arr)


def string_of_model(model, label):
    (initial, tran_model, obs_model) = model
    return """
Model: %s 
initial: 
%s

transition: 
%s

observation: 
%s
""" % (label, 
       format_array(initial),
       format_array(tran_model),
       format_array(obs_model))

    
def check_model(model):
    """Check that things add to one as they should"""
    (initial, tran_model, obs_model) = model
    for state in range(len(initial)):
        assert((abs(sum(tran_model[state,:]) - 1)) <= 0.01)
        assert((abs(sum(obs_model[state,:]) - 1)) <= 0.01)
        assert((abs(sum(initial) - 1)) <= 0.01)


def print_model(model, label):
    check_model(model)
    print string_of_model(model, label)    

class HMM:
    """ HMM Class that defines the parameters for HMM """
    def __init__(self, states, outputs):
        """If the hmm is going to be trained from data with labeled states,
        states should be a list of the state names.  If the HMM is
        going to trained using EM, states can just be range(num_states)."""
        self.states = states
        self.outputs = outputs
        n_s = len(states)
        n_o = len(outputs)
        self.num_states = n_s
        self.num_outputs = n_o
        self.initial = zeros(n_s)
        self.transition = zeros([n_s,n_s])
        self.observation = zeros([n_s, n_o])

    def set_hidden_model(self, init, trans, observ):
        """ Debugging function: set the model parameters explicitly """
        self.num_states = len(init)
        self.num_outputs = len(observ[0])
        self.initial = array(init)
        self.transition = array(trans)
        self.observation = array(observ)
        self.compute_logs()
        
    def get_model(self):
        return (self.initial, self.transition, self.observation)

    def compute_logs(self):
        """Compute and store the logs of the model"""
        f = lambda xs: map(log, xs)
        self.log_initial = f(self.initial)
        self.log_transition = map(f, self.transition)
        self.log_observation = map(f, self.observation)
        

    def __repr__(self):
        return """states = %s
observations = %s
%s
""" % (" ".join(array_to_string(self.states)), 
       " ".join(array_to_string(self.outputs)), 
       string_of_model((self.initial, self.transition, self.observation), ""))

     
    # declare the @ decorator just before the function, invokes print_timing()
    @print_timing
    def learn_from_labeled_data(self, state_seqs, obs_seqs):
        """
        Learn the parameters given state and observations sequences. 
        Tje ordering of states in states[i][j] must correspond with observations[i][j].
        Uses Laplacian smoothing to avoid zero probabilities.
        """

        # Fill this in...
#       self.initial = normalize(...)
#       self.transition = ...
#       self.observation = ...
#       self.compute_logs()
        
        prefix = zeros(self.num_states)
        for state in state_seqs:
            self.initial[state[0]] += 1
            for i in range(len(state) - 1):
                self.transition[state[i]][state[i+1]] += 1
                prefix[state[i]] += 1
            #prefix[state[-1]] += 1

        for i in range(self.num_states):
            self.initial[i] = (self.initial[i] + 1.0) / (len(state_seqs) + self.num_states)
            for j in range(self.num_states):
                self.transition[i][j] = (self.transition[i][j] + 1.0) / (prefix[i] + self.num_states)

        prefix = zeros(self.num_states)
        for i in range(len(state_seqs)):
            for j in range(len(state_seqs[i])) :
                self.observation[state_seqs[i][j]][obs_seqs[i][j]] += 1
                prefix[state_seqs[i][j]] += 1

        for i in range(self.num_states):
            for j in range(self.num_outputs):
                self.observation[i][j] = (self.observation[i][j] + 1.0) / (prefix[i] + self.num_outputs)

        self.compute_logs()
                     
    # declare the @ decorator just before the function, invokes print_timing()
    @print_timing
    def learn_from_observations(self, instances, debug=False, flag=False):
        """
        Learn hmm parameters based on the specified instances.
        This would find the maximum likelyhood transition model,
        observation model, and initial probabilities.
        """
        #def baumwelch(obs,N,M, num_iters=0, debug=False,init_model=None, flag=False):   
        loglikelihoods = None
        if not flag:
            (self.transition, 
             self.observation,
             self.initial) = baumwelch(instances,
                                       len(self.states), 
                                       len(self.outputs), 
                                       0,
                                       debug)
        else:
            (self.transition, 
             self.observation,
             self.initial,
             loglikelihoods) = baumwelch(instances,
                                       len(self.states), 
                                       len(self.outputs), 
                                       0,
                                       debug, None, flag)
            
        
        self.compute_logs()

        if flag:
            return loglikelihoods    

    # Return the log probability that this hmm assigns to a particular output
    # sequence
    # def log_prob_of_sequence(self, sequence):
    #     model = (self.initial, self.transition, self.observation) 
    #     alpha, loglikelyhood = get_alpha(sequence, model)

    #     return loglikelyhood

    def most_likely_states(self, sequence, debug=False):
        """Return the most like sequence of states given an output sequence.
        Uses Viterbi algorithm to compute this.
        """
        # Code modified from wikipedia
        # Change this to use logs
       
        cnt = 0
        states = range(0, self.num_states)
        T = {}
        for state in states:
            ##          V.path   V. prob.
            output = sequence[0]
            p = self.log_initial[state] + self.log_observation[state][output]
            T[state] = ([state], p)
        for output in sequence[1:]:
            cnt += 1
            if debug:
                if cnt % 500 == 0:
                    print "processing sequence element %d" % cnt
                    sys.stdout.flush()
            U = {}
            for next_state in states:
                argmax = None
                valmax = None
                for source_state in states:
                    (v_path, v_prob) = T[source_state]
                    p = (self.log_transition[source_state][next_state] +
                         self.log_observation[next_state][output])
                    v_prob += p

                    if valmax is None or v_prob > valmax:
                        argmax = v_path
                        valmax = v_prob
                # Using a nested (reversed) list for performance
                # reasons: the wikipedia code does a list copy, which
                # causes problems with long lists.  The reverse is
                # needed to make the flatten easy.  (This is
                # essentially using a lisp-like Cons cell representation)
                argmax = [next_state, argmax]
                U[next_state] = (argmax, valmax)
            T = U
        ## apply sum/max to the final states:
        argmax = None
        valmax = None
        for state in states:
            (v_path, v_prob) = T[state]
#            print "%s  %s" % T[state]
            if valmax is None or v_prob > valmax:
                argmax = v_path
                valmax = v_prob

        # Kept the list as in reverse order, and nested to make things fast.
        ans = custom_flatten(argmax)
        ans.reverse()
        return ans
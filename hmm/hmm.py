import random
import math
in_name = 'english1000.txt'
out_name = 'markov-large.txt'

#This is the data structure for the different states,
#storing 
class State:
    def __init__(self):
        self.transitions = []
        self.emissions = []
        self.alpha = 1

#This creates a random distribution of a given length
def initialize(n):
    l = []
    for i in range(n):
        l.append(random.randrange(1,1000))
    tot = float(sum(l))
    return [x/tot for x in l]

#This implements the formula for total probability
def total_probability(times,beta_times,states):
    sum = 0
    for i in range(len(times)):
        for j in range(len(states)):
            sum += beta_times[i][j]*times[i][j]
    return sum

def main():
  #set this to True for more output
  verbose = False
  inf = open(in_name, 'r')
  outf = open(out_name, 'w')
  words = []
  letters = []
  #Read in the file line by line, adding the # character
  for line in inf.readlines():
      words.append(line.strip() + '#\n')
  z = len(words)

    #Construct the list of letters which appear
  for w in words:
        for c in w.strip():
            letters.extend(c)
  letters = list(set(letters))
  outf.write('---------------------------------\n- Initialization -\n---------------------------------\n')

  states = [State() for _ in range(2)]
  #Initialize the random transition and emission probabilities
  for index,state in enumerate(states):
        outf.write('\nCreating State %d\n' % index)
        outf.write('Transitions\n')
        states[index].transitions = initialize(len(states))
        for inner,transition in enumerate(states[index].transitions):
            outf.write('    To state   %d  %f\n' % (inner, transition))
        states[index].emissions = zip(initialize(len(letters)), letters)
        
        outf.write('\nEmission Probabilities\n')
        for (probability, letter) in sorted(states[index].emissions, reverse=True):
            outf.write('    Letter    %c   %f\n' % (letter, probability))
        outf.write('    Total: %f\n\n' % sum(prob for (prob,letter) in states[index].emissions))
  #These can be uncommented in order to use the data used for the sample output
  #in the assignment write up
  pis = initialize(len(states))#[.3196,.6804]
  #states[0].transitions = [.5,.5]
  #states[0].emissions = [(0.3181,'b'),(.2141,'a'),(.2035,'#'),(.0156,'i'),(.2486, 'd')]
  #states[1].transitions = [.5, .5]
  #states[1].emissions = [(.0504,'b'),(.1197,'a'),(.2868,'#'),(.2610,'i'), (.2821, 'd')]
  outf.write('\n---------------------------\nPi:\n')
  for i in range(len(pis)):
        outf.write('    State   %d       %f\n' % (i,pis[i]))
  soft_counts = {}
  transition_counts = []
  initial_soft_counts = []
  for i in range(len(states)):
        initial_soft_counts.append(0)

    #Set up the structures for the soft counts and transition counts
    #to be used in parts 4 and 5
  for i in range(len(states)):
        transition_counts.append([])
        for j in range(len(states)):
            transition_counts[i].append(0.0)
  previous_probability = -100
  #We run the algorithm at most a certain number of iterations
  #and also stop if the probability has stopped increasing by
  #more than 0.01%
  for iterations in range(300):
    if iterations > 5 and math.fabs((probability - previous_probability) / probability) < 0.0001:
      print probability, previous_probability, math.fabs((probability - previous_probability) / probability)
      break
    previous_probability = probability
    soft_counts = {}
    initial_soft_counts = []
    transition_counts = []
    for i in range(len(states)):
        transition_counts.append([])
        for j in range(len(states)):
            transition_counts[i].append(0.0)
    for i in range(len(states)):
          initial_soft_counts.append(0)
    for letter in letters:
          soft_counts[letter] = []
          for i in range(len(states)):
                  soft_counts[letter].append(0.0)
    probability = 0
    for w in words:
          times = []
          w = w.strip()
          t = 1
          times.append([])
          times[t-1] = pis
      if verbose:
            outf.write('\n*** word: %s***\n' % w)
            outf.write('\nForward\n')
          #Print out the initial pi values
          for index,s in enumerate(states):
          if verbose:
                outf.write('Pi of state %d %f\n' % (index,pis[index]))
              states[index].alpha = pis[index]
          #Time will start at 2
          t += 1
          #Iterate through each character in the word
          for c in w:
              times.append([])
              #Go step by step, incrementing the alpha value by referencing
              #the transition and emission probabilities
              if verbose:
                  outf.write('time %d: \'%c\'\n' % (t, c))
              for i,to_state in enumerate(states):
                  current_alpha = 0
                  if verbose:
                      outf.write('to state: %d\n' % i)
                  temp = 0
                  for j, from_state in enumerate(states):
                      temp += from_state.alpha*from_state.transitions[i]*[x for (x,y) in from_state.emissions if y == c][0]
                      if verbose:
                          outf.write('  from state   %d   Alpha: %g\n' % (j, temp))
                  times[t-1].append(temp)
                  current_alpha = sum(times[t-1])
              
              for i,state in enumerate(states):
                  states[i].alpha = times[t-1][i]
              t += 1
      if verbose:
        outf.write('Sum of alpha\'s: %g\n' % current_alpha)
          #Now we write out the total alphas for the word
            outf.write('Alpha:\n')
            for index,time in enumerate(times):
              outf.write('    Time  %d ' % (index+1))
              for j,state in enumerate(states):
                  outf.write('State  %d:  %g  ' % (j, time[j]))
              outf.write('\n')
          #Now we start the backwards probability
          beta_times = []
          for i in range(len(times)):
              beta_times.append([1,1])
  
          for i in reversed(range(len(beta_times)-1)):
              for j,state in enumerate(states):
                  temp = 0
                  for k,to_state in enumerate(states):
                      temp += beta_times[i+1][k]*state.transitions[k]*[x for (x,y) in state.emissions if y == w[i]][0]
                  beta_times[i][j] = temp
          if verbose:
            outf.write('Beta:\n')
            for index,time in enumerate(beta_times):
              outf.write('    Time  %d ' % (index+1))
              for j,state in enumerate(states):
                  outf.write('State  %d:  %g  ' % (j, time[j]))
              outf.write('\n')
          #Print out the accumulated probability value
          probability += total_probability(times,beta_times,states)
      if verbose:
            outf.write("\n---------------------------\nSoft counts\n-------------------------\n")
          #Now we start the soft counts, iterating through the dictionary we've constructed
          #using each letter in the corpus
          for i,c in enumerate(w):
          if verbose:
                outf.write("    Letter: %c\n" % c)
              for j, from_state in enumerate(states):
              if verbose:
                    outf.write("        From state: %d\n" % j)
                  for k, to_state in enumerate(states):
                      temp =  times[i][j]*from_state.transitions[k]*[x for (x,y) in from_state.emissions if y == c][0]*beta_times[i+1][k]/current_alpha
                      soft_counts[c][j] += temp
              if i == 0:
                initial_soft_counts[j] += temp
                      transition_counts[j][k] += temp
              if verbose:
                        outf.write("            To state:   %d  %g;\n" % (k, temp))
      #Now we start calculating the Viterbi path for each word
          outf.write('----------------------------\nViterbi path\n----------------------------\n%s\n\n' % w)
          total_path = [()]
          viterbis = [[]]
      #Initial values will be set based on pi values
          for i,pi in enumerate(pis):
            outf.write('Delta[1] of stateno %d  %g\n' % (i, pi))
        viterbis[0].append((pi, i))
      #Then we iterate through each letter of the word
          for i,letter in enumerate(w):
        total_path.append(())
            outf.write('Time t+1    %d  %c\n' % (i+2,letter))
        viterbis.append([])
            for j, state in enumerate(states):
              outf.write('at state %d:\n' % j)
          from_probability = []
          for k, from_state in enumerate(states):
        #Here the main formula is run   
            from_probability.append((viterbis[i][k][0]*from_state.transitions[j]*[x for (x,y) in from_state.emissions if y == letter][0], k))
            outf.write('    from-state %d: %g\n' % tuple(reversed(from_probability[k])))
          outf.write('best state to come from is %d (at %g)\n' % tuple(reversed(max(from_probability))))
          #Here viterbis is storing both the Induction and backtrace values as a tuple
          viterbis[i+1].append(max(from_probability))
      #We set the last Viterbi value first
      total_path[len(w)] = max(viterbis[len(viterbis)-1])[1]
      #Then we move backwards through the rest
      for i in reversed(range(len(w))):
        total_path[i] = viterbis[i+1][total_path[i+1]][1]
      #And finally we print out the best path
      outf.write('Viterbi path:\n')
      outf.write('time:    ')
      for i in range(len(total_path)):
        outf.write('%d  ' % i)
      outf.write('\nstate:   ') 
          for i in total_path:
        outf.write('%d  ' % i)
      outf.write('\n')
        
        


    outf.write("\n\nEmission\n")
    #Now we normalize and print out our constructed soft counts
    for i in range(len(states)):
        outf.write("\n  From State:  %d\n" % i)
        running_total = 0.0
        for letter in letters:
            running_total += soft_counts[letter][i]
        for letter in letters:
      index = [ind for ind,value in enumerate(states[i].emissions) if value[1] == letter][0]
      states[i].emissions[index] = (soft_counts[letter][i]/running_total, letter)
    for V in sorted(states[i].emissions, reverse=True):
      outf.write("      letter: %c probability: %g\n" % tuple(reversed(V)))
    outf.write("\nTotal Probability: %g %g\n" % (probability,previous_probability))
    outf.write("\n")
    #Ditto for the transition counts
    outf.write("Transition Probabilities\n")
    for i in range(len(states)):
        outf.write("\n    From_State: %d\n" % i)
        from_total = sum(transition_counts[i])
        for j in range(len(states)):
            normalized = transition_counts[i][j] / from_total
            outf.write("        To state:   %d prob: %g (%g over %g)\n" % (j, normalized, transition_counts[i][j], from_total))
        states[i].transitions[j] = normalized
    letter_logs = []
    for letter in letters:
      emission_0 = [x for (x,y) in states[0].emissions if y == letter][0]
      emission_1 = [x for (x,y) in states[1].emissions if y == letter][0]
      #We append the log values, being careful to avoid a divide by zero
      #error which sometimes occurs after a large number of iterations
      try:
       letter_logs.append((math.log(max(emission_0, 0.0000001) / max(emission_1,0.0000001)), letter))
      except ValueError:
       print emission_0, emission_1
    #Now we write out the letters based on their log values   
    outf.write('Letters:\n  State 0:\n')
    for (log,letter) in sorted(letter_logs, reverse=True): 
      if log < 0:
        break
      outf.write('      %c %g\n' % (letter,log))
    outf.write('\n  State 1:\n')
    for log,letter in sorted(letter_logs):
      if log > 0:
        break
      outf.write('      %c %g\n' % (letter,-log))

    pis = [i/z for i in initial_soft_counts]
    outf.write("---------------------------\nPi:\n")
    for index,pi in enumerate(pis):
        outf.write('State   %d  %g\n' % (index,pi))

      

  inf.close()
  outf.close()


if __name__ == "__main__":
    main()

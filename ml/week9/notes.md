week9_solution.py takes a shortcut in the implementation of best subset and forward stepwise selction:

- there is no zero model because it was clear that the given predictors would be better then the mean. but that's a little bit lazy.
- step 3. is omitted as well. because the adjusted r^2 is used and not C_p, BIC or CV. highest r^2 for a constant amount of features will also have the highest adjusted r^2. therefore, storing adjusted r^2 and some sorting does the job.
- forward stepwise selction is mostly copy paste. itertools.combination is not necessary

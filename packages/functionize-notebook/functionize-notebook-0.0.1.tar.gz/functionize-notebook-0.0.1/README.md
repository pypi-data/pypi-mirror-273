functionize-notebook
========

`functionize-notebook` allows you to wrap `jupyter-notebook` and use it like a function. It 
allows passing input and output. It is **not** multi-thread safe.

## Installation
```
$ pip install -U functionize-notebook
```

## Start
The main function used in pandasql is `NotebookWrapper`. `NotebookWrapper` expect 3 parameters
   - a path to the notebook.
   - a list of input params' names (these params will be used in the notebook).
   - a list of output params' names (these params must exist in the notebook).
   - (optional) which tag indicating input. Default "input". 


## Notebook

If you want to use input, you must create a cell dedicated to input. In which, only assignment happens. Any calculation in this cell may lead to unexpected results. This cell also need to have tag `input` or the value you put in `inputTag`


## Run the notebook

Example: you want to pass `a`, `b` as input and want `sum` back. 

```Python 
calculateSum = NotebookWrapper("./sum.ipynb", ["a", "b"], "sum")
```

You can now run this by method `run`
```Python
sum = calculateSum.run(5, 10)
```
or just call it like a function 
``` Python
sum = calculateSum(5, 10)
```

You can also pass input as named params (you don't have to specify these params beforehand while create the object). These params will overide the previous. 

```Python
sum = calculateSum(5, 10, a = 8, c = 9)
```
This will overide value of a. Now a = 8. Variable c = 9 is also injected to notebook.

You can also pass other datatype. However, Any modifications made by notebook won't be reflected on the object. You can still return the object to get the modifications.

More information and code samples available in the [examples folder](./examples/).



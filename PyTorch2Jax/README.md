# PyTorch to Jax Conversion

This example illustrates how Benchify can be used to test the equivalence of two austensibly equivalent functions.  In this case, the customer translated some code from PyTorch to Jax, and wanted to make sure that the two implementations were functionally equivalent.  Thank you to [Nithin Santi](https://www.linkedin.com/in/nithinsonti/) for contributing this example!

Read the report [here](https://github.com/maxvonhippel/benchify-examples/pull/20).  We're working on formatting improvements, and will share updates on this thread as they ship.

Note, to run this example you do need to add `jax` and `torch` back to the requirements.txt.  We removed them because they take a long time to install and slow down other tests which we run more frequently.
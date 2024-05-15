import numpy as np


def gradient_descent(fun, x0, args=(), options=None, callback=None, f_old=np.inf):
    """
    Mininize a function using the gradient descent method

    - input:
        * fun: callable, method that given an x return the evaluation in x of the function to minimize and its gradient
        * x0: the initial point from which the iterative optimization algorithm will starts
        * args: tuple, arguments that should be given to the callable fun besides x
        * options:
            dictionnary, by default None,
            contains several options that can be given to customize the gradient descent method and its stopping criteria
            these options are:
            the step size, or learning rate, of the gradient descent 'step size', constant for now, by default step_size=1
            the maximal number of iteration 'nit_max', by default nit_max=50,
            the tolerance on two consecutive evaluation of the function to minimize 'ftol', by default ftol=1e-7,
            the tolerance on the gradient 'gtol, by default gtol=1e-7.
        * callback: A AJOUTER
        * f_old:
            float, by default np.inf,
            if the optimization processe is restarted, enable to store the previous value of the cost function
    - output:
        * the optimal value of x
        * the evaluation of the function to minimize at the optimal value of x
        * the evaluation of the gradient of the function to minimize at the optimal value of x
        * the number of iteration needed to converge
    - TO DO:
        * ameliorer le critere d arret
        * ameliorer la doc
        * ajouter exception pour vérifier que les types en entrees sont les bons
    """

    if not isinstance(args, tuple):
        args = (args,)

    # if callable(jac):
    #    pass
    # elif jac is True:
    #    # fun returns func and grad
    #    jac = lambda x, *args : fun(x, *args)[1]
    #    fct = lambda x, *args : fun(x, *args)[0]

    if options is None:
        options = {}

    # if 'ftol' in options.keys():
    #     ftol = options['ftol']
    # else:
    #     ftol = 1e-7

    # if 'gtol' in options.keys():
    #     gtol = options['gtol']
    # else:
    #     gtol = 1e-7

    if 'nit_max' in options.keys():
        nit_max = options['nit_max']
    else:
        nit_max = 50

    if 'step size' in options.keys():
        step_size = options['step size']
    else:
        step_size = 1

    if callback is None:

        def callback(x):
            pass

    # initilization of the iteration number, of x, the stopping criteria and the previous evaluation of the function
    nit = 0
    x = x0
    flag_stop = True

    # loop until the stopping criteria is reached
    while flag_stop:
        # evaluation of the function to minimize and its gradient
        f, df = fun(x, *args)

        if f > f_old:
            raise ValueError(
                "The cost function at the current iteration is larger than the cost function at the previous iteration."
                + " This is likely to be du to a too large step."
            )

        # updating x following the descent gradient method
        x -= df * step_size

        # call the callback function and update the iteration number
        callback(x)
        nit += 1

        # update the flag of the stopping criteria and the previous evaluation of the function
        flag_ite = nit < nit_max
        # flag_ftol = np.abs(f - f_old) < ftol
        # flag_gtol = np.max(np.abs(df)) < gtol
        flag_stop = flag_ite  # and flag_ftol and flag_gtol
        f_old = np.copy(f)

    return x, f, df, nit

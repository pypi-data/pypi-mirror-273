import numpy as np


def proximal_gradient(x0, fun1, proximal_fun2, args=(), options=None, callback=None):
    """
    Uses accelerated proximal gradient (FISTA) to solve :
    argmin f(x) + g(x)
    with f a differentiable function and g a fonction whose proximal operator is known
    in the present context :
    f is the L2 norm terms of the cost function (cost of the observations and Tikhonov regularization terms)
    g is the L1 norm / LASSO regularization term

    - input:
        * x0: the initial point from which the iterative optimization algorithm will starts
        * fun1: callable, method that given an x return the evaluation of the differentiable function f and its gradient
        * proximal_fun2: callable, method that given an x return the evaluation of proximal operator of the function g
        * algorithm: string, by default 'ISTA', the type of algorithm used, ISTA and FISTA are implemented
        * args: tuple, arguments that should be given to the callable fun1 besides x
        * options:
            dictionnary, by default None,
            contains several options that can be given to customize the gradient descent method and its stopping criteria
            these options are:
            the step size of the gradient descent by default step_size=1, for FISTA, should be 1/L with L the Lipschitz constant
            the maximal number of iteration 'nit_max', by default nit_max=50,
            the tolerance on two consecutive evaluation of the function to minimize 'ftol', by default ftol=1e-7,
            the tolerance on the gradient 'gtol, by default gtol=1e-7.
        * callback: A AJOUTER
    - output:
        * the optimal value of x
        * the evaluation of the function f at the optimal value of x
        * the evaluation of the gradient of the function f at the optimal value of x
        * the number of iteration needed to converge
    """

    # ADD EXCEPTIONS

    if not isinstance(args, tuple):
        args = (args,)

    if options is None:
        options = {}

    if 'nit_max' in options.keys():
        nit_max = options['nit_max']
    else:
        nit_max = 50

    if 'algorithm' in options.keys():
        algorithm = options['algorithm']
    else:
        algorithm = 'ISTA'

    if 'step size' in options.keys():
        step_size = options['step size']
    else:
        step_size = 1

    if callback is None:

        def callback(x):
            pass

    # initilization of the iteration number, of x, the stopping criteria and the previous evaluation of the function
    x = np.copy(x0)
    nit = 0
    flag_convergence = False

    # if the used algorithm is the FISTA algorithm
    # the step size should be 1/L with L the Lipschitz constant in the case of the FISTA algorithm !
    if algorithm == 'FISTA':
        # initialization of the inertial coefficient
        t = 1
        x_old = np.copy(x)

        # loop until the stopping criteria is reached
        while not (flag_convergence):
            # store the inertial coefficient at the previous iteration
            # and computation of the inertial coefficient at the current iteration (see Beck and Teboule, 2009)
            told = np.copy(t)
            t = 0.5 * (1 + np.sqrt(1 + 4 * told**2))
            alpha = (told - 1) / t

            # adding the inertial terme to x
            z = x + alpha * (x - x_old)
            x_old = np.copy(x)

            # computation of the differentiable function f and its gradient
            f, df = fun1(z, *args)
            # computation of the proximal part of the algorithm and update of x
            x = proximal_fun2(z - step_size * df, step_size)

            # call the callback function and update the iteration number
            callback(x)
            nit += 1

            # update the flag of the stopping criteria and the previous evaluation of the function
            flag_ite = nit >= nit_max
            flag_convergence = flag_ite

    # if the used algorithm is the ISTA algorithm
    elif algorithm == 'ISTA':
        # loop until the stopping criteria is reached
        f_old = np.inf
        while not (flag_convergence):
            # computation of the differentiable function f and its gradient
            f, df = fun1(x, *args)
            if f > f_old:
                raise ValueError(
                    "The cost function at the current iteration is larger than the cost function at the previous iteration."
                    + " This is likely to be du to a too large step."
                )

            # computation of the proximal part of the algorithm and update of x
            x = proximal_fun2(x - step_size * df, step_size)

            # call the callback function and update the iteration number
            callback(x)
            nit += 1

            # update the flag of the stopping criteria and the previous evaluation of the function
            flag_ite = nit >= nit_max
            flag_convergence = flag_ite
            f_old = np.copy(f)

    else:
        raise ValueError("The given type of algorithm has not been implemented. It should be ISTA or FISTA ")

    return x, f, df, nit

import numpy as np

def get_ranks_inplace(_list):
    '''
    Takes a list/array of values and returns the corresponding rank of each
    element in its 'place'.

    Example:
    A = np.array((2, 5, 1, 8, 9))
    get_ranks(A)
    >> [3, 2, 4, 1, 0]

    Parameters
    ----------
    _list : list or np.array
     - List/array of elements to arrange

    Returns
    -------
    ranks : list
     - List containing ranks of element in given list/array
    '''
    res_tmp = -_list

    # List sorted from true highest to lowest
    res_tmpSorted = np.sort(res_tmp)

    list_ranks_inplace = []

    for e in res_tmp:
        list_ranks_inplace.append(np.where(res_tmpSorted==e)[0][0])

    return list_ranks_inplace

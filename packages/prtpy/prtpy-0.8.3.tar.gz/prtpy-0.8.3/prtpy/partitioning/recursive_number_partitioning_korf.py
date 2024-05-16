
"""
This class is based on "Multi-Way Number Partitioning" by: Richard E. Korf , 2009 
The main purpose of this article is to solve the known Number Partitioning problem, in focus 
on multy way Partitioning (more than 2 bins). 
In this article he develops two new linear-space algorithms for multi-way partitioning, and demonstrate their
performance on three, four, and five-way partitioning.

In this class we gone a focus on the second algorithm called RNP (Recursive Number Partitioning). 
RNP Description (in few words - to the complete explanation see the link below):
In general, for an even number of subsets, RNP starts with two-way partitioning at the top level (using CKK),
and then recursively partitions each half.
With an odd number of subsets, RNP searches an inclusion-exclusion tree for a first subset, then calls RNP to divide the
remaining numbers two ways, etc.

Link to the article : https://www.ijcai.org/Proceedings/09/Papers/096.pdf

Authors: Jonathan Escojido & Samuel Harroch
Date:    03-2022
"""

from typing import Callable, List
from prtpy import outputtypes as out, objectives as obj, Binner, BinnerKeepingContents, BinsArray, printbins
from prtpy.partitioning.karmarkar_karp import kk
import numpy as np, logging
from prtpy import partition
from prtpy.partitioning.complete_karmarkar_karp import optimal as ckk_optimal, generator as ckk_generator
from prtpy.inclusion_exclusion_tree import InExclusionBinTree

logger = logging.getLogger(__name__)

def find_diff(l1: List, l2: List):
    from collections import Counter
    c1 = Counter(l1)
    c2 = Counter(l2)
    diff = c1 - c2
    return list(diff.elements())


# works only for 3, 4, 5 ways partitioning (as present in the paper)
def rnp(binner: Binner, numbins: int, items: List[any]) -> BinsArray:
    """
    In general, for an even number of subsets, RNP starts with two-way partitioning at the top level (using CKK),
    and then recursively partitions each half.
    With an odd number of subsets, RNP searches an inclusion-exclusion tree for a first subset, then calls RNP to divide the
    remaining numbers two ways, etc.

    bins - a Bins structure. It is initialized with no bins at all. It contains a function for adding new empty bins.
    items - a list of item-names.
    valueof - a function that accepts an item and returns its value.

    return: a Bins structure with the partition (according to the algorithm output)

    >>> from prtpy import BinnerKeepingContents, BinnerKeepingSums
    >>> rnp(BinnerKeepingContents(), 3, items=[4, 5, 7, 8, 6])[1]
    [[8], [4, 7], [5, 6]]
    >>> list(rnp(BinnerKeepingContents(), 3, items=[4, 5, 7, 8, 6])[0])
    [8.0, 11.0, 11.0]
    >>> rnp(BinnerKeepingContents(), 4, items=[4, 5, 7, 8, 6])[1]
    [[6], [7], [8], [4, 5]]
    >>> list(rnp(BinnerKeepingContents(), 4, items=[4, 5, 7, 8, 6])[0])
    [6.0, 7.0, 8.0, 9.0]
    >>> rnp(BinnerKeepingContents(), 4, items=[1,3,3,4,4,5,5,5])[1]
    [[1, 5], [3, 5], [3, 5], [4, 4]]
    >>> list(rnp(BinnerKeepingContents(), 3, items=[1,3,3,4,4,5,5,5])[0])
    [10.0, 10.0, 10.0]
    >>> rnp(BinnerKeepingContents(), 5, items=[1,2,3,4,5,6,7,8,9])[1]
    [[2, 7], [4, 5], [9], [3, 6], [1, 8]]
    >>> list(rnp(BinnerKeepingContents(), 5, items=[1,2,3,4,5,6,7,8,9])[0])
    [9.0, 9.0, 9.0, 9.0, 9.0]

    >>> sorted(rnp(BinnerKeepingContents(), 5, items=[3, 16, 22, 24, 24, 29])[0])
    [19.0, 22.0, 24.0, 24.0, 29.0]

    >>> from prtpy import partition
    >>> partition(algorithm=rnp, numbins=4, items={"a":1, "b":1, "c":1, "d":1})
    [['c'], ['d'], ['b'], ['a']]
    >>> partition(algorithm=rnp, numbins=4, items={"a":1, "b":1, "c":1, "d":1}, outputtype=out.Sums)
    [1.0, 1.0, 1.0, 1.0]
    """
    best_partition_so_far = kk(binner=binner, numbins=numbins, items=items)
    sums = binner.sums(best_partition_so_far)
    best_difference_so_far = max(sums) - min(sums)
    if best_difference_so_far == 0:  
        return best_partition_so_far     # 0 is the best possible value

    prior_bins = binner.new_bins(0)
    best_partition_so_far = rec_generate_sets(prior_bins, best_partition_so_far, items, numbins, numbins, trees=[], binner=binner)
    return best_partition_so_far


def rec_generate_sets(prior_bins: BinsArray, best_partition_so_far: BinsArray, items: List, total_numbins:int, current_numbins:int, trees: List, binner: Binner):
    """
    A recursive subroutine of RNP.
    """
    logger.info("Recursive call: best_partition_so_far=%s, prior_bins=%s, items=%s, total_numbins=%d, current_numbins=%d", best_partition_so_far, prior_bins, items, total_numbins, current_numbins)
    num_prior_bins = total_numbins - current_numbins
    bins_sums = binner.sums(best_partition_so_far)
    best_difference_so_far = max(bins_sums) - min(bins_sums)

    #### Base case: numbins == 2
    if current_numbins == 2:
        return ckk_optimal(binner=binner, numbins=2, items=items)

    #### Odd case: numbins is odd
    if current_numbins % 2 == 1:  
        # take one with in_ex_tree end then split in 2
        t = sum(map(binner.valueof, items))  # t is the sum of all the remaining items
        in_ex_tree = InExclusionBinTree(
            items=items,
            valueof=binner.valueof,
            lower_bound=(t - (current_numbins - 1) * best_difference_so_far) / current_numbins, upper_bound=t / current_numbins
        )
        trees.append((in_ex_tree, t, current_numbins))

        for items_for_last_bin in in_ex_tree.generate_tree():
            prior_bins = binner.add_empty_bins(prior_bins, 1)
            for item in items_for_last_bin:
                binner.add_item_to_bin(prior_bins, item=item, bin_index=num_prior_bins)
            remaining_items = find_diff(items, items_for_last_bin)
            new_bins = rec_generate_sets(prior_bins, best_partition_so_far, remaining_items, total_numbins, current_numbins - 1, trees, binner)
            # if new_bins:
            bins_sums = binner.sums(best_partition_so_far)
            best_difference_so_far = max(bins_sums) - min(bins_sums)
            combined_sums = np.append(binner.sums(new_bins), binner.sums(prior_bins))
            diff = max(combined_sums) - min(combined_sums)
            if diff < best_difference_so_far:
                best_partition_so_far = binner.concatenate_bins(prior_bins, new_bins)
            prior_bins = binner.remove_bins(prior_bins, 1)
    
    #### Even case: numbins is odd
    else:
        ckk_binner = BinnerKeepingContents(binner.valueof)
        for top_level_part in ckk_generator(binner=ckk_binner, numbins=2, items=items, best_difference_so_far=-best_difference_so_far):
            bin1items, bin2items = top_level_part[1]
            new_bin1 = rec_generate_sets(prior_bins, best_partition_so_far, bin1items, total_numbins, current_numbins/2, trees, binner)
            new_bin2 = rec_generate_sets(prior_bins, best_partition_so_far, bin2items, total_numbins, current_numbins/2, trees, binner)

            combined_sums = np.append(binner.sums(new_bin1), binner.sums(new_bin2))
            diff = max(combined_sums) - min(combined_sums)
            if diff < best_difference_so_far:
                best_partition_so_far = binner.concatenate_bins(new_bin1, new_bin2)

    return best_partition_so_far

if __name__ == '__main__':
    import doctest
    (failures, tests) = doctest.testmod(report=True, optionflags=doctest.FAIL_FAST)
    print("{} failures, {} tests".format(failures, tests))

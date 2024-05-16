import logging
import os
from typing import Callable, List
from itertools import combinations, permutations

from mapel.core.matchings import *
from mapel.elections.objects.OrdinalElection import OrdinalElection
import mapel.core.utils as utils
from mapel.core.inner_distances import swap_distance
import mapel.elections.distances.ilp_isomorphic as ilp_iso

import mapel.elections.distances.lp as lp

try:
    import mapel.elections.distances.cppdistances as cppd
except:
    logging.warning("The quick C++ procedures for computing the swap and "
                    "Spearman distance is unavailable: using the (slow) python one instead")


# MAIN DISTANCES
def compute_pos_swap_distance(election_1: OrdinalElection, election_2: OrdinalElection,
                              inner_distance: Callable) -> (float, list):
    """ Compute Positionwise distance between ordinal elections """
    cost_table = get_matching_cost_positionwise(election_1, election_2, inner_distance)
    obj_val, matching = solve_matching_vectors(cost_table)
    cost_table = get_matching_cost_pos_swap(election_1, election_2, matching)
    return solve_matching_vectors(cost_table)


def compute_positionwise_distance(election_1: OrdinalElection, election_2: OrdinalElection,
                                  inner_distance: Callable) -> (float, list):
    """ Compute Positionwise distance between ordinal elections """
    cost_table = get_matching_cost_positionwise(election_1, election_2, inner_distance)
    return solve_matching_vectors(cost_table)


def compute_agg_voterlikeness_distance(election_1: OrdinalElection, election_2: OrdinalElection,
                                       inner_distance: Callable) -> (float, list):
    """ Compute Aggregated-Voterlikeness distance between ordinal elections """
    vector_1, num_possible_scores = election_1.votes_to_agg_voterlikeness_vector()
    vector_2, _ = election_2.votes_to_agg_voterlikeness_vector()
    return inner_distance(vector_1, vector_2, num_possible_scores)


def compute_bordawise_distance(election_1: OrdinalElection, election_2: OrdinalElection,
                               inner_distance: Callable) -> (float, list):
    """ Compute Bordawise distance between ordinal elections """
    vector_1 = election_1.votes_to_bordawise_vector()
    vector_2 = election_2.votes_to_bordawise_vector()
    return inner_distance(vector_1, vector_2), None


def compute_pairwise_distance(election_1: OrdinalElection, election_2: OrdinalElection,
                              inner_distance: Callable) -> (float, list):
    """ Compute Pairwise distance between ordinal elections """
    length = election_1.num_candidates
    matrix_1 = election_1.votes_to_pairwise_matrix()
    matrix_2 = election_2.votes_to_pairwise_matrix()
    return solve_matching_matrices(matrix_1, matrix_2, length, inner_distance), None


def compute_voterlikeness_distance(election_1: OrdinalElection, election_2: OrdinalElection,
                                   inner_distance: Callable) -> (float, list):
    """ Compute Voterlikeness distance between elections """
    length = election_1.num_voters
    matrix_1 = election_1.votes_to_voterlikeness_matrix()
    matrix_2 = election_2.votes_to_voterlikeness_matrix()
    return solve_matching_matrices(matrix_1, matrix_2, length, inner_distance), None


# DEPRECATED
def compute_swap_distance_bf(election_1: OrdinalElection,
                             election_2: OrdinalElection) -> (int, list):
    """ Compute swap distance between elections (using brute force) """
    obj_values = []
    for mapping in permutations(range(election_1.num_candidates)):
        cost_table = get_matching_cost_swap_bf(election_1, election_2, mapping)
        obj_values.append(solve_matching_vectors(cost_table)[0])
    return min(obj_values), None


def compute_swap_distance(election_1: OrdinalElection,
                          election_2: OrdinalElection) -> (int, list):
    """ Compute swap distance between elections (using the C++ extension) """
    if not utils.is_module_loaded("mapel.elections.distances.cppdistances"):
        print("Using ILP instead of C++ BF")
        return compute_swap_distance_ilp_py(election_1, election_2), None

    if election_1.num_candidates < election_2.num_candidates:
        swapd = cppd.tswapd(election_1.votes.tolist(),
                           election_2.votes.tolist())
    elif election_1.num_candidates > election_2.num_candidates:
        swapd = cppd.tswapd(election_2.votes.tolist(),
                           election_1.votes.tolist())
    else:
        swapd = cppd.swapd(election_1.votes.tolist(),
                           election_2.votes.tolist())

    return swapd, None


def compute_truncated_swap_distance(election_1: OrdinalElection,
                          election_2: OrdinalElection) -> (int, list):
    """ Compute truncated swap distance between elections """
    obj_values = []
    for mapping in permutations(range(election_1.num_candidates)):
        cost_table = get_matching_cost_truncated_swap_bf(election_1, election_2, mapping)
        obj_values.append(solve_matching_vectors(cost_table)[0])
    return min(obj_values), None


def compute_spearman_distance(election_1: OrdinalElection,
                              election_2: OrdinalElection) -> (int, list):
    """ Compute Spearman distance between elections (using the C++ extension) """
    if not utils.is_module_loaded("mapel.elections.distances.cppdistances"):
        return compute_spearman_distance_ilp_py(election_1, election_2), None
    speard = cppd.speard(election_1.votes.tolist(),
                         election_2.votes.tolist())
    return speard, None


def compute_spearman_distance_ilp_py(election_1: OrdinalElection,
                                     election_2: OrdinalElection) -> (int, list):
    """ Compute Spearman distance between elections """
    votes_1 = election_1.votes
    votes_2 = election_2.votes
    params = {'voters': election_1.num_voters,
              'candidates': election_1.num_candidates}

    file_name = f'{np.random.random()}.lp'
    path = os.path.join(os.getcwd(), "trash", file_name)
    ilp_iso.generate_ilp_spearman_distance(path, votes_1, votes_2, params)
    objective_value = ilp_iso.solve_ilp_distance(path)
    ilp_iso.remove_lp_file(path)
    objective_value = int(round(objective_value, 0))
    return objective_value, None


def compute_swap_distance_ilp_py(election_1: OrdinalElection,
                                 election_2: OrdinalElection) -> (int, list):
    """ Compute Spearman distance between elections """
    votes_1 = election_1.votes
    votes_2 = election_2.votes
    params = {'voters': election_1.num_voters,
              'candidates': election_1.num_candidates}

    file_name = f'{np.random.random()}.lp'
    path = os.path.join(os.getcwd(), 'trash', file_name)
    ilp_iso.generate_ilp_swap_distance(path, votes_1, votes_2, params)
    objective_value = ilp_iso.solve_ilp_distance_swap(path, votes_1, votes_2, params)
    ilp_iso.remove_lp_file(path)
    objective_value = int(round(objective_value, 0))
    return objective_value, None


def compute_discrete_distance(election_1: OrdinalElection,
                              election_2: OrdinalElection) -> (int, list):
    """ Compute Discrete distance between elections """
    return election_1.num_voters - compute_voter_subelection(election_1, election_2), None


# SUBELECTIONS #
def compute_voter_subelection(election_1: OrdinalElection, election_2: OrdinalElection) -> int:
    """ Compute Voter-Subelection """
    return lp.solve_lp_voter_subelection(election_1, election_2)


def compute_candidate_subelection(election_1: OrdinalElection, election_2: OrdinalElection) -> int:
    """ Compute Candidate-Subelection """
    file_name = f'{np.random.random()}.lp'
    path = os.path.join(os.getcwd(), 'trash', file_name)
    objective_value = lp.solve_lp_candidate_subelections(path, election_1, election_2)
    lp.remove_lp_file(path)
    return objective_value


# HELPER FUNCTIONS #
def get_matching_cost_pos_swap(election_1: OrdinalElection, election_2: OrdinalElection,
                               matching) -> List[list]:
    """ Return: Cost table """
    votes_1 = election_1.votes
    votes_2 = election_2.votes
    size = election_1.num_voters
    return [[swap_distance(votes_1[i], votes_2[j], matching=matching) for i in range(size)]
            for j in range(size)]


def get_matching_cost_positionwise(election_1: OrdinalElection, election_2: OrdinalElection,
                                   inner_distance: Callable) -> List[list]:
    """ Return: Cost table """

    vectors_1 = election_1.get_vectors()
    vectors_2 = election_2.get_vectors()
    size = election_1.num_candidates
    return [[inner_distance(vectors_1[i], vectors_2[j]) for i in range(size)] for j in range(size)]


def get_matching_cost_swap_bf(election_1: OrdinalElection, election_2: OrdinalElection,
                              mapping):
    """ Return: Cost table """
    cost_table = np.zeros([election_1.num_voters, election_1.num_voters])

    election_1.get_potes()
    election_2.get_potes()

    for v1 in range(election_1.num_voters):
        for v2 in range(election_2.num_voters):
            swap_distance = 0
            for i, j in combinations(election_1.potes[0], 2):
                if (election_1.potes[v1][i] > election_1.potes[v1][j] and
                    election_2.potes[v2][mapping[i]] < election_2.potes[v2][mapping[j]]) or \
                        (election_1.potes[v1][i] < election_1.potes[v1][j] and
                         election_2.potes[v2][mapping[i]] > election_2.potes[v2][mapping[j]]):
                    swap_distance += 1
            cost_table[v1][v2] = swap_distance
    return cost_table


def get_matching_cost_truncated_swap_bf(election_1: OrdinalElection,
                                        election_2: OrdinalElection,
                                        mapping):
    """ Return: Cost table """
    cost_table = np.zeros([election_1.num_voters, election_1.num_voters])

    election_1.get_potes()
    election_2.get_potes()

    for v1 in range(election_1.num_voters):
        for v2 in range(election_2.num_voters):
            swap_distance = 0
            for i, j in combinations(election_1.potes[0], 2):
                if (election_1.potes[v1][i] > election_1.potes[v1][j] and
                    election_2.potes[v2][mapping[i]] < election_2.potes[v2][mapping[j]]) or \
                        (election_1.potes[v1][i] < election_1.potes[v1][j] and
                         election_2.potes[v2][mapping[i]] > election_2.potes[v2][mapping[j]]):
                    swap_distance += 1
            cost_table[v1][v2] = swap_distance
    return cost_table


def compute_blank_distance(election_1: OrdinalElection,
                           election_2: OrdinalElection) -> (int, list):
    return 1, None

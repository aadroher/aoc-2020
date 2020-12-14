from pathlib import Path
from pprint import pprint as pp
from itertools import chain, combinations, product, takewhile, islice
from functools import reduce
from math import ceil

allowed_jolt_diff_range = range(1, 4)

current_dir = Path(__file__).parent
file_handler = open(current_dir/"input.txt", 'r')

joltages = [
    int(line.strip())
    for line
    in file_handler.readlines()
]

outlet_joltage = 0
device_joltage = max(joltages) + 3

min_adapter_chain_length = ceil(
    (device_joltage - outlet_joltage) / max(allowed_jolt_diff_range)
)


def get_connections(adapter_joltages):
    with_initial_value = chain(
        [outlet_joltage],
        adapter_joltages
    )
    with_end_value = chain(
        adapter_joltages,
        [device_joltage]
    )
    return zip(
        with_initial_value,
        with_end_value
    )


def is_valid_chain(connections):
    return all(
        y - x in allowed_jolt_diff_range
        for x, y in connections
    )


def count_length_allowed_combinations(length, sorted_joltages):
    pp(f"Checking combinations of length: {length}")
    return sum(
        1 if is_valid_chain(connections) else 0
        for connections in map(
            get_connections,
            combinations(sorted_joltages, length)
        )
    )


def count_allowed_combinations(sorted_joltages):
    lengths = range(len(joltages), min_adapter_chain_length, -1)
    pp(lengths)
    return sum(
        count_length_allowed_combinations(length, sorted_joltages)
        for length in lengths
    )


def get_edges(root, nodes):
    pp(root)
    new_edges = [
        (root, node)
        for node in takewhile(
            lambda node: node - root in {1, 2, 3},
            nodes
        )
    ]



    next_edges = [
        get_edges(
            new_root,
            [
                node
                for node in nodes
                if new_root < node
            ]
        )
        for _, new_root
        in new_edges
    ]

    return new_edges + next_edges


def get_paths(parent, descendants):
    if len(descendants) == 0:
        return
        children = [
            *takewhile(
                lambda descendant: descendant - parent in allowed_jolt_diff_range,
                list(descendants)
            )
        ]

        pp(children)

        # paths = [
        #   [parent, child]
        #   for child in children
        # ]

        # pp(paths)

        # new_paths = [
        #   get_paths(
        #     child,
        #     [
        #       descendant
        #       for descendant
        #       in descendants
        #       if descendant != child
        #     ]
        #   )
        #   for child in children
        # ]

        # pp(new_paths)

        return reduce(
            lambda new_paths, child: new_paths +
            get_paths(
                child,
                [
                    descendant
                    for descendant
                    in descendants
                    if descendant != child
                ]
            ),
            children,
            []
        )

        # return [
        #     prefix +
        #      get_paths([child]
        #     # get_paths(
        #     #     prefix + [child],
        #     #     [
        #     #         descendant
        #     #         for descendant
        #     #         in descendants
        #     #         if descendant != child
        #     #     ]
        #     # )
        #     for child in children
        # ]

# def build_dependency_graph(candidate_nodes):
#   parent, *descendants = candidate_nodes
#   children = [
#     descendant
#     for descendant
#     in descendants
#     if parent - descendant
#   ]
#   return [

#   ]

        # pp(f"root: {root}")
        # return (
        #   root,
        #   tuple(
        #     build_dependency_graph(
        #       candidate_node,
        #       [
        #         new_candidate_node
        #         for new_candidate_node
        #         in candidate_nodes
        #         if new_candidate_node < candidate_node
        #       ]
        #     )
        #     for candidate_node
        #     in candidate_nodes
        #     if root - candidate_node in allowed_jolt_diff_range
        #   )
        # )


sorted_joltages = list(sorted(joltages))
pp(sorted_joltages)

# pp(
#     list(
#         islice(
#             get_edges(0, sorted_joltages),
#             10
#         )
#     )
# )

all_unique = len(sorted_joltages) == len(set(sorted_joltages))
pp(all_unique)

all_adapters_diffs = [
    y - x for x, y
    in get_connections(
        sorted_joltages
    )
]

pp(all_adapters_diffs)
ones_interval_lengths = [
    len(ones)
    for ones
    in "".join(
        map(
            str,
            all_adapters_diffs
        )
    ).split('3')
    if len(ones) > 0
]
pp(ones_interval_lengths)

branches = [
    sum(
        sum(
            1 for combination
            in combinations(
                range(n + 1),
                r
            )
        ) for r
        in range(min(n, 3) + 1)
    )
    for n in ones_interval_lengths
]

pp(branches)

num_combinations = reduce(
    lambda n, m: n * m,
    branches
)

pp(num_combinations)


all_adapters_diff_counts = [
    (
        allowed_diff,
        sum(
            1 if diff == allowed_diff else 0
            for diff in all_adapters_diffs
        )
    )
    for allowed_diff
    in allowed_jolt_diff_range
]

pp(all_adapters_diff_counts)

product_of_1_and_3_diff_counts = \
    all_adapters_diff_counts[0][1] * all_adapters_diff_counts[2][1]

pp(f"Puzzle 1: {product_of_1_and_3_diff_counts}")

# num_allowed_combinations = count_allowed_combinations(sorted_joltages)

# pp(build_dependency_graph(device_joltage, sorted_joltages))

# pp(f"Puzzle 2: {num_allowed_combinations}")

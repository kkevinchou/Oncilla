from lib.vec2d import Vec2d

def circular_pairs(list):
    for i in range(len(list) - 1):
        yield (list[i], list[i + 1])
    else:
        yield (list[i + 1], list[0])

def get_min_max_projection(points, vectors, axis):
    starting_proj = points[0].scalar_projection(axis)
    min_proj = starting_proj
    max_proj = starting_proj

    for i, point in enumerate(points):
        if i == 0:
            continue

        projection = points[i].scalar_projection(axis)

        if projection > max_proj:
            max_proj = projection
        elif projection < min_proj:
            min_proj = projection

    return min_proj, max_proj

def calculate_separating_vectors(points_0, points_1):
    polygon_vectors_0 = [p2 - p1 for p1, p2 in circular_pairs(points_0)]
    polygon_normals_0 = [v.perpendicular().normalized() for v in polygon_vectors_0]

    polygon_vectors_1 = [p2 - p1 for p1, p2 in circular_pairs(points_1)]
    polygon_normals_1 = [v.perpendicular().normalized() for v in polygon_vectors_1]

    axes = set(polygon_normals_0)
    for normal in polygon_normals_1:
        if any([negation in axes for negation in normal.get_negations()]):
            continue
        else:
            axes.add(normal)

    separating_vectors = []

    overlap = True

    for axis in axes:
        min_proj_0, max_proj_0 = get_min_max_projection(points_0, polygon_vectors_0, axis)
        min_proj_1, max_proj_1 = get_min_max_projection(points_1, polygon_vectors_1, axis)

        if max_proj_0 > min_proj_1 and min_proj_0 <= min_proj_1:
            delta = -(max_proj_0 - min_proj_1)
        elif max_proj_1 > min_proj_0 and min_proj_1 <= min_proj_0:
            delta = max_proj_1 - min_proj_0
        else:
            overlap = False
            continue

        separating_vectors.append(axis * delta)

    return separating_vectors, overlap

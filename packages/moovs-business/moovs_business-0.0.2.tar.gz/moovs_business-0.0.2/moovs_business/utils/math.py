import numpy as np
from typing import Union, List, Tuple
from scipy.optimize import linear_sum_assignment as linear_assignment
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import squareform


def _cosine_distance(a, b, data_is_normalized=False):
    """Compute pair-wise cosine distance between points in `a` and `b`.

    Parameters
    ----------
    a : array_like
        An NxM matrix of N samples of dimensionality M.
    b : array_like
        An LxM matrix of L samples of dimensionality M.
    data_is_normalized : Optional[bool]
        If True, assumes rows in a and b are unit length vectors.
        Otherwise, a and b are explicitly normalized to lenght 1.

    Returns
    -------
    ndarray
        Returns a matrix of size len(a), len(b) such that eleement (i, j)
        contains the squared distance between `a[i]` and `b[j]`.

    """
    if not data_is_normalized:
        a = np.asarray(a) / np.linalg.norm(a, axis=1, keepdims=True)
        b = np.asarray(b) / np.linalg.norm(b, axis=1, keepdims=True)
    return 1.0 - np.dot(a, b.T)


def nn_cosine_distance(x, y, data_is_normalized=False):
    """Helper function for nearest neighbor distance metric (cosine).

    Parameters
    ----------
    x : ndarray
        A matrix of N row-vectors (sample points).
    y : ndarray
        A matrix of M row-vectors (query points).

    Returns
    -------
    ndarray
        A vector of length M that contains for each entry in `y` the
        smallest cosine distance to a sample in `x`.

    """
    distances = _cosine_distance(x, y, data_is_normalized=data_is_normalized)
    return distances.min(axis=0)


class NearestNeighborDistanceMetric(object):
    """
    A nearest neighbor distance metric that, for each target, returns
    the closest distance to any sample that has been observed so far.

    Parameters
    ----------
    metric : str
        Either "euclidean" or "cosine".
    matching_threshold: float
        The matching threshold. Samples with larger distance are considered an
        invalid match.
    budget : Optional[int]
        If not None, fix samples per class to at most this number. Removes
        the oldest samples when the budget is reached.

    Attributes
    ----------
    samples : Dict[int -> List[ndarray]]
        A dictionary that maps from target identities to the list of samples
        that have been observed so far.

    """

    def __init__(self, metric, matching_threshold, budget):
        # if metric == "euclidean":
        #    self._metric = nn_euclidean_distance
        # elif metric == "cosine":
        #    self._metric = nn_cosine_distance

        # else:
        #    raise ValueError("Invalid metric; must be either 'euclidean' or 'cosine'")

        # self._metric = torchreid.metrics.distance.compute_distance_matrix
        self._metric = nn_cosine_distance

        self.matching_threshold = matching_threshold
        self.budget = budget
        self.samples = {}
        self.classes = {}

    def terminate(self):
        del self.samples
        del self.classes

    # TODO - partial fit? Why do we need this function
    def partial_fit(self, features, targets, active_targets, active_classes):
        """[Update the distance metric with new data.]

        Args:
            features : ndarray
                An NxM matrix of N targets of dimensionality M.
            targets : ndarray
                An N, integer array of associated target identities.
            active_targets : List[int]
                A list of targets that are currently present in the scene.
            active_classes List[int]
                An N, str array of assocfiiated target classes.
        """
        for feature, target, class_id in zip(features, targets, active_classes):
            # append the features (1,M) per target
            self.samples.setdefault(target, []).append(feature)
            # each target class with its own budget
            self.classes.setdefault(target, self.budget[class_id])

        self.samples = {k: self.samples[k][-self.classes[k] :] for k in active_targets}

    def distance(self, features, targets, debug=False):
        """Compute distance between features and targets.

        Parameters
        ----------
        features : ndarray
            An NxM matrix of N features of dimensionality M.
        targets : List[int]
            A list of targets to match the given `features` against.

        Returns
        -------
        ndarray
            Returns a cost matrix of shape len(targets), len(features), where
            element (i, j) contains the closest squared distance between
            `targets[i]` and `features[j]`.

        """

        cost_matrix = np.zeros((len(targets), len(features)))
        for i, target in enumerate(targets):
            cost_matrix[i, :] = self._metric(self.samples[target], features)
        return cost_matrix


def xyxy_to_tlwh_vectorized(bbox_xyxy: np.ndarray):
    """Convert bounding box coordinates from [x1, y1, x2, y2] to [x, y, w, h] format.
    x1, y1, x2, y2: top left and bottom right coordinates

    Args:
        bbox_xyxy (np.ndarray): bounding box coordinates in [x1, y1, x2, y2] format

    Returns:
        _type_: bounding box coordinates in [x, y, w, h] format
    """
    x1, y1, x2, y2 = np.split(bbox_xyxy, 4, axis=-1)
    t = x1
    tl = y1
    w = x2 - x1
    h = y2 - y1
    return np.concatenate([t, tl, w, h], axis=1)


def xyxy_to_tlwh_(bbox_xyxy: Union[Tuple, List, np.ndarray]):
    """Convert bounding box coordinates from [x1, y1, x2, y2] to [x, y, w, h] format.
    x1, y1, x2, y2: top left and bottom right coordinates

    Args:
        bbox_xyxy (Tuple or Array): bounding box coordinates in [x1, y1, x2, y2] format

    Returns:
        _type_: bounding box coordinates in [x, y, w, h] format
    """
    if isinstance(bbox_xyxy, np.ndarray):
        return xyxy_to_tlwh_vectorized(bbox_xyxy)
    x1, y1, x2, y2 = bbox_xyxy
    t = x1
    tl = y1
    w = x2 - x1
    h = y2 - y1

    return np.array([t, tl, w, h], dtype=np.float32)


def missing_rate(bboxs):
    nb_frames = len(bboxs)

    if nb_frames > 0:
        missing = np.sum(np.isnan(bboxs), axis=0)[0]
        return missing / nb_frames
    else:
        return 1.0


def score_ball(bboxs, scores, volatility: float = None):
    # TODO - we need to take into account the ball movement. Big difference
    """Calculate a score for a ball, given the following criteria:
    The closer to 1 the better
    1. The ball area
    2. The ball score
    3. The ball missing frames
    4. The ball movement standard deviation
    Args:
        bboxs (_type_): position of the track
        scores (_type_): position scores
        frame_shape (_type_): frame shape
    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """
    # if no bboxs return 0
    if len(bboxs) == 0:
        return 0
    # calculate the average score of the track
    mean_score = np.nanmean(scores)
    # calculate the average missing rate
    miss_rate = 1 - missing_rate(bboxs)
    # check ball movement
    return np.nanmean([mean_score, miss_rate])


def calculate_area(bbox_xyxy: Union[List, np.ndarray]):
    if isinstance(bbox_xyxy, list):
        x1, y1, x2, y2 = bbox_xyxy
    else:
        x1, y1, x2, y2 = np.split(bbox_xyxy, 4, axis=-1)
    return np.absolute((x2 - x1) * (y2 - y1))


def score_person(bboxs, scores, frame_shape):
    """Calculate a score for a ball, given the following criteria:
    1. The ball area
    2. The ball score
    3. The ball missing frames
    Args:
        bboxs (_type_): position of the track
        scores (_type_): position scores
        frame_shape (_type_): frame shape
    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """
    if len(bboxs) == 0:
        return 0
    # get width and height
    widht, height = frame_shape[0:2]
    # calculate the average score of the track
    mean_score = np.nanmean(scores)
    # calculate the average missing rate
    miss_rate = 1 - missing_rate(bboxs)
    # calculate the frame size
    frame_size = calculate_area([0, 0, widht, height])
    # calculate the size of the ball
    person_size = np.nanmean(calculate_area(np.array(bboxs)))
    # normalize the ball size
    normalized_area = 0 if person_size == 0 else person_size / frame_size
    # return values
    return np.nanmean([mean_score, miss_rate, normalized_area])


def _pdist(a, b):
    """Compute pair-wise squared distance between points in `a` and `b`.

    Parameters
    ----------
    a : array_like
        An NxM matrix of N samples of dimensionality M.
    b : array_like
        An LxM matrix of L samples of dimensionality M.

    Returns
    -------
    ndarray
        Returns a matrix of size len(a), len(b) such that eleement (i, j)
        contains the squared distance between `a[i]` and `b[j]`.

    """
    a, b = np.asarray(a), np.asarray(b)
    if len(a) == 0 or len(b) == 0:
        return np.zeros((len(a), len(b)))
    a2, b2 = np.square(a).sum(axis=1), np.square(b).sum(axis=1)
    r2 = -2.0 * np.dot(a, b.T) + a2[:, None] + b2[None, :]
    r2 = np.clip(r2, 0.0, float(np.inf))
    return r2


def nn_euclidean_distance(x, y):
    """Helper function for nearest neighbor distance metric (Euclidean).

    Parameters
    ----------
    x : ndarray
        A matrix of N row-vectors (sample points).
    y : ndarray
        A matrix of M row-vectors (query points).

    Returns
    -------
    ndarray
        A vector of length M that contains for each entry in `y` the
        smallest Euclidean distance to a sample in `x`.

    """
    distances = _pdist(x, y)
    return np.maximum(0.0, distances.min(axis=0))


def track_feature_similarity(
    track1_feat, track2_feat, metric, minimum_frames=0.01, budget_dim=50
):
    """Given list of track1 feature descriptors and track2 feature descriptors, calculate the similarity between the two tracks given the metric

    Args:
        track1_feat (np.ndarray): vector of (X1,512) where X1 is the number of frames
        track2_feat (np.ndarray): vector of (X2,512) where X2 is the number of frames
        metric (function): metric to calculate the similarity between the two tracks
        ignored_threshold (float, optional): _description_. Defaults to 0.01.

    Returns:
        [float]: [similarity between the two tracks, 0 not the same, 1 same track]
    """
    # assign the metric with the correct function
    if metric == "cosine":
        metric = nn_cosine_distance
    elif metric == "euclidean":
        metric = nn_euclidean_distance
    else:
        raise ValueError("Invalid metric. Available metrics are cosine and euclidean")

    # ignore tracks that have less than 1% detected frames (compared to the total video)
    total = len(track1_feat)
    minimum_frames_required = minimum_frames * total
    if (
        total - np.any(np.isnan(track1_feat), axis=-1).sum() < minimum_frames_required
        or total - np.any(np.isnan(track2_feat), axis=-1).sum()
        < minimum_frames_required
    ):
        return 0  # not the same
    # calculate the similarity between the two tracks
    # remove nans from the tracks
    track1_feat = track1_feat[~np.isnan(track1_feat).any(axis=1)][-budget_dim:]
    track2_feat = track2_feat[~np.isnan(track2_feat).any(axis=1)][-budget_dim:]
    # calculate the similarity between the two tracks
    similarity = metric(track1_feat, track2_feat)
    # get the mean
    similarity = similarity.mean()
    # if the similarity is above the threshold, then the tracks are considered the same
    return 1 - similarity


def track_missing_similarity(track1_pos, track2_pos, ignored_threshold=0.01):
    """
    Calculate the merging probability between two tracks, given the following criterion:
        If two tracks are potentially the same (1 ball, 2 tracks), then search for the inverse track, when track X have its
        positions infered, logically track Y will have nan's at that time step and vice-versa, since only 1 ball is present.
        Calculte how many times track X differ from Y in terms of Nans. If it matches the size of the video, it means that this
        event is contant throughout all the frames.

    Do not count when bot tracks are nan, for two reasons
        1 - both tracks could start at the end of the video, therefore a great percentage of the positions would be the same
        2 - if the tracks are potentially the same (1 ball, 2 tracks) and if the ball is not detected both will have the same value (nan)

    Attention cases:
        1 - Only account after index > track time step
        2 - If one track has very few tracked positions through the video don't match to the main track.
    Args:
        track1_pos ([np.array]): [track1 positions]
        track2_pos ([np.array]): [track2 positions]

    Returns:
        [float]: [similarity between the two tracks, 0 not the same, 1 same track]
    """
    total = len(track1_pos)
    miss1 = np.isnan(track1_pos).any(axis=1)
    miss2 = np.isnan(track2_pos).any(axis=1)
    # ignore tracks that have less than 1% detected frames (compared to the total video)
    minimum_frames_required = ignored_threshold * total
    if (
        np.invert(miss1).sum() < minimum_frames_required
        or np.invert(miss2).sum() < minimum_frames_required
    ):
        return 0  # not the same
    num_equal_nans = np.logical_and(miss1, miss2).sum()
    num_diff = np.sum(miss1 != miss2)
    assert (
        num_diff <= total - num_equal_nans
    ), "Merge tracks computation error at track_missing_similarity"
    merge_proba = num_diff / (total - num_equal_nans)
    # if merge probability is less than 5% then the tracks are the same
    return merge_proba


def bbox_intersection(person_bbox: np.ndarray, ball_bbox: np.ndarray):
    """Calculate if intersection exists between two bounding boxes."""
    person_bbox = xyxy_to_tlwh_(person_bbox)
    ball_bbox = xyxy_to_tlwh_(ball_bbox)
    x1, y1, w1, h1 = np.split(person_bbox, 4, axis=-1)
    x2, y2, w2, h2 = np.split(ball_bbox, 4, axis=-1)
    x1, x2 = np.maximum(x1, x2), np.minimum(x1 + w1, x2 + w2)
    y1, y2 = np.maximum(y1, y2), np.minimum(y1 + h1, y2 + h2)
    intersection = np.maximum(x2 - x1, 0) * np.maximum(y2 - y1, 0)
    intersection = intersection > 0
    return np.nanmean(intersection)


def sort_tracks_football(tracks):
    """
    Sorts the tracks given a score.
    """
    # isolate tracks by their class
    # [track["class_id"].max() for track in tracks]
    ball_tracks = [track for track in tracks if track["class_id"][0] == 32]
    person_tracks = [track for track in tracks if track["class_id"][0] == 0]
    # define a cost matrix
    cost_matrix = np.zeros(shape=(len(person_tracks), len(ball_tracks)))
    # calculate the cost matrix
    for i, person_track in enumerate(person_tracks):
        pp = 1 - score_person(
            person_track["bbox"], person_track["score"], person_track["shape"]
        )
        for j, ball_track in enumerate(ball_tracks):
            cost_matrix[i, j] = (
                1
                - score_ball(ball_track["bbox"], ball_track["score"])
                + pp
                + 2 * (1 - bbox_intersection(ball_track["bbox"], person_track["bbox"]))
            )

    # run hungarian algorithm here
    row_ind, col_ind = linear_assignment(cost_matrix)

    # remove same ids from row_ind and col_ind (if there are any)
    for index in range(len(person_tracks)):
        if index in row_ind:
            continue
        else:
            row_ind = np.concatenate([row_ind, [index]], axis=0)

    for index in range(len(ball_tracks)):
        if index in col_ind:
            continue
        else:
            col_ind = np.concatenate([col_ind, [index]], axis=0)

    sorted_person_tracks = [person_tracks[i] for i in row_ind]
    sorted_ball_tracks = [ball_tracks[i] for i in col_ind]
    # return the sorted tracks
    return sorted_person_tracks + sorted_ball_tracks


def sort_tracks(tracks, valid_classes: List[int]):
    """
    Sorts the tracks given a score.
    """
    # isolate group of tracks by their class track.class_id
    tracks_by_class = {
        class_id: [track for track in tracks if track["class_id"][0] == class_id]
        for class_id in valid_classes
    }
    # sort all the classes thar are ball with the score_ball function
    sorted_tracks = []
    for class_id, class_tracks in tracks_by_class.items():
        if class_id == 32:
            sorted_tracks += sorted(
                class_tracks,
                key=lambda track: score_ball(
                    track["bbox"], track["score"], track["shape"]
                ),
                reverse=True,
            )
        elif class_id == 0:
            sorted_tracks += sorted(
                class_tracks,
                key=lambda track: score_person(
                    track["bbox"], track["score"], track["shape"]
                ),
                reverse=True,
            )
        else:
            raise Exception("Unknown class")
    return sorted_tracks


def score_tracks(tracks, class_dependent=False, valid_classes: List[int] = [0, 32]):
    """
    Sort the tracks given a score.
    If class_dependent is True, then the objects are depedent when calculating a score.
    One example is Football, where the ball and the players are dependent.
    """
    if class_dependent:
        return sort_tracks_football(tracks)
    else:
        return sort_tracks(tracks, valid_classes)


def group_tracks(similarity_matrix, threshold: float = 0.05):
    """
    This function groups tracks based on similiarity.

    # closest to 1 - same track
    # closest to 0 - different tracks

    It uses the similiarity matrix to construct a distance matrix.
    Then it constructs a hierarchical clustering dendogram using to the distance matrix.
    The linkage method is maximum link. Within a group what is are the most distant tracks.
    The dendrogram, and the threshold is then used to find the desired aggregation ammount.

    We select the maximum grouping where the sum of cluster distance is smaller than the threshold.
    """
    n = similarity_matrix.shape[1]

    # linkage minimizes the distance cost
    distance_matrix = 1 - similarity_matrix  # ( np.eye(n) + cost_matrix)

    z = linkage(squareform(distance_matrix), "complete")

    # hierarchy is used to permforma hierarchical clustering
    hierarchy = []
    # add each element of the track to hierarchy
    hierarchy.append(({str(i): ([i], 0.0, 1) for i in range(n)}, 0.0))

    latest = n

    for z_i in z:
        a, b, dist_ab, count = z_i
        a_key, b_key = str(int(a)), str(int(b))
        new_hierarchy = hierarchy[-1][0].copy()

        members_a, _, _ = new_hierarchy.pop(a_key)
        members_b, _, _ = new_hierarchy.pop(b_key)

        members_ab = members_a + members_b  # joins the two groups

        new_hierarchy[str(latest)] = (
            members_ab,
            (dist_ab),
            int(count),
        )  # new grouping.

        cost = np.max(
            [cost_i for _, cost_i, _ in new_hierarchy.values()]
        )  # grouping cost.
        hierarchy.append((new_hierarchy, cost))

        latest += 1  # next cluster index

    hierarchy.reverse()
    best_ordering = list(filter(lambda x: x[1] <= threshold, hierarchy))
    if len(best_ordering) > 0:
        best_ordering = best_ordering[0]
    else:
        return []

    return [m for m, _, _ in best_ordering[0].values()]

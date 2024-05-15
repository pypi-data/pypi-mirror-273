import numpy as np


class OnlineMovingAverage:
    def __init__(self, beta, bias_correction):
        self.beta = beta
        self.threshold = 1e-8  # fine-tunned value
        self.bias_correction = bias_correction
        self.cache = []
        self.missing = 0
        self.index = 0

    def init_state(self, start_value):
        self.mv_avg = start_value
        self.missing = 0
        self.index = 0
        self.cache.append(start_value)

    def update_state(self, value):
        self.index += 1
        result = self.mv_avg * self.beta + value * (1 - self.beta)

        if self.bias_correction is True:
            # if index is a lower value, (1 - self.beta ** self.index) will be less than 1 increasing the result in initial cases
            result = result / (1 - self.beta**self.index)

        self.mv_avg = result
        self.cache.append(result)

    def dummy_update(self):
        self.cache.append(self.mv_avg)

    def delay(self):
        if isinstance(self.cache[0], np.ndarray):
            # moving average
            self.cache.append(np.ones(self.cache[0].shape))
        else:
            # integer like volatility - std - mean.
            self.cache.append(1)

    def get_cache(self):
        return self.cache[1:]

    def current_estimate(self):
        return self.mv_avg

    def pop(self, index):
        return self.cache.pop(index)


class MovingAverageTracker:
    def __init__(self, name, beta, bias_correction=True):
        """
        Parameters Description:
            name - name of the method
            beta - beta used in the exponential moving average
            bias_correction - bool to determine if a bias correction is performed in th exponential moving average
        """
        self.name = name
        self.beta = beta
        self.bias_correction = bias_correction
        self.ma_ball = OnlineMovingAverage(
            self.beta, bias_correction=self.bias_correction
        )
        self.ma_volatility = OnlineMovingAverage(
            self.beta, bias_correction=self.bias_correction
        )

        self.missing = 0
        self.object_track = []
        self.area_track = []
        self.ontrack = False
        # start counting frames
        self.frame_index = 0

        # self.initiate_tracker()

    def initiate_tracker(self):
        self.ma_ball.init_state(np.zeros(shape=(2, 2)))
        self.ma_volatility.init_state(0)

    def target_update(self, prev_object, volatility):
        self.ma_ball.update_state(prev_object)
        self.ma_volatility.update_state(volatility)

    def target_missing(self):
        self.ma_ball.dummy_update()
        self.ma_volatility.dummy_update()

    def target_delay(self):
        self.ma_ball.delay()
        self.ma_volatility.delay()

    def return_cache(self):
        return self.ma_ball.get_cache(), self.ma_volatility.get_cache()

    def pop(self, index):
        return self.ma_ball.pop(index), self.ma_volatility.pop(index)


# Voltatility std Tracker
class VolatilityTracker(MovingAverageTracker):
    def __init__(
        self,
        growth_factor=2.2,
        beta=0.5,
        bias_correction=True,
        start_std=100,
        eps=1e-4,
        max_std=1000,
    ):
        super(VolatilityTracker, self).__init__(
            name="volatilityTracker", beta=beta, bias_correction=bias_correction
        )

        self.ma_volatility_std = OnlineMovingAverage(beta, bias_correction=False)
        self.growth_factor = growth_factor
        self.start_std = start_std
        self.eps = eps
        self.max_std = max_std
        self.initiate_tracker()

    def initiate_tracker(self):
        super(VolatilityTracker, self).initiate_tracker()
        self.ma_volatility_std.init_state(np.ones(shape=()) * self.start_std)

    def target_update(self, position, volatility):
        super(VolatilityTracker, self).target_update(position, volatility)

        self.ma_volatility_std.update_state(
            np.abs(volatility - self.ma_volatility.current_estimate())
        )

        if self.ma_volatility_std.current_estimate() < self.eps:
            self.ma_volatility_std.mv_avg = self.eps

    def target_missing(self):
        super(VolatilityTracker, self).target_missing()
        current_estimate = self.ma_volatility_std.current_estimate()
        if current_estimate <= self.max_std:
            current_estimate = current_estimate * self.growth_factor
        self.ma_volatility_std.update_state(current_estimate)

    def target_delay(self):
        super(VolatilityTracker, self).target_missing()
        self.ma_volatility_std.update_state(1)

    # return cache
    def return_cache(self):
        return (
            self.ma_volatility_std.get_cache(),
            *super().return_cache(),
        )

    def pop(self, index):
        return (self.ma_volatility_std.pop(index), *super().pop(index))

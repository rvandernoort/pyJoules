# MIT License
# Copyright (c) 2019, INRIA
# Copyright (c) 2019, University of Lille
# All rights reserved.
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from pyJoules.energy_meter import EnergySample


class FakeAPI:
    def reset_values(self):
        raise NotImplementedError()


class CorrectTraceGenerator:
    """
    Generate the correct trace, consistent with given API
    """

    def __init__(self, domains, fake_api, timestamps):
        self.domains = domains
        self.fake_api = fake_api
        self.energy_states = []
        self.correct_timestamps = timestamps
        self.duration_trace = self._compute_duration_trace(timestamps)

        self.energy_states.append(self._get_new_energy_values())

    def _get_new_energy_values(self):
        new_values = {}
        for domain in self.domains:
            new_values[str(domain)] = self.fake_api.domains_current_energy[str(domain)]
        return new_values

    def _compute_duration_trace(self, timestamps):
        duration_trace = []
        current_ts = timestamps[0]
        for next_ts in timestamps[1:]:
            duration_trace.append(next_ts - current_ts)
            current_ts = next_ts
        return duration_trace

    def reset_fake_api_values(self):
        self.fake_api.reset_values()
        self.energy_states.append(self._get_new_energy_values())

    def _compute_energy_trace(self):
        trace = []
        current_state = self.energy_states[0]
        for next_state in self.energy_states[1:]:
            sample = {}
            for domain in self.domains:
                sample[str(domain)] = next_state[str(domain)] - current_state[str(domain)]
            current_state = next_state
            trace.append(sample)
        return trace

    def generate_correct_trace(self, tag_trace):
        trace = []
        energy_trace = self._compute_energy_trace()
        zipped_list = zip(energy_trace, tag_trace, self.duration_trace,
                          self.correct_timestamps)
        for values, tag, duration, timestamp in zipped_list:
            trace.append(EnergySample(timestamp, tag, duration, values))
        return trace

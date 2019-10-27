import math


class DirectFourierTransformer:
    def __init__(self, sequence):
        self.__sequence = sequence

    def get_cosine_component_amplitude(self, harmonic_number):
        sequence_length = len(self.__sequence)
        trigonometric_const_part = 2 * math.pi * harmonic_number / sequence_length
        return 2 * sum(x * math.cos(trigonometric_const_part * i) for i, x in enumerate(self.__sequence)) \
               / sequence_length

    def get_sinus_component_amplitude(self, harmonic_number):
        sequence_length = len(self.__sequence)
        trigonometric_const_part = 2 * math.pi * harmonic_number / sequence_length
        return 2 * sum(x * math.sin(trigonometric_const_part * i) for i, x in enumerate(self.__sequence)) \
               / sequence_length

    def get_amplitude(self, harmonic_number):
        return math.hypot(self.get_cosine_component_amplitude(harmonic_number),
                          self.get_sinus_component_amplitude(harmonic_number))

    def get_initial_phase(self, harmonic_number):
        return math.atan2(self.get_sinus_component_amplitude(harmonic_number),
                          self.get_cosine_component_amplitude(harmonic_number))

    def get_amplitude_spectrum(self, harmonics_count):
        return [self.get_amplitude(j) for j in range(harmonics_count)]

    def get_phase_spectrum(self, harmonics_count):
        return [self.get_initial_phase(j) for j in range(harmonics_count)]

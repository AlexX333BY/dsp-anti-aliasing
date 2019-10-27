from array import array


def central_moving_average(signals, sample_window_width):
    assert sample_window_width > 0, "Sample window width should be positive"
    assert sample_window_width % 2 == 1, "Sample window width should be odd"

    half_width = sample_window_width // 2
    signals_count = len(signals)

    result = array('d')
    for signal_pos in range(signals_count):
        signals_sum = 0.0
        signals_sum_size = 0
        for offseted_signal_pos \
                in range(max(signal_pos - half_width, 0), min(signal_pos + half_width + 1, signals_count)):
            signals_sum += signals[offseted_signal_pos]
            signals_sum_size += 1
        result.append(signals_sum / signals_sum_size)

    return result


def parabolic(signals, divisor, multipliers):
    multipliers_count = len(multipliers)
    assert multipliers_count > 0, "Multipliers shouldn't be empty"
    signals_count = len(signals)

    result = array('d')
    for signal_pos in range(signals_count):
        signals_sum = multipliers[0] * signals[signal_pos]
        for signal_pos_offset in range(1, multipliers_count):
            if signal_pos - signal_pos_offset >= 0:
                signals_sum += multipliers[signal_pos_offset] * signals[signal_pos - signal_pos_offset]
            if signal_pos + signal_pos_offset < signals_count:
                signals_sum += multipliers[signal_pos_offset] * signals[signal_pos + signal_pos_offset]
        result.append(signals_sum / divisor)

    return result


def median_filter(signals, sample_window_width, deleted_elements_count):
    assert sample_window_width > 0, "Sample window width should be positive"
    assert sample_window_width % 2 == 1, "Sample window width should be odd"

    assert deleted_elements_count > 0, "Deleted elements count should be non-negative"
    assert deleted_elements_count <= sample_window_width / 2, \
        "Deleted elements count should be not greater than half size of sample window length"

    half_width = sample_window_width // 2
    half_elements_left = half_width - deleted_elements_count
    signals_count = len(signals)

    result = array('d', signals)
    for signal_pos in range(signals_count):
        window = []
        for i in range(max(signal_pos - half_width, 0), min(signal_pos + half_width + 1, signals_count)):
            window.append(result[i])
        window.sort()
        elements_to_the_left = signal_pos
        how_much_to_delete = max(min(deleted_elements_count, elements_to_the_left - half_elements_left), 0)
        for i in range(how_much_to_delete):
            window.pop(0)
        elements_to_the_right = signals_count - signal_pos - 1
        how_much_to_delete = max(min(deleted_elements_count, elements_to_the_right - half_elements_left), 0)
        for i in range(how_much_to_delete):
            window.pop()
        result[signal_pos] = sum(window) / len(window)
    return result

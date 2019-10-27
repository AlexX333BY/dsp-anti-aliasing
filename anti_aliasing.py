from array import array


def central_moving_average(signals, sample_window_width):
    assert (sample_window_width > 0), "Sample window width should be positive"
    assert (sample_window_width % 2 == 1), "Sample window width should be odd"

    half_width = sample_window_width / 2
    signals_count = len(signals)

    result = array('i')
    for signal_pos in range(signals_count):
        signals_sum = signals[signal_pos]
        signals_sum_size = 1
        for signal_pos_offset in range(1, half_width + 1):
            if signal_pos - signal_pos_offset >= 0:
                signals_sum += signals[signal_pos - signal_pos_offset]
                signals_sum_size += 1
            if signal_pos + signal_pos_offset < signals_count:
                signals_sum += signals[signal_pos + signal_pos_offset]
                signals_sum_size += 1
        result.append(signals_sum / signals_sum_size)

    return result
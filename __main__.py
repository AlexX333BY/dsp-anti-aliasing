from array import array
import math
import random
import argparse
import anti_aliasing
from fourier_transform import DirectFourierTransformer
import graphs


def generate_signals(b1, b2, n):
    const_trigonometric_part = 2 * math.pi / n
    result = array('d')
    for i in range(n):
        signal_trigonometric_part = const_trigonometric_part * i
        result.append(b1 * math.sin(signal_trigonometric_part)
                      + sum(math.pow(-1, random.randint(0, 1)) * b2 * math.sin(signal_trigonometric_part * j)
                            for j in range(50, 70)))
    return result


def moving_average(signals):
    parser = argparse.ArgumentParser()
    parser.add_argument('--moving-average-window', action='store', required=False, help='moving average window width',
                        dest='moving_average_window', type=int, default=3)
    args = parser.parse_known_args()[0]
    return anti_aliasing.central_moving_average(signals, args.moving_average_window)


def parabolic(signals):
    parser = argparse.ArgumentParser()
    parser.add_argument('--parabolic-divisor', action='store', required=True, help='parabolic divisor',
                        dest='parabolic_divisor', type=int)
    parser.add_argument('--parabolic-multipliers', action='store', required=True, help='parabolic multipliers',
                        dest='parabolic_multipliers', type=int, nargs='+')
    args = parser.parse_known_args()[0]
    return anti_aliasing.parabolic(signals, args.parabolic_divisor, args.parabolic_multipliers)


def median(signals):
    parser = argparse.ArgumentParser()
    parser.add_argument('--median-window', action='store', required=False, help='median filter window width',
                        dest='median_window', type=int, default=5)
    parser.add_argument('--median-deleted-count', action='store', required=True, help='median deleted signals count',
                        dest='median_deleted_count', type=int)
    args = parser.parse_known_args()[0]
    return anti_aliasing.median_filter(signals, args.median_window, args.median_deleted_count)


def main():
    tasks_callbacks = {'moving-average': moving_average, 'parabolic': parabolic, 'median': median}

    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--method', action='store', required=True, help='anti-aliasing method',
                        choices=tasks_callbacks.keys(), dest='method', type=str)
    parser.add_argument('-b1', action='store', required=True, help='main signal amplitude', dest='b1', type=float)
    parser.add_argument('-b2', action='store', required=True, help='noise amplitude', dest='b2', type=float)
    parser.add_argument('-n', action='store', required=False, help='counts', dest='n', type=int, default=512)

    args = parser.parse_known_args()[0]
    signals = generate_signals(args.b1, args.b2, args.n)
    amplitude_spectrum_before = DirectFourierTransformer(signals).get_amplitude_spectrum(len(signals) // 2)

    anti_aliased_signals = tasks_callbacks[args.method](signals)
    amplitude_spectrum_after = DirectFourierTransformer(anti_aliased_signals) \
        .get_amplitude_spectrum(len(anti_aliased_signals) // 2)

    drawer = graphs.GraphDrawer()
    drawer.add_plot(graphs.Graph(range(len(signals)), signals, 'Original signals'))
    drawer.add_stem(graphs.Graph(range(len(amplitude_spectrum_before)), amplitude_spectrum_before,
                                 'Original signals amplitude spectrum'))
    drawer.add_plot(graphs.Graph(range(len(anti_aliased_signals)), anti_aliased_signals, 'Anti-aliased signals'))
    drawer.add_stem(graphs.Graph(range(len(amplitude_spectrum_after)), amplitude_spectrum_after,
                                 'Anti-aliased signals amplitude spectrum'))
    drawer.draw()
    drawer.show()


if __name__ == "__main__":
    main()

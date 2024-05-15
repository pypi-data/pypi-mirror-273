import logging
import numpy as np
import pandas as pd

logger = logging.getLogger('laff')

def sequential_findflares(data) -> list:
    logger.debug("Starting sequential_findflares()")

    data_original = data.copy()

    # Apply smoothing function.
    data['smoothed_flux'] = 10**(np.log10(data['flux']).rolling(window=3).mean())
    data.at[0, 'smoothed_flux'] = data['flux'].iloc[0]

    final_index = len(data.flux) - 2
    n = 0
    prev_start, prev_decay = 0, 0

    FLARES = []

    while n < final_index:

        logger.debug(f"Looking at index {n}")

        dev_start = n
        dev_count = 0
        
        # Run deviation check.
        if data.iloc[n+1].smoothed_flux > data.iloc[n].smoothed_flux:
            dev_count = 1
            if n+dev_count+1 >= final_index:
                n = final_index
                continue
            while data.iloc[n+dev_count+1].smoothed_flux >= data.iloc[n+dev_count].smoothed_flux:
                dev_count += 1

        if dev_count >= 2:
            logger.debug(f"Possible deviation from {dev_start}->{dev_start+dev_count}")

            start_point = find_start(data, dev_start, prev_decay)
            peak_point = find_peak(data, start_point)

            logger.debug(f'Possible flare rise from {start_point}->{peak_point}')

            if check_rise(data, start_point, peak_point):
                decay_point = find_decay(data, peak_point)
                checks = [check_noise(data, start_point, peak_point, decay_point),
                          check_above(data, start_point, decay_point),
                          check_decay_shape(data, peak_point, decay_point)]
                logger.debug(f"Checks: {checks}")

                if all(checks):
                    FLARES.append([start_point, peak_point, decay_point])
                    logger.debug(f"Confirmed flare::  {start_point, peak_point, decay_point}")
                    n = decay_point + 1
                    prev_decay = decay_point
                    continue
                else:
                    # All checks failed.
                    logger.debug("Flare failed passing all tests - discarding.")
            else:
                # Check failed.
                logger.debug(f"Deviations has NOT passed checks - discarding")
        else:
            # dev_count not greater than 2, move on.
            pass

        n += 1

    # Reset data.
    data = data_original.copy()
    return FLARES

def find_start(data: pd.DataFrame, start: int, prev_decay: int) -> int:
    """Return flare start by looking for local minima."""
    if start < 3:
        points = data.iloc[0:3]
    else:
        points = data.iloc[start-3:start+1]
    minimum = data[data.flux == min(points.flux)].index.values[0]
    minimum = (minimum + 1) if (minimum <= prev_decay) else minimum
    logger.debug(f"Flare start found at {minimum}")

    return minimum

def find_peak(data, start):
    """
    Return flare peak by looking for local maxima.

    Starting at point {start}, look for the peak of the flare. Since this could
    be one, or many points away a moving average algorithm is used. Work out
    the average of 5 point chunks and see if this is still rising. Until the
    rise stops, continue to search. Once a decay has been found, the peak is the
    datapoint with maximum value.

    :param data: The pandas dataframe containing the lightcurve data.
    :param start: Integer position of the flare start.
    :return: Integer position of the flare peak.
    """

    chunksize = 5
    prev_chunk = data['flux'].iloc[start] # Flare start position is first point.
    next_chunk = np.average(data.iloc[start+1:start+1+chunksize].flux) # Calculate first 'next chunk'.
    i = 1

    while next_chunk > prev_chunk:
        logger.debug(f"Looking at chunk i={i} : {(start+1)+(chunksize*i)}->{(start+1+4)+(chunksize*i)}")
        # Next chunk interation.
        i += 1
        print('chunk is this', data.iloc[(start+1)+(chunksize*i):(start+1+chunksize)+(chunksize*i)])
        prev_chunk = next_chunk
        next_chunk = np.average(data.iloc[(start+1)+(chunksize*i):(start+1+chunksize)+(chunksize*i)].flux)
    else:
        # Data has now begin to descend so look for peak up to these points.
        # Include next_chunk in case the peak lays in this list, but is just
        # brought down as an average by remaining points.
        points = data.iloc[start:(start+1+chunksize)+(chunksize*i)]
        maximum = data[data.flux == max(points.flux)].index.values[0]

        logger.debug(f"Flare peak found at {maximum}")
    return maximum

def find_decay(data: pd.DataFrame, peak: int) -> int:
    """
    Find the end of the flare as the decay smoothes into continuum.

    Longer description.

    :param data:
    :param peak:
    :returns:
    """
    decay = peak
    condition = 0
    decaypar = 2

    logger.debug(f"Looking for decay")

    def calc_grad(data: pd.DataFrame, idx1: int, idx2: int) -> int:
        """Calculate gradient between first (idx1) and second (idx2) points."""
        deltaFlux = data.iloc[idx2].flux - data.iloc[idx1].flux
        deltaTime = data.iloc[idx2].time - data.iloc[idx1].time
        return deltaFlux/deltaTime

    while condition < decaypar:
        decay += 1
        if data.idxmax('index').time in [decay + i for i in range(-1,2)]:
            logger.debug(f"Reached end of data, automatically ending flare at {decay +1}")
            return data.idxmax('index').time

        # Calculate gradients.
        NextAlong = calc_grad(data, decay, decay+1)
        PrevAlong = calc_grad(data, decay-1, decay)
        PeakToCurrent = calc_grad(data, peak, decay)
        PeakToPrev = calc_grad(data, peak, decay-1)

        cond1 = NextAlong > PeakToCurrent # Next sequence is shallower than from peak to next current.
        cond2 = NextAlong > PrevAlong # Next grad is shallower than previous grad.
        cond3 = PeakToCurrent > PeakToPrev # Peak to next point is shallower than from peak to previous point.

        # Evaluate conditions.
        if cond1 and cond2 and cond3:
            condition += 1
        elif cond1 and cond3:
            condition += 0.5
        else:
            # condition = 0
            condition -= 0.5 if condition >= 0.5 else 0

    logger.debug(f"Decay end found at {decay}")

    return decay


    # once end is found we will check if the flare is 'good'
    # if flare is good, accept it and continue search -> from end + 1
    # if flare is not good, disregard and continue search from deviation + 1

def check_rise(data: pd.DataFrame, start: int, peak: int) -> bool:
    """Test the rise is significant enough."""
    if data.iloc[peak].flux > data.iloc[start].flux + (2 * data.iloc[start].flux_perr):
        logger.debug("check_rise: true")
        return True
    else:
        logger.debug("check_rise: false")
        return False


def check_noise(data: pd.DataFrame, start: int, peak: int, decay: int) -> bool:
    """Check if flare is greater than x1.75 the average noise across the flare."""
    average_noise = abs(np.average(data.iloc[start:decay].flux_perr)) + abs(np.average(data.iloc[start:decay].flux_nerr))
    flux_increase = data.iloc[peak].flux - data.iloc[start].flux
    logger.debug(f"noise: {average_noise} | delta_flux: {flux_increase}")
    return True if flux_increase > 1.75 * average_noise else False

# def check_shape(data: pd.DataFrame, start: int, peak:int, decay:int) -> bool:
    # """Check the shape of the flare."""

def check_above(data: pd.DataFrame, start: int, decay: int) -> bool:
    """
    Check the flare is above the (estimated) continuum.
    
    We calculate the powerlaw continuum through the flare by solving a set of
    power functions for (x, y) co-ordinates corresponding to the found flare
    start and end times. The number of points above and below the slope can then
    be found. If the fraction above the continuum is below 0.7, to allow some
    variation through noise, we discard the flare.

    """
    # Check flare boundaries.
    start = 0 if start == 0 else start - 1
    decay = data.idxmax('index').time if decay == data.idxmax('index').time else decay + 1

    x_coords = data['time'].iloc[start], data['time'].iloc[decay]
    y_coords = data['flux'].iloc[start], data['flux'].iloc[decay]

    ## Solving y = nx^a for start and stop.
    alpha = np.emath.logn(x_coords[1]/x_coords[0], y_coords[1]/y_coords[0])
    norm = y_coords[1] / x_coords[1] ** alpha
    # logger.debug(f"ALPHA IS {alpha}")
    # logger.debug(f"NORM IS {norm}")
    
    points_above = sum(flux > (norm*time**alpha) for flux, time in zip(data['flux'].iloc[start:decay], data['time'].iloc[start:decay]))
    num_points = len(data['flux'].iloc[start:decay])

    logger.debug(f"points above/num_points => {points_above}/{num_points} = {points_above/num_points}")
    return True if points_above/num_points >= 0.7 else False

def check_decay_shape(data: pd.DataFrame, peak: int, decay: int):

    decay_data = list(data.iloc[peak:decay].flux_perr)
    count_decrease = sum(b < a for a, b in zip(decay_data, decay_data[1:]))
    decay_shape = count_decrease / len(decay_data)
    # print("DECAY SHAPE VALUE", decay_shape)
    return True if decay_shape > 0.7 else False
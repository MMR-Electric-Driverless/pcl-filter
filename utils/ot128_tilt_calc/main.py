from params import *
from math import radians

def main(args=None):

    min_angle = FOV_MIN_ANGLE
    max_angle = FOV_MAX_ANGLE
    min_tilt_angle = FOV_MIN_ANGLE + TILT_ANGLE
    max_tilt_angle = FOV_MAX_ANGLE + TILT_ANGLE
    fov = abs(FOV_MIN_ANGLE) + abs(FOV_MAX_ANGLE)
    rays = RAYS
    in_rays = INPUT    
    dist = [FOV_MIN_ANGLE] + DISTRIBUTION + [FOV_MAX_ANGLE]
    
    print(f'[INFO] [tilt_angle]: {radians(TILT_ANGLE)}\n')

    ranges = []
    ranges_unclipped = []
    for i in range(len(dist) - 1):
        start = dist[i] + TILT_ANGLE
        end = dist[i + 1] + TILT_ANGLE
        if start > 0:
            break
        if end > 0:
            ranges.append((start, 0))
        else:
            ranges.append((start, end))
        ranges_unclipped.append((start, end))

    if DEBUG:
        print(f'[INFO] [ranges]: {ranges}\n')
    
    if min_angle < 0:
        clip_fov = abs(min_tilt_angle - max_tilt_angle)
        acc = 0.0
        for i, r in enumerate(ranges):
            if r[0] < 0:
                # Handle split ranges crossing zero
                if r[1] < 0:
                    delta = abs(r[0] - r[1]) / clip_fov
                else:
                    delta = abs(r[0]) / clip_fov
                try:
                    ds_factor = int(in_rays / (fov / abs(ranges_unclipped[i][0] - ranges_unclipped[i][1])) / rays[i])
                except ZeroDivisionError:
                    ds_factor = 1  # fallback
                print(f'- "start: {acc:.3f}, end: {acc + delta:.3f}, downsample: {ds_factor}"')
                if DEBUG:
                    print(f'[INFO] [range]: {r[0]}, {r[1]}, {rays[i]}')
                acc += delta
    else:
        print('[ERROR]: with this range the lidar won’t see any cone!')

if __name__ == '__main__':
    main()

import os
import json
import numpy as np
from glob import glob
from datetime import datetime, timedelta

from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import visual, event, core

SUBJECT = 'test'
RUN = 1


if __name__ == '__main__':
    assert RUN in [1, 2, 3, 4, 5]
    with open(f'runs/{RUN}.json', 'r') as f:
        run_info = json.load(f)
    timelabel = datetime.now().strftime('%Y%m%d-%H%M%S')
    os.makedirs('logs', exist_ok=True)
    out_fn = f'logs/{SUBJECT}_{RUN}_{timelabel}.json'
    results = {'stim_events': [], 'key_events': [], 'subject': SUBJECT, 'run': RUN}

    event.globalKeys.add(
        key='q', modifiers=['ctrl'], func=core.quit)

    win = visual.Window(
        size=[1280, 1024], allowGUI=False, units='pix',
        screen=1, rgb=[-1, -1, -1], fullscr=True)


    clips = {}
    # for fn in sorted(glob(os.path.join('stimuli', '*', '*.mp4'))):
    for trial in run_info:
        fn = trial[0]
        if fn not in clips:
            clips[fn]  = visual.MovieStim3(
                win, fn, size=(1280, 940), name=fn, noAudio=True, loop=True)

    fixation = visual.TextStim(win, text='+', height=31, pos=(0, 0), color='#FFFFFF')
    intro_text = "Please pay attention to these clips.\nPress the first (left) button whenever you see a repeated clip."
    intro = visual.TextStim(win, text=intro_text, height=31, wrapWidth=900)

    intro.draw()
    win.flip()
    print('Waiting for trigger')

    event.waitKeys(keyList=['5'])
    print('Starting experiment')
    clock = core.Clock()
    exp_start_time = datetime.now() - timedelta(seconds=clock.getTime())
    results['exp_start_time'] = exp_start_time.strftime('%Y%m%d-%H%M%S')

    for stim_name, start_time, end_time in run_info:
        clip = clips[stim_name]

        while clock.getTime() < start_time:
            fixation.draw()
            win.flip()
        actual_start_time = clock.getTime()

        while clock.getTime() < end_time:
            keys = event.getKeys(timeStamped=clock)
            for key, time in keys:
                if key in ['1', '2', '3', '4', '5']:
                    results['key_events'].append([key, time])
            clip.draw()
            win.flip()
        actual_end_time = clock.getTime()
        results['stim_events'].append([stim_name, actual_start_time, actual_end_time])

    end_time += 18
    while clock.getTime() < end_time:
        fixation.draw()
        win.flip()

    keys = event.getKeys(timeStamped=clock)
    for key, time in keys:
        if key in ['1', '2', '3', '4', '5']:
            results['key_events'].append([key, time])

    exp_end_time = exp_start_time + timedelta(seconds=clock.getTime())
    results['exp_end_time'] = exp_end_time.strftime('%Y%m%d-%H%M%S')
    print(exp_start_time, exp_end_time)

    with open(out_fn, 'w') as f:
        json.dump(results, f)

    win.close()
    core.quit()

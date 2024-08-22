import os
import json
import numpy as np
from glob import glob
from datetime import datetime, timedelta

from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import visual, event, core


if __name__ == '__main__':
    # read subject ID
    with open("../sid.txt", "r") as file:
        sid = file.read() 
    
    # automatically update run number
    logs = glob(f'logs/{sid}*finish.json')
    runs = [int(log.split('_')[1][3:]) for log in logs]
    run_ = 1 if not runs else max(runs) + 1
    assert run_ in [1, 2, 3, 4, 5]

    with open(f'runs/{run_}.json', 'r') as f:
        run_info = json.load(f)
    timelabel = datetime.now().strftime('%Y%m%d-%H%M%S')
    os.makedirs('logs', exist_ok=True)
    finish_fn = f'logs/{sid}_run{run_}_{timelabel}_finish.json'
    start_fn = f'logs/{sid}_run{run_}_{timelabel}_start.json'
    results = {'stim_events': [], 'key_events': [], 'subject': sid, 'run': run_}

    event.globalKeys.clear()
    event.globalKeys.add(key='q', modifiers=['ctrl'], func=os._exit, func_args=[1], func_kwargs=None)

    win = visual.Window(
        size=[1920, 1080], allowGUI=False, units='pix',
        screen=0, color='#000000', fullscr=True)

    clips = {}
    # for fn in sorted(glob(os.path.join('stimuli', '*', '*.mp4'))):
    for trial in run_info:
        fn = trial[0]
        if fn not in clips:
            clips[fn]  = visual.MovieStim3(
                win, fn, size=(1472, 1080), name=fn, noAudio=True, loop=True)

    fixation = visual.TextStim(win, text='+', height=80, pos=(0, 0), color='#FFFFFF')
    intro_text = "Please pay attention to these clips.\n\nPress the left button (button 1) whenever you see an immediate repeat of the same clip."
    intro = visual.TextStim(win, text=intro_text, height=70, wrapWidth=1400, alignText='left')

    intro.draw()
    win.flip()
    print('Waiting for trigger')

    event.waitKeys(keyList=['5'])
    print('Starting experiment')
    clock = core.Clock()
    exp_start_time = datetime.now() - timedelta(seconds=clock.getTime())
    results['exp_start_time'] = exp_start_time.strftime('%Y%m%d-%H%M%S')

    with open(start_fn, 'w') as f:
        json.dump(results, f)   # in case the experiment is terminated prematurely

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
        keys = event.getKeys(timeStamped=clock)
        for key, time in keys:
            if key in ['1', '2', '3', '4', '5']:
                results['key_events'].append([key, time])
        fixation.draw()
        win.flip()

    exp_end_time = exp_start_time + timedelta(seconds=clock.getTime())
    results['exp_end_time'] = exp_end_time.strftime('%Y%m%d-%H%M%S')
    print(exp_start_time, exp_end_time)

    with open(finish_fn, 'w') as f:
        json.dump(results, f)

    win.close()
    core.quit()

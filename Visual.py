from psychopy import visual, core, gui, data
from psychopy.hardware import keyboard
import numpy as np
import random, os, sys

kb = keyboard.Keyboard()
win = visual.Window(
    size=[400, 400],
    units="pix",
    fullscr=False,
    color=[-1, -1, -1]
)


info = {
    'Subject Number': '',
    'Handedness': ['Left', 'Right', 'Ambidextrous']
}
dlg = gui.DlgFromDict(info, title="Participant Information")
if not dlg.OK:
    core.quit()

# Construct the data path and check for existing file
data_path = f"{info['Subject Number']}.csv"
if os.path.exists(data_path):
    sys.exit(f"Data path {data_path} already exists!")


welcome_text = visual.TextStim(win=win, text="""Welcome to the experiment! 
Press the Y key if a blue circle is visible. 
Press N key if no blue circle is visible. 

Press any key to begin.""", color=[1, 1, 1])  
welcome_text.draw()
win.flip()
kb.waitKeys()

# Trial setup
num_trials = 10  
num_circles = 25 
radius = 15  # Radius in pixels

# TrialHandler
trials = data.TrialHandler(nReps=num_trials, method="sequential", trialList=[{}])
trials.data.addDataType("response")  # for response (Y/N)
trials.data.addDataType("response_time")  
trials.data.addDataType("target_present")  # if the blue circle was present

#function to make sure circles do not overlap
def create_random_circle(win, color, radius, existing_positions):
    while True:
        x_pos = random.randint(-180 + radius, 180 - radius)
        y_pos = random.randint(-180 + radius, 180 - radius)
        pos = (x_pos, y_pos)
        if all(np.linalg.norm(np.array(pos) - np.array(existing)) > 2 * radius for existing in existing_positions):
            return visual.Circle(win=win, units="pix", radius=radius, fillColor=color, lineColor=[-1, -1, -1], pos=pos)


for trial in trials:
    circles = []
    # Generate red circles with random positions
    for _ in range(num_circles):
        circle = create_random_circle(win, color=[1, -1, -1], radius=radius, existing_positions=[c.pos for c in circles])
        circles.append(circle)
    
  
    show_blue_circle = random.random() < 0.8  # True 80% of the time, False 20% of the time
    blue_circle = None
    if show_blue_circle:
        blue_circle = create_random_circle(win, color=[0, 0, 1], radius=radius, existing_positions=[c.pos for c in circles])


    for circle in circles:
        circle.draw()
    if blue_circle:
        blue_circle.draw()
    
    win.flip()
    

    kb.clearEvents()  # Clear previous events
    start_time = core.getTime()
    response = kb.waitKeys(keyList=["y", "n"])[0]  # Wait for a response
    response_time = response.rt 
    response_key = response.name  

  
    trials.data.add("response", response_key)
    trials.data.add("response_time", response_time)
    trials.data.add("target_present", show_blue_circle)
    
print(f"Trial {trials.thisN + 1}: {'Blue circle present' if show_blue_circle else 'No blue circle'}, "
      f"Response: {response_key}, Response Time: {response_time if response_time is not None else 'N/A'} seconds")



ycore.wait(0.5)  

# Save data to file
trials.saveAsText(data_path, delim=",")
print(f"Data saved to {data_path}")

win.close()
core.quit()


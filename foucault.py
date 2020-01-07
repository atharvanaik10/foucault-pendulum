GlowScript 2.7 VPython
scene.title = "Foucault Pendulum\n"

running = False

def Run(b):
    global running
    running = not running
    if running: b.text = "Pause"
    else: b.text = "Run"

button(text="Run", pos=scene.title_anchor, bind=Run)
## constants
g = 9.8         # acceleration due to gravity
time = 0           # start counting time at zero
dt = .001   # time step




theta1 = 0.174533 # starting angle in rads
L1 = 1.25     # string length
m1 = 0.16556  # ball mass in kg
v1 = vector(0,0,0)  # initial velocity of pendulum (x,y,z) directions
p1 = m1*v1 # starting momentum


#tension in string
k = 1e5

## create the ceiling, masses, and strings
ceiling = box(pos=vector(0,1,0), size = vector(0, 0, 0))
ball1 = sphere(pos=vector(ceiling.pos.x-L1*sin(theta1),ceiling.pos.y-L1*cos(theta1),0), radius=0.02, color=color.green)

string1 = cylinder(pos=ceiling.pos, axis=ball1.pos-ceiling.pos, color=color.white, radius=0.002)
plate = cylinder(pos = vec(ceiling.pos.x, ceiling.pos.y - 1.27, ceiling.pos.z), size = vec(0.01,0.4,0.4), axis= vec(0,-1,0), color = color.white)
plate1 = compound([plate])
plate1.texture = "https://upload.wikimedia.org/wikipedia/commons/9/97/The_Earth_seen_from_Apollo_17.jpg"
#Slider
lat = 0
scene.caption = "\n"
scene.append_to_caption("Latitude (90 is the north pole, 0 is equator):\n\n")
def latitude(s):
    wt.text = '{:.0f}'.format(s.value)
    lat = s.value
sl = slider(min=0, max=90, step = 5, left = 200, length = 1000, length=150, bind=latitude)
wt = wtext(text='{:.0f}'.format(sl.value))
scene.append_to_caption(' degrees')

#Graph
gd = graph(x = 0, y = 0, width = 400, height = 200, xtitle = 'time(hr)', ytitle = 'plate rotation', xmax = 24, xmin = 0, ymax = 2, ymin = -2)
position = series(graph = gd, color = color.blue, label = "position")

gd1 = graph(x = 0, y = 0, width = 400, height = 200, xtitle = 'time(hr)', ytitle = 'pendulum movement', xmax = 24, xmin = 0, ymax = 2, ymin = -2)
pend = series(graph = gd1, color = color.red, label = 'pendulum')

gd2 = graph(x = 0, y = 0, width = 400, height = 200, xtitle = 'time(hr)', ytitle = 'momentum (x dir)', xmax = 24, xmin = 0, ymax = 2, ymin = -2)
momentum = series(graph = gd2, color = color.green, label = 'momentum')

## calculation loop
while True:
    rate(1000)
    if(running):
      # calc radial vectors and forces
      r1 = vector(ball1.pos.x - ceiling.pos.x,ball1.pos.y - ceiling.pos.y,ball1.pos.z - ceiling.pos.z)
      F1 = m1*vector(0,-g,0) - k*(r1 - L1*r1.norm())#norm is the unit vector #Force gravity - spring force (tension)

      p1 = p1 + F1*dt #change in momentum of pendulum
      ball1.pos.x = (ball1.pos + (p1/m1)*dt).x
      ball1.pos.y = (ball1.pos + (p1/m1)*dt).y#change in position of pendulum
      plate1.axis = vec(cos((2*pi*sin(sl.value)/24)*time),0,sin((2*pi*sin(sl.value)/24)*time))
      position.plot(time,plate1.axis.z)
      pend.plot(time, ball1.pos.x)
      momentum.plot(time,p1.x)
      string1.axis = ball1.pos - ceiling.pos #rotates string
      time = time + dt
      

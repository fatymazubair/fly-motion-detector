import numpy as np
import matplotlib.pyplot as plt

dt = 0.001                      # time step (s)
t = np.arange(0, 2, dt)         # 2 seconds

def lowpass(signal, tau):
    """Delays/smooths a signal (tau = delay time constant)."""
    out = np.zeros_like(signal)
    a = dt / (tau + dt)
    for i in range(1, len(signal)):
        out[i] = out[i-1] + a * (signal[i] - out[i-1])
    return out

def reichardt(A, B, tau):
    return lowpass(A, tau) * B - lowpass(B, tau) * A

def grating(x, t, wavelength, speed):
    """Moving stripes. Positive speed = rightward."""
    return np.sin(2*np.pi*(x - speed*t)/wavelength)

d = 0.2            # spacing between sensors
wl = 1.0           # stripe width (wavelength)
tau = 0.05         # delay

for speed in [+0.5, -0.5]:
    A = grating(0, t, wl, speed)
    B = grating(d, t, wl, speed)
    R = reichardt(A, B, tau)
    print(speed, "→ mean output:", R[500:].mean())   # skip start-up


#PLOT THE TUNING CURVE
speeds = np.linspace(-3, 3, 61)
resp = []
for v in speeds:
    A = grating(0, t, wl, v)
    B = grating(d, t, wl, v)
    resp.append(reichardt(A, B, tau)[500:].mean())

plt.plot(speeds, resp)
plt.axhline(0, color='k')
plt.xlabel("Stimulus speed (negative = leftward)")
plt.ylabel("Mean detector output")
plt.show()

#FOR STREAMLIT

import streamlit as st
st.title("Fly Motion Detector")
tau = st.slider("Delay (s)", 0.01, 0.2, 0.05)
d = st.slider("Sensor spacing", 0.05, 0.5, 0.2)
wl = st.slider("Stripe width", 0.5, 2.0, 1.0)
# ...compute tuning curve with these values...
fig, ax = plt.subplots()
ax.plot(speeds, resp)
st.pyplot(fig)

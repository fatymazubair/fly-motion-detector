import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

dt = 0.001
t = np.arange(0, 2, dt)

def lowpass(signal, tau):
    out = np.zeros_like(signal)
    a = dt / (tau + dt)
    for i in range(1, len(signal)):
        out[i] = out[i-1] + a * (signal[i] - out[i-1])
    return out

def reichardt(A, B, tau):
    return lowpass(A, tau) * B - lowpass(B, tau) * A

def grating(x, t, wavelength, speed):
    return np.sin(2*np.pi*(x - speed*t)/wavelength)

def tuning_curve(d, wl, tau):
    speeds = np.linspace(-3, 3, 41)
    resp = []
    for v in speeds:
        A = grating(0, t, wl, v)
        B = grating(d, t, wl, v)
        resp.append(reichardt(A, B, tau)[500:].mean())
    return speeds, resp

def two_frame_test(sign, tau):
    n = 200
    A = np.zeros(n)
    B = np.zeros(n)
    A[20:70] = 1        # frame 1: bright dot at sensor A
    B[70:120] = sign    # frame 2: dot at sensor B (+1 bright, -1 dark)
    return reichardt(A, B, tau).sum(), A, B

st.title("Fly Motion Detector")

# 1. sliders first
tau = st.slider("Delay (s)", 0.01, 0.2, 0.05)
d = st.slider("Sensor spacing", 0.05, 0.5, 0.2)
wl = st.slider("Stripe width", 0.5, 2.0, 1.0)

# 2. compute using the slider values
speeds, resp = tuning_curve(d, wl, tau)

# 3. plot
fig, ax = plt.subplots()
ax.plot(speeds, resp)
ax.axhline(0, color="k")
ax.set_xlabel("Stimulus speed (negative = leftward)")
ax.set_ylabel("Mean detector output")
st.pyplot(fig)

st.header("Reverse-phi illusion")
reverse = st.checkbox("Reverse contrast (reverse-phi)")
sign = -1 if reverse else 1

out, A, B = two_frame_test(sign, tau)   # tau comes from the slider

if out > 0:
    st.markdown("## → Rightward motion detected")
else:
    st.markdown("## ← Leftward motion detected")
st.write(f"Detector output: {out:.2f}")

fig2, ax2 = plt.subplots()
ax2.plot(A, label="Sensor A")
ax2.plot(B, label="Sensor B")
ax2.set_xlabel("Time (ms)")
ax2.set_ylabel("Light level")
ax2.legend()
st.pyplot(fig2)


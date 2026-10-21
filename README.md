# Can a Fly's Motion Detector Be Fooled?

A small interactive model of how a fly detects motion, and how that same circuit can be tricked into seeing movement in the wrong direction.

**Live app:** https://fly-motion-detector-svfhwid2wzxkn95pcv427h.streamlit.app/

---

## Why I made this

I come from a biophysics background and I'm teaching myself computational neuroscience. I'm a beginner at programming, so I wanted a project small enough that I could understand every line, but with an actual scientific idea behind it and not just a tutorial copy.

Fly motion vision is a good fit. It's one of the best-understood circuits in neuroscience, the core idea fits in a few lines of maths, and there's a real illusion you can reproduce with it.

## The biology in short

Flies need to know which way things are moving to steer and avoid crashing. In the fly visual system, neurons called **T4** (respond to bright moving edges) and **T5** (respond to dark moving edges) are the first cells that care about direction. Each type comes in four subtypes, one for each direction.

When I looked at T4 and T5 in the FlyWire connectome (the full wiring map of the fly brain), I noticed that they receive input from neighbouring points in space, and those inputs differ in timing.

The inputs I looked for in FlyWire Codex were Mi1, Tm3 (for T4) and Tm1, Tm2 (for T5). The Mi1 was present on the very right side of the fly brain wth a known function of ON delayed input. On the other hand, the Tm1 is associated with OFF delayed input and is present on the left side of the fly brain. 

That suggests a simple trick: compare what a point saw a moment ago with what its neighbour sees now. If the two match, something moved from one point to the other.

## The model: Hassenstein-Reichardt correlator

This idea was first proposed in 1956 by Bernhard Hassenstein and Werner Reichardt, studying beetles. My version has four parts:

1. **Two sensors**, A on the left and B on the right, a small distance apart.
2. **A delay** on each signal. I used a low-pass filter (a filter that smooths a signal and makes it lag behind).
3. **Multiplication.** Delayed A × B is large only when the same pattern hit A first and then B.
4. **Subtraction.** I do the mirror version (delayed B × A) and subtract it.

The result: positive means rightward motion, negative means leftward, and zero means no net direction.

I multiply because a product is only big when both signals are active together. That is the "did the same thing show up at both places, one after the other?" check.

```
  A ──[delay]──×──┐
                  │
  B ──────────────┘  (+)
                         →  output = (delayed A × B) − (delayed B × A)
  B ──[delay]──×──┐
                  │  (−)
  A ──────────────┘
```

## What the app does

The app has two parts.

**1. Tuning curve.** It plots the average detector output against stimulus speed, for a moving striped pattern (a sine-wave grating). Three sliders change the model:

- **Delay:** how long the signal is held back
- **Sensor spacing:** distance between A and B
- **Stripe width:** wavelength of the pattern

**2. Reverse-phi illusion.** A tick box that flips the contrast of the second flash. More on this below.

## What I found

### 1. The response flips with direction
Rightward stripes give a positive output and leftward stripes give a negative one, with the same size. Zero speed gives zero output.

### 2. The peak depends on temporal frequency, not speed alone
When I changed the stripe width, the best speed changed too. What stayed fixed was speed divided by stripe width (temporal frequency, how many stripes pass a point per second). Real flies show this same kind of behaviour, which is a good sign the model captures something real.

For example, with stripe width 1.0 the peak was at about 0.3 on the Y axis, with 2.0 it moved to 0.4 on the Y axis.

### 3. Reverse-phi: the detector can be fooled
Reverse-phi is an illusion where a bright dot appears at one spot and then a *dark* dot appears at a neighbouring spot. You'd expect motion in one direction, but animals report motion in the opposite direction. This has been shown in humans and in flies.

In my model, the output flips sign when I tick the "reverse contrast" box. The reason is simple. The detector only multiplies signals, and bright (+) × dark (−) gives a negative number. It never knew there was an object moving. It only measures whether signals at two places are correlated over time.

The takeaway for me: the fly's motion detector isn't tracking objects. It's computing a correlation, and the illusion is a fingerprint of that.

## Limitations

I want to be upfront about what this is not.

- **It's a simplified model.** Real T4 and T5 cells take in several inputs with different delays and have nonlinearities that I left out.
- **Real reverse-phi responses are not a perfect flip.** In real neurons the reversed response is usually weaker than the normal one. My model gives the exact same size with the opposite sign.
- **I picked the parameters by hand.** The delay, spacing and stripe width are not fitted to real fly data.
- **It's one detector.** A real fly has thousands of them across the eye, plus later stages that combine their output.
- **The reverse-phi test is two simple flashes**, not a full moving stimulus.

Files:

- `app.py`: the model and the Streamlit app
- `requirements.txt`: streamlit, numpy, matplotlib

## What I'd like to do next

- Fit the delay and spacing to published fly data (a light machine learning step).
- Add a more realistic version with separate ON (T4) and OFF (T5) pathways.
- Add a 2D version with four directions.
- Compare against a different motion model, such as the motion energy model.

## What I learned

- How to turn a neural circuit into a few lines of code.
- How to read tuning curves, and why neuroscientists use them.
- How to build and deploy a Streamlit app.
- That a clean illusion can tell you how a system works inside.
- The Reverse phi phenomenon took me a little while to understand. I had to think as a fly and then go back and forth between the fly and the moving object itself.
- At first the slider plot was stuck. I figured out it was because the calculation was above the slider. 

## References

- Borst, A. & Egelhaaf, M. (1989). Principles of visual motion detection.
- Maisak, M. S. et al. (2013). A directional tuning map of Drosophila elementary motion detectors. 
- FlyWire connectome: https://flywire.ai (data viewed through Codex, https://codex.flywire.ai)

## Author

**Fatima Zubair**  
MSc Biophysics, University of Delhi  
Interested in computational neuroscience and neurodegenerative disease  
GitHub: [fatymazubair](https://github.com/fatymazubair) · LinkedIn: [Fatima Zubair](https://www.linkedin.com/in/fatimazubair29)

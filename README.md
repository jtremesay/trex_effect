# T-Rex effect

It's vision is based on movement!

Inspired by this [video](https://www.youtube.com/watch?v=RNhiT-SmR1Q).


## Explanation

This effect is based on the idea that the human eye is more sensitive to changes in light intensity than to constant light. By flipping pixels of a noise pattern using a mask, we can create the illusion of the shape. If you stop the animation, the shape disappears into noise.

![Demo of the T-Rex effect, a static heart shape](demo_heart.webp)

## Implementation

Render using a depth buffer to create a mask of the shapes. Use the depth information as a speed buffer to move noise pixels. Move the pixels in the noise pattern according to the speed buffer, flipping pixels as they move. The result is that pixels in front of the shape move faster, creating a visible shape out of noise.

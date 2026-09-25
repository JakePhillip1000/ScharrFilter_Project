## Scharr Filter project
A Python programming implementation of Scharr filter for edge detection, created using linear algebra matrix transformation applied together with image processing. The scharr filter use for detecting the edge by measuring the pixel intensity.
Here in this project, the image is being known as numerical values wheree each pixel represent the element of the matrix. Then applying the small matrices with the value specified called kernels to the regions of the image.


### The Horizontal matrix detection gradient
 $$
G_x =
\begin{bmatrix}
-3 & 0 & 3 \\
-10 & 0 & 10 \\
-3 & 0 & 3
\end{bmatrix}
$$

 ### The vertical detection gradient
 $$
G_y =
\begin{bmatrix}
-3 & -10 & -3 \\
0 & 0 & 0 \\
3 & 10 & 3
\end{bmatrix}
$$

### The magnitude of the gradient
 $$
G(i,j) =
\sqrt{G_x(i,j)^2 + G_y(i,j)^2}
$$

### We can simplify the magnitude as this...
 $$
G=\sqrt{G_x^2+G_y^2}
$$

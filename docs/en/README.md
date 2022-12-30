Why was the library created?

On one of my job, we had to work with a lot of extremely poor quality data:
* Data type mismatch in documents;
* Data mismatch between related documents;
* Garbage information;

And we've created library named `fuse` that included [fuse-box](https://github.com/uselessvevo/fuse-box/) and [fuse-sheets](https://github.com/uselessvevo/fuse-sheets/), but then was splitted up.

Yes, there are many libraries for **Python** for validation, "cleaning" and loading/unloading data,
but we wanted to make one lite, minimalistic package for all the tasks because of its specificity.

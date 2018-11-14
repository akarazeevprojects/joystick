## Quantum Keypad

[[video demonstration](https://youtu.be/EVqfnaaUThU)]

[![](https://img.youtube.com/vi/EVqfnaaUThU/0.jpg)](https://youtu.be/EVqfnaaUThU)

All the code can be found in [quantum_keypad/](quantum_keypad/) folder.

Here I used [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/).

| Front side | Back side     |
| :------------- | :------------- |
| <img src="img/img3.jpg" height="500px">       | <img src="img/img4.JPG" height="500px">       |

| Bell State | Result of two Hadamard gates     |
| :------------- | :------------- |
| <img src="img/img5.jpg" width="500px">       | <img src="img/img6.jpg" width="500px">       |

## Joystick

| [[video demonstration 1](https://youtu.be/bS0-Sjmxa1g)] | [[video demonstration 2](https://youtu.be/AWBQyz4jdUo)]     |
| :------------- | :------------- |
| [![](https://img.youtube.com/vi/bS0-Sjmxa1g/0.jpg)](https://youtu.be/bS0-Sjmxa1g)       | [![](https://img.youtube.com/vi/AWBQyz4jdUo/0.jpg)](https://youtu.be/AWBQyz4jdUo)       |

All the code can be found in [mouse_controller/](mouse_controller/) folder.

`Server` was launched on MacBook and `client` was launched on [Raspberry Pi 2 Model B](https://www.raspberrypi.org/products/raspberry-pi-2-model-b/).

Raspberry Pi was used as a controller with joystick and water sensor (it simulates the pressing of Space bar).

| Action | Inside the box     |
| :------------- | :------------- |
| <img src="img/img1.jpg" width="500px">       | <img src="img/img2.jpg" width="500px">       |

## Additional software

| Name | Description     |
| :------------- | :------------- |
| [Etcher](https://etcher.io)       | Burn [Raspbian images](https://www.raspberrypi.org/downloads/raspbian/) to Raspberry Pi      |
| [slither.io](http://slither.io)  | Used this game to test my Joystick made with water sensor  |
| [autopy](https://github.com/msanders/autopy/)  | Used for controlling the mouse on my MacBook from Python script. Supports only Python 2 |
| [evdev](https://github.com/gvalkov/python-evdev)  | Python package helped me a lot to read inputs from keypad and turn it into Quantum Keypad. [Here](http://python-evdev.readthedocs.io/en/latest/tutorial.html) one can find awesome tutorial on how to use the evdev  |
| [QISKit](https://www.qiskit.org)   | Quantum simulator to evaluate quantum circuits  |
| [ModelQ](https://www.qiskit.org/modelq/)   | Inspiration  |

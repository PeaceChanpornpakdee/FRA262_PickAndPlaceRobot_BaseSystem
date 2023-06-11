# Base System
The base system with user interface for FRA262 (Robotics Studio III) pick & place robot project. 

$~$

## Installation
### Font

Please install `Inter-SemiBold.ttf` from `font` folder.

### TK (Ubuntu only)
```
sudo apt-get install python3-tk
```
### Pillow
Windows/MacOS
```
pip install Pillow
```
Ubuntu
```
sudo apt-get install python3-pil python3-pil.imagetk
```
### Pyserial
```
pip install pyserial
```
### Pymodbus
```
pip install pymodbus==3.1.3
```

$~$

## Configuration
You might need to change COM port in `protocol.py`.
> The original COM port is `self.port = "COM5"`
 
View port on linux: `sudo dmesg | grep tty`

$~$

## Running
The most basic way to run base system is to run `app.py` on Visual Studio Code.

$~$

## Protocol
### Register Address

| Address  | Meaning | Operation |
| -------- | ------- | --------- |
| 0x00 | Heartbeat Protocol | Read/Write
| 0x01 | Base System Status | Write
| 0x02 | End Effector Status | Read/Write
| 0x10 | y-axis Moving Status | Read
| 0x11 | y-axis Actual Position | Read
| 0x12 | y-axis Actual Speed | Read
| 0x13 | y-axis Actual Acceleration | Read
| 0x20 | Pick Tray Origin x | Read
| 0x21 | Pick Tray Origin y | Read
| 0x22 | Pick Tray Orientation  | Read
| 0x23 | Place Tray Origin x | Read
| 0x24 | Place Tray Origin y | Read
| 0x25 | Place Tray Orientation  | Read
| 0x30 | Goal Point x | Write
| 0x31 | Goal Point y | Write
| 0x40 | x-axis Moving Status | Read/Write
| 0x41 | x-axis Target Position | Read
| 0x42 | x-axis Target Speed | Read
| 0x43 | x-axis Target Acceleration Time | Read
| 0x44 | x-axis Actual Position | Write
| 0x45 | x-axis Actual Speed | Write

$~$

### Bit Position
![alt text](https://github.com/PeaceChanpornpakdee/FRA262_PickAndPlaceRobot_BaseSystem/blob/dev/image/readme_image/bit_position.png?raw=true)

$~$

### Data Format
**1. Base System Status**
| Bit  | Meaning |
| ---- | ------- |
| 0 | Set Pick Tray | 
| 1 | Set Place Tray | 
| 2 | Home |
| 3 | Run Tray Mode |
| 4 | Run Point Mode |

$~$

**2. End Effector Status**
| Bit  | Meaning |
| ---- | ------- |
| 0 | Laser On/Off | 
| 1 | Gripper Power | 
| 2 | Gripper Picking |
| 3 | Gripper Placing |

$~$

**3. y-axis Moving Status**
| Bit  | Meaning |
| ---- | ------- |
| 0 | Jog Pick | 
| 1 | Jog Place | 
| 2 | Home |
| 3 | Go Pick |
| 4 | Go Place |
| 5 | Go Point |

$~$

**4. Position / Speed / Acceleration**

```Value * 10```

*Ex. 123.4 mm --> 1234*
> **_Maximum speed for x-axis is 300 mm/s_**

$~$

**5. Orientation**

Orientation cannot be nagative and must be less than 360 degree. 

```Value * 100```

*Ex. 180.45 degree --> 18045*

$~$

**6. x-axis Moving Status**
| Bit  | Meaning |
| ---- | ------- |
| 0 | Home | 
| 1 | Run | 
| 2 | Jog Left (-) | 
| 3 | Jog Right (+) | 

$~$

**7. x-axis Target Acceleration Time**
- ```1``` = 100 ms
- ```2``` = 500 ms
- ```3``` = 1000 ms

$~$

### Protocol Flow
**1. Heartbeat**
![alt text](https://github.com/PeaceChanpornpakdee/FRA262_PickAndPlaceRobot_BaseSystem/blob/dev/image/readme_image/heartbeat.png?raw=true)

**2. Routine**
![alt text](https://github.com/PeaceChanpornpakdee/FRA262_PickAndPlaceRobot_BaseSystem/blob/dev/image/readme_image/routine.png?raw=true)

**3. Laser On/Off**
![alt text](https://github.com/PeaceChanpornpakdee/FRA262_PickAndPlaceRobot_BaseSystem/blob/dev/image/readme_image/laser.png?raw=true)

**4. Gripper Power**
![alt text](https://github.com/PeaceChanpornpakdee/FRA262_PickAndPlaceRobot_BaseSystem/blob/dev/image/readme_image/gripper_power.png?raw=true)

**5. Gripper Pick**
![alt text](https://github.com/PeaceChanpornpakdee/FRA262_PickAndPlaceRobot_BaseSystem/blob/dev/image/readme_image/gripper_pick.png?raw=true)

**6. Gripper Place**
![alt text](https://github.com/PeaceChanpornpakdee/FRA262_PickAndPlaceRobot_BaseSystem/blob/dev/image/readme_image/gripper_place.png?raw=true)

**7. Set Pick Tray**
![alt text](https://github.com/PeaceChanpornpakdee/FRA262_PickAndPlaceRobot_BaseSystem/blob/dev/image/readme_image/set_pick_tray.png?raw=true)

**8. Set Place Tray**
![alt text](https://github.com/PeaceChanpornpakdee/FRA262_PickAndPlaceRobot_BaseSystem/blob/dev/image/readme_image/set_place_tray.png?raw=true)

**9. Set Goal Point**
![alt text](https://github.com/PeaceChanpornpakdee/FRA262_PickAndPlaceRobot_BaseSystem/blob/dev/image/readme_image/set_goal_point.png?raw=true)

**10. Home**
![alt text](https://github.com/PeaceChanpornpakdee/FRA262_PickAndPlaceRobot_BaseSystem/blob/dev/image/readme_image/home.png?raw=true)

**11. Run Tray Mode**
![alt text](https://github.com/PeaceChanpornpakdee/FRA262_PickAndPlaceRobot_BaseSystem/blob/dev/image/readme_image/run_tray.png?raw=true)

**12. Run Point Mode**
![alt text](https://github.com/PeaceChanpornpakdee/FRA262_PickAndPlaceRobot_BaseSystem/blob/dev/image/readme_image/run_point.png?raw=true)

**13. Home x-axis**
![alt text](https://github.com/PeaceChanpornpakdee/FRA262_PickAndPlaceRobot_BaseSystem/blob/dev/image/readme_image/home_x.png?raw=true)

**14. Run x-axis**
![alt text](https://github.com/PeaceChanpornpakdee/FRA262_PickAndPlaceRobot_BaseSystem/blob/dev/image/readme_image/run_x.png?raw=true)

**15. Jog x-axis**
![alt text](https://github.com/PeaceChanpornpakdee/FRA262_PickAndPlaceRobot_BaseSystem/blob/dev/image/readme_image/jog_x.png?raw=true)

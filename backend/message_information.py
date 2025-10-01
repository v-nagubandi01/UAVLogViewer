AHR2 = """
Table Description: Backup AHRS data. 

Fields:
    TimeUS: Time since system startup (μs).
    Roll: Estimated roll (deg). 
    Pitch: Estimated pitch (deg). 
    Yaw: Estimated yaw (degheading). 
    Alt: Estimated altitude (m). 
    Lat: Estimated latitude (deglatitude). 
    Lng: Estimated longitude (deglongitude). 
    Q1: Estimated attitude quaternion component 1. 
    Q2: Estimated attitude quaternion component 2. 
    Q3: Estimated attitude quaternion component 3. 
    Q4: Estimated attitude quaternion component 4. 

Extra Information:
Think of this as the drone's backup "inner ear" or sense of balance. The primary system (see XKF1) is constantly figuring out the drone's orientation (roll, pitch, yaw) and location. The AHR2 message logs the data from a secondary, simpler system that runs alongside it. If the primary system has a problem, the drone can use this backup data to stay stable. It's a crucial safety feature for redundancy.
"""

ATT = """
Table Description: Canonical vehicle attitude. 

Fields:
    TimeUS: Time since system startup (μs). 
    DesRoll: vehicle desired roll (deg). 
    Roll: achieved vehicle roll (deg). 
    DesPitch: vehicle desired pitch (deg). 
    Pitch: achieved vehicle pitch (deg). 
    DesYaw: vehicle desired yaw (degheading). 
    Yaw: achieved vehicle yaw (degheading). 
    AEKF: active EKF type. 

Extra Information:
This is one of the most important messages for analyzing flight performance. It directly compares what the pilot or autopilot *wanted* the drone to do (Desired Roll/Pitch/Yaw) with what it *actually* did (achieved Roll/Pitch/Yaw). A large gap between the two indicates poor tuning or a physical problem, meaning the drone is not responding to commands as expected.
"""

AUXF = """
Table Description: Auxiliary function invocation information. 

Fields:
    TimeUS: Time since system startup (μs). 
    function: ID of triggered function (instance). 
    pos: switch position when function triggered (enum). 
    source: source of auxiliary function invocation (enum). 
    index: index within source. 0 indexed.  Invalid for scripting. 
    result: true if function was successful. 

Enums for 'function' field:
    DO_NOTHING (0): aux switch disabled. 
    FLIP (2): flip. 
    SIMPLE_MODE (3): change to simple mode. 
    RTL (4): change to RTL flight mode. 
    SAVE_TRIM (5): save current position as level. 
    SAVE_WP (7): save mission waypoint or RTL if in auto mode. 
    CAMERA_TRIGGER (9): trigger camera servo or relay. 
    RANGEFINDER (10): allow enabling or disabling rangefinder in flight which helps avoid surface tracking when you are far above the ground. 
    FENCE (11): allow enabling or disabling fence in flight. 
    RESETTOARMEDYAW (12): UNUSED. 
    SUPERSIMPLE_MODE (13): change to simple mode in middle, super simple at top. 
    ACRO_TRAINER (14): low = disabled, middle = leveled, high = leveled and limited. 
    SPRAYER (15): enable/disable the crop sprayer. 
    AUTO (16): change to auto flight mode. 
    AUTOTUNE_MODE (17): auto tune. 
    LAND (18): change to LAND flight mode. 
    GRIPPER (19): Operate cargo grippers low=off, middle=neutral, high=on. 
    PARACHUTE_ENABLE (21): Parachute enable/disable. 
    PARACHUTE_RELEASE (22): Parachute release. 
    PARACHUTE_3POS (23): Parachute disable, enable, release with 3 position switch. 
    MISSION_RESET (24): Reset auto mission to start from first command. 
    ATTCON_FEEDFWD (25): enable/disable the roll and pitch rate feed forward. 
    ATTCON_ACCEL_LIM (26): enable/disable the roll, pitch and yaw accel limiting. 
    RETRACT_MOUNT1 (27): Retract Mount1. 
    RELAY (28): Relay pin on/off (only supports first relay). 
    LANDING_GEAR (29): Landing gear controller. 
    LOST_VEHICLE_SOUND (30): Play lost vehicle sound. 
    MOTOR_ESTOP (31): Emergency Stop Switch. 
    MOTOR_INTERLOCK (32): Motor On/Off switch. 
    BRAKE (33): Brake flight mode. 
    RELAY2 (34): Relay2 pin on/off. 
    RELAY3 (35): Relay3 pin on/off. 
    RELAY4 (36): Relay4 pin on/off. 
    THROW (37): change to THROW flight mode. 
    AVOID_ADSB (38): enable AP_Avoidance library. 
    PRECISION_LOITER (39): enable precision loiter. 
    AVOID_PROXIMITY (40): enable object avoidance using proximity sensors (ie. horizontal lidar). 
    ARMDISARM_UNUSED (41): UNUSED. 
    SMART_RTL (42): change to SmartRTL flight mode. 
    INVERTED (43): enable inverted flight. 
    WINCH_ENABLE (44): winch enable/disable. 
    WINCH_CONTROL (45): winch control. 
    RC_OVERRIDE_ENABLE (46): enable RC Override. 
    USER_FUNC1 (47): user function #1. 
    USER_FUNC2 (48): user function #2. 
    USER_FUNC3 (49): user function #3. 
    LEARN_CRUISE (50): learn cruise throttle (Rover). 
    MANUAL (51): manual mode. 
    ACRO (52): acro mode. 
    STEERING (53): steering mode. 
    HOLD (54): hold mode. 
    GUIDED (55): guided mode. 
    LOITER (56): loiter mode. 
    FOLLOW (57): follow mode. 
    CLEAR_WP (58): clear waypoints. 
    SIMPLE (59): simple mode. 
    ZIGZAG (60): zigzag mode. 
    ZIGZAG_SaveWP (61): zigzag save waypoint. 
    COMPASS_LEARN (62): learn compass offsets. 
    SAILBOAT_TACK (63): rover sailboat tack. 
    REVERSE_THROTTLE (64): reverse throttle input. 
    GPS_DISABLE (65): disable GPS for testing. 
    RELAY5 (66): Relay5 pin on/off. 
    RELAY6 (67): Relay6 pin on/off. 
    STABILIZE (68): stabilize mode. 
    POSHOLD (69): poshold mode. 
    ALTHOLD (70): althold mode. 
    FLOWHOLD (71): flowhold mode. 
    CIRCLE (72): circle mode. 
    DRIFT (73): drift mode. 
    SAILBOAT_MOTOR_3POS (74): Sailboat motoring 3pos. 
    SURFACE_TRACKING (75): Surface tracking upwards or downwards. 
    STANDBY (76): Standby mode. 
    TAKEOFF (77): takeoff. 
    RUNCAM_CONTROL (78): control RunCam device. 
    RUNCAM_OSD_CONTROL (79): control RunCam OSD. 
    VISODOM_ALIGN (80): align visual odometry camera’s attitude to AHRS. 
    DISARM (81): disarm vehicle. 
    Q_ASSIST (82): disable, enable and force Q assist. 
    ZIGZAG_Auto (83): zigzag auto switch. 
    AIRMODE (84): enable / disable airmode for copter. 
    GENERATOR (85): generator control. 
    TER_DISABLE (86): disable terrain following in CRUISE/FBWB modes. 
    CROW_SELECT (87): select CROW mode for diff spoilers;high disables,mid forces progressive. 
    SOARING (88): three-position switch to set soaring mode. 
    LANDING_FLARE (89): force flare, throttle forced idle, pitch to LAND_PITCH_DEG, tilts up. 
    EKF_SOURCE_SET (90): change EKF data source set between primary, secondary and tertiary. 
    ARSPD_CALIBRATE (91): calibrate airspeed ratio. 
    FBWA (92): Fly-By-Wire-A. 
    RELOCATE_MISSION (93): used in separate branch MISSION_RELATIVE. 
    VTX_POWER (94): VTX power level. 
    FBWA_TAILDRAGGER (95): enables FBWA taildragger takeoff mode.  Once this feature is enabled it will stay enabled until the aircraft goes above TKOFF_TDRAG_SPD1 airspeed, changes mode, or the pitch goes above the initial pitch when this is engaged or goes below 0 pitch.  When enabled the elevator will be forced to TKOFF_TDRAG_ELEV. This option allows for easier takeoffs on taildraggers in FBWA mode, and also makes it easier to test auto-takeoff steering handling in FBWA. 
    MODE_SWITCH_RESET (96): trigger re-reading of mode switch. 
    WIND_VANE_DIR_OFSSET (97): flag for windvane direction offset input, used with windvane type 2. 
    TRAINING (98): mode training. 
    AUTO_RTL (99): AUTO RTL via DO_LAND_START. 
    KILL_IMU1 (100): disable first IMU (for IMU failure testing). 
    KILL_IMU2 (101): disable second IMU (for IMU failure testing). 
    CAM_MODE_TOGGLE (102): Momentary switch to cycle camera modes. 
    EKF_LANE_SWITCH (103): trigger lane switch attempt. 
    EKF_YAW_RESET (104): trigger yaw reset attempt. 
    GPS_DISABLE_YAW (105): disable GPS yaw for testing. 
    DISABLE_AIRSPEED_USE (106): equivalent to AIRSPEED_USE 0. 
    FW_AUTOTUNE (107): fixed wing auto tune. 
    QRTL (108): QRTL mode. 
    CUSTOM_CONTROLLER (109): use Custom Controller. 
    KILL_IMU3 (110): disable third IMU (for IMU failure testing). 
    LOWEHEISER_STARTER (111): allows for manually running starter. 
    AHRS_TYPE (112): change AHRS_EKF_TYPE. 
    RETRACT_MOUNT2 (113): Retract Mount2. 
    CRUISE (150): CRUISE mode. 
    TURTLE (151): Turtle mode - flip over after crash. 
    SIMPLE_HEADING_RESET (152): reset simple mode reference heading to current. 
    ARMDISARM (153): arm or disarm vehicle. 
    ARMDISARM_AIRMODE (154): arm or disarm vehicle enabling airmode. 
    TRIM_TO_CURRENT_SERVO_RC (155): trim to current servo and RC. 
    TORQEEDO_CLEAR_ERR (156): clear torqeedo error. 
    EMERGENCY_LANDING_EN (157): Force long FS action to FBWA for landing out of range. 
    OPTFLOW_CAL (158): optical flow calibration. 
    FORCEFLYING (159): enable or disable land detection for GPS based manual modes preventing land detection and maintainting set_throttle_mix_max. 
    WEATHER_VANE_ENABLE (160): enable/disable weathervaning. 
    TURBINE_START (161): initialize turbine start sequence. 
    FFT_NOTCH_TUNE (162): FFT notch tuning function. 
    MOUNT_LOCK (163): Mount yaw lock vs follow. 
    LOG_PAUSE (164): Pauses logging if under logging rate control. 
    ARM_EMERGENCY_STOP (165): ARM on high, MOTOR_ESTOP on low. 
    CAMERA_REC_VIDEO (166): start recording on high, stop recording on low. 
    CAMERA_ZOOM (167): camera zoom high = zoom in, middle = hold, low = zoom out. 
    CAMERA_MANUAL_FOCUS (168): camera manual focus.  high = long shot, middle = stop focus, low = close shot. 
    CAMERA_AUTO_FOCUS (169): camera auto focus. 
    QSTABILIZE (170): QuadPlane QStabilize mode. 
    MAG_CAL (171): Calibrate compasses (disarmed only). 
    BATTERY_MPPT_ENABLE (172): Battery MPPT Power enable.  high = ON, mid = auto (controlled by mppt/batt driver), low = OFF. This effects all MPPTs. 
    PLANE_AUTO_LANDING_ABORT (173): Abort Glide-slope or VTOL landing during payload place or do_land type mission items. 
    CAMERA_IMAGE_TRACKING (174): camera image tracking. 
    CAMERA_LENS (175): camera lens selection. 
    VFWD_THR_OVERRIDE (176): force enabled VTOL forward throttle method. 
    MOUNT_LRF_ENABLE (177): mount LRF enable/disable. 
    FLIGHTMODE_PAUSE (178): e.g. pause movement towards waypoint. 
    ICE_START_STOP (179): AP_ICEngine start stop. 
    AUTOTUNE_TEST_GAINS (180): auto tune tuning switch to test or revert gains. 
    QUICKTUNE (181): quicktune 3 position switch. 
    AHRS_AUTO_TRIM (182): in-flight AHRS autotrim. 
    AUTOLAND (183): Fixed Wing AUTOLAND Mode. 
    SYSTEMID (184): system ID as an aux switch. 
    ROLL (201): roll input. 
    PITCH (202): pitch input. 
    THROTTLE (203): throttle pilot input. 
    YAW (204): yaw pilot input. 
    MAINSAIL (207): mainsail input. 
    FLAP (208): flap input. 
    FWD_THR (209): VTOL manual forward throttle. 
    AIRBRAKE (210): manual airbrake control. 
    WALKING_HEIGHT (211): walking robot height input. 
    MOUNT1_ROLL (212): mount1 roll input. 
    MOUNT1_PITCH (213): mount1 pitch input. 
    MOUNT1_YAW (214): mount1 yaw input. 
    MOUNT2_ROLL (215): mount2 roll input. 
    MOUNT2_PITCH (216): mount3 pitch input. 
    MOUNT2_YAW (217): mount4 yaw input. 
    LOWEHEISER_THROTTLE (218): allows for throttle on slider. 
    TRANSMITTER_TUNING (219): use a transmitter knob or slider for in-flight tuning. 
    TRANSMITTER_TUNING2 (220): use another transmitter knob or slider for in-flight tuning. 
    SCRIPTING_1 (300). 
    SCRIPTING_2 (301). 
    SCRIPTING_3 (302). 
    SCRIPTING_4 (303). 
    SCRIPTING_5 (304). 
    SCRIPTING_6 (305). 
    SCRIPTING_7 (306). 
    SCRIPTING_8 (307). 
    SCRIPTING_9 (308). 
    SCRIPTING_10 (309). 
    SCRIPTING_11 (310). 
    SCRIPTING_12 (311). 
    SCRIPTING_13 (312). 
    SCRIPTING_14 (313). 
    SCRIPTING_15 (314). 
    SCRIPTING_16 (315). 
    STOP_RESTART_SCRIPTING (316): emergency scripting disablement. 
    AUX_FUNCTION_MAX (317). 

Enums for 'pos' field:
    LOW (0): indicates auxiliary switch is in the low position (pwm <1200). 
    MIDDLE (1): indicates auxiliary switch is in the middle position (pwm >1200, <1800). 
    HIGH (2): indicates auxiliary switch is in the high position (pwm >1800). 

Enums for 'source' field:
    INIT (0): Source index is RC channel index. 
    RC (1): Source index is RC channel index. 
    BUTTON (2): Source index is button index. 
    MAVLINK (3): Source index is MAVLink channel number. 
    MISSION (4): Source index is mission item index. 
    SCRIPTING (5): Source index is not used (always 0). 

Extra Information:
This log entry is like a record of every time a special function was activated using a switch on the remote control. Think of it as logging when the pilot flips a switch to engage "Return to Home," "Land," "Take a picture," or deploy landing gear. It's useful for understanding what commands were given during a flight and confirming if the drone successfully executed them. The `result` field is useful for this.
"""

BARO = """
Table Description: Gathered Barometer data. 

Fields:
    TimeUS: Time since system startup (μs). 
    I: barometer sensor instance number (instance). 
    Alt: calculated altitude (m). 
    AltAMSL: altitude AMSL (m). 
    Press: measured atmospheric pressure (Pa). 
    Temp: measured atmospheric temperature (degC). 
    CRt: derived climb rate from primary barometer (m/s). 
    SMS: time last sample was taken (ms). 
    Offset: raw adjustment of barometer altitude, zeroed on calibration, possibly set by GCS (m). 
    GndTemp: temperature on ground, specified by parameter or measured while on ground (degC). 
    H: true if barometer is considered healthy. 
    CPress: compensated atmospheric pressure (Pa). 

Extra Information:
This is the drone's altimeter. The barometer sensor measures air pressure. Since air pressure decreases predictably as you go higher, the drone can use this measurement to calculate its altitude. This data is crucial for tasks like holding a steady height ("Altitude Hold"), automated landing, and following terrain. It's often more reliable for short-term altitude changes than GPS.
"""

BAT = """
Table Description: Gathered battery data. 

Fields:
    TimeUS: Time since system startup (μs). 
    Inst: battery instance number (instance). 
    Volt: measured voltage (V). 
    VoltR: estimated resting voltage (V). 
    Curr: measured current (A). 
    CurrTot: consumed Ah, current * time (mAh). 
    EnrgTot: consumed Wh, energy this battery has expended (W.h). 
    Temp: measured temperature (degC). 
    Res: estimated battery resistance (Ohm). 
    RemPct: remaining percentage (%). 
    H: health. 
    SH: state of health percentage. 0 if unknown (%). 

Extra Information: 
This is the drone's "fuel gauge." It provides critical information about the battery's voltage, the amount of current being drawn by the motors, and the total energy consumed. This data is essential for monitoring the health of the battery and diagnosing power issues. A sudden voltage drop under high current (a "voltage sag") can indicate a weak battery and is a common cause of crashes. It tracks the voltage, how much power is being drawn (current), the temperature, and the estimated percentage remaining. This is one of the most important messages to monitor, as it helps the pilot know when to land before the battery runs out, preventing a crash.
"""

CMD = """
Table Description: Uploaded mission command information. 

Fields:
    TimeUS: Time since system startup (μs). 
    CTot: Total number of mission commands. 
    CNum: This command’s offset in mission. 
    CId: Command type. 
    Prm1: Parameter 1. 
    Prm2: Parameter 2. 
    Prm3: Parameter 3. 
    Prm4: Parameter 4. 
    Lat: Command latitude (deglatitude). 
    Lng: Command longitude (deglongitude). 
    Alt: Command altitude (m). 
    Frame: Frame used for position. 

This message logs each step of a pre-planned autonomous mission. It's like looking at the drone's to-do list. When the drone reaches a waypoint or performs an action like "take a picture," a CMD message is logged. This is invaluable for debugging autonomous flights to see if the drone was executing the mission as planned.
"""

CTUN = """
Table Description: Control Tuning information. 

Fields:
    TimeUS: Time since system startup (μs). 
    NavRoll: desired roll (deg). 
    Roll: achieved roll (deg). 
    NavPitch: desired pitch assuming pitch trims are already applied (deg). 
    Pitch: achieved pitch assuming pitch trims are already applied,ie “0deg” is level flight trimmed pitch attitude as shown on artificial horizon level line. (deg). [cite: 101, 102]
    ThO: scaled output throttle. 
    RdO: scaled output rudder. 
    ThD: demanded speed-height-controller throttle. 
    As: airspeed estimate (or measurement if airspeed sensor healthy and ARSPD_USE>0) (m/s). 
    AsT: airspeed type ( old estimate or source of new estimate) (enum). 
    SAs: DCM’s airspeed estimate, NaN if not available (m/s). 
    E2T: equivalent to true airspeed ratio. 
    GU: groundspeed undershoot when flying with minimum groundspeed (cm/s). 

Enums for 'AsT' field:
    NO_NEW_ESTIMATE (0). 
    AIRSPEED_SENSOR (1). 
    DCM_SYNTHETIC (2). 
    EKF3_SYNTHETIC (3). 
    SIM (4). 

Extra Information:
This message gives a detailed look into the drone's navigation and throttle control. It's more specific than the 'ATT' message, showing how the navigation controller is trying to steer the drone (NavRoll, NavPitch) and how the throttle is being managed. This is used by developers and advanced users to fine-tune the drone's performance in guided modes like 'Auto' or 'Loiter'. This data is essential for engineers to "tune" the drone's software (its PID settings) to make it fly more smoothly, responsively, and accurately, especially in windy conditions.
"""

DSF = """
Table Description: Onboard logging statistics. 

Fields:
    TimeUS: Time since system startup (μs). 
    Dp: Number of times we rejected a write to the backend. 
    Blk: Current block number. 
    Bytes: Current write offset (B). 
    FMn: Minimum free space in write buffer in last time period. 
    FMx: Maximum free space in write buffer in last time period. 
    FAv: Average free space in write buffer in last time period. 

Extra Information:
This is a health-check message for the drone's "black box" logging system itself. It tells you if the memory card is keeping up with the amount of data being written. If you see a high number of 'Dp' (dropped messages), it means your log file is incomplete because the system was overloaded. This isn't for flight analysis, but for diagnosing problems with the logging hardware.    
"""

ERR = """
Table Description: Specifically coded error messages. 

Fields:
    TimeUS: Time since system startup (μs). 
    Subsys: Subsystem in which the error occurred (enum). 
    ECode: Subsystem-specific error code. 

Enums for 'Subsys' field:
    MAIN (1). 
    RADIO (2). 
    COMPASS (3). 
    OPTFLOW (4): not used. 
    FAILSAFE_RADIO (5). 
    FAILSAFE_BATT (6). 
    FAILSAFE_GPS (7): not used. 
    FAILSAFE_GCS (8). 
    FAILSAFE_FENCE (9). 
    FLIGHT_MODE (10). 
    GPS (11). 
    CRASH_CHECK (12). 
    FLIP (13). 
    AUTOTUNE (14): not used. 
    PARACHUTES (15). 
    EKFCHECK (16). 
    FAILSAFE_EKFINAV (17). 
    BARO (18). 
    CPU (19). 
    FAILSAFE_ADSB (20). 
    TERRAIN (21). 
    NAVIGATION (22). 
    FAILSAFE_TERRAIN (23). 
    EKF_PRIMARY (24). 
    THRUST_LOSS_CHECK (25). 
    FAILSAFE_SENSORS (26). 
    FAILSAFE_LEAK (27). 
    PILOT_INPUT (28). 
    FAILSAFE_VIBE (29). 
    INTERNAL_ERROR (30). 
    FAILSAFE_DEADRECKON (31). 

Extra Information:
This is the drone's error log. When something goes wrong, the system generates an ERR message to record the problem. It identifies which part of the drone had the issue (the Subsys, like GPS, Compass, or Failsafe system) and a specific code (ECode) to describe the exact error. This is often the first place to look when a flight goes wrong to diagnose what happened.
"""

FILE = """
Table Description: File data. 

Fields:
    FileName: File name (char 16). 
    Offset: Offset into the file of this block. 
    Length: Length of this data block. 
    Data: File data of this block (char 64). 

Extra Information:
This message type is used for transferring files to or from the drone's flight controller, typically over the MAVLink telemetry link. For example, it could be used to download a different log file or upload a terrain map. It's not related to the flight performance itself but is part of the drone's data management capabilities.    
"""

FMT = """
Table Description: Message defining the format of messages in this file. 

Fields:
    Type: unique-to-this-log identifier for message being defined. 
    Length: the number of bytes taken up by this message (including all headers) (B). 
    Name: name of the message being defined (char 4). 
    Format: character string defining the C-storage-type of the fields in this message (char 16). 
    Columns: the labels of the message being defined (char 64). 

Extra Information:
This is a critical "header" message that appears at the beginning of every log file. It acts as a dictionary, defining the structure of every other message type in the log (like 'ATT', 'GPS', etc.). Log analysis software reads these FMT messages first to understand how to interpret the rest of the data file. A user would almost never look at this directly.
"""

FMTU = """
Table Description: Message defining units and multipliers used for fields of other messages. 

Fields:
    TimeUS: Time since system startup (μs). 
    FmtType: numeric reference to associated FMT message. 
    UnitIds: each character refers to a UNIT message.  The unit at an offset corresponds to the field at the same offset in FMT.Format (char 16). 
    MultIds: each character refers to a MULT message. The multiplier at an offset corresponds to the field at the same offset in FMT.Format (char 16). 

Extra Information:
Working alongside the 'FMT', 'UNIT', and 'MULT' messages, this message helps make the log file self-describing. It links the data fields defined in 'FMT' to their correct units (e.g., meters/second, degrees) and any necessary multipliers. Like 'FMT', this is part of the log's internal structure and is read by software, not by a human analyst.
"""

FTN = """
Table Description: Filter Tuning Message - per motor. 

Fields:
    TimeUS: microseconds since system startup (μs). 
    I: instance (instance). 
    NDn: number of active harmonic notches. 
    NF1: desired harmonic notch centre frequency for motor 1 (Hz). 
    NF2: desired harmonic notch centre frequency for motor 2 (Hz). 
    NF3: desired harmonic notch centre frequency for motor 3 (Hz). 
    NF4: desired harmonic notch centre frequency for motor 4 (Hz). 
    NF5: desired harmonic notch centre frequency for motor 5 (Hz). 
    NF6: desired harmonic notch centre frequency for motor 6 (Hz). 
    NF7: desired harmonic notch centre frequency for motor 7 (Hz). 
    NF8: desired harmonic notch centre frequency for motor 8 (Hz). 
    NF9: desired harmonic notch centre frequency for motor 9 (Hz). 
    NF10: desired harmonic notch centre frequency for motor 10 (Hz). 
    NF11: desired harmonic notch centre frequency for motor 11 (Hz). 
    NF12: desired harmonic notch centre frequency for motor 12 (Hz). 

Extra Information:
This message is for advanced vibration analysis and suppression. It shows the specific noise frequencies associated with each motor that the autopilot is trying to filter out. This is useful for confirming that the dynamic notch filters are correctly tracking motor RPM to eliminate vibration that could otherwise harm sensor performance.
"""

FTN1 = """
Table Description: FFT Filter Tuning. 

Fields:
    TimeUS: microseconds since system startup (μs). 
    PkAvg: peak noise frequency as an energy-weighted average of roll and pitch peak frequencies (Hz). 
    BwAvg: bandwidth of weighted peak frequency where edges are determined by FFT_ATT_REF (Hz). 
    SnX: signal-to-noise ratio on the roll axis. 
    SnY: signal-to-noise ratio on the pitch axis. 
    SnZ: signal-to-noise ratio on the yaw axis. 
    FtX: harmonic fit on roll of the highest noise peak to the second highest noise peak (%). 
    FtY: harmonic fit on pitch of the highest noise peak to the second highest noise peak (%). 
    FtZ: harmonic fit on yaw of the highest noise peak to the second highest noise peak (%). 
    FHX: FFT health, X-axis. 
    FHY: FFT health, Y-axis. 
    FHZ: FFT health, Z-axis. 
    Tc: FFT cycle time (μs). 

Extra Information:
This message gives an overview of the drone's vibration management system. The autopilot uses a technique called FFT (Fast Fourier Transform) to "listen" to the vibrations from the motors and propellers. This log shows the primary noise frequency it has detected and how strong that noise is compared to the actual flight signals (the Signal-to-Noise ratio). It's a key indicator of overall vibration levels.
"""

FTN2 = """
Table Description: FFT Noise Frequency Peak. 

Fields:
    TimeUS: microseconds since system startup (μs). 
    Id: peak id where 0 is the centre peak, 1 is the lower shoulder and 2 is the upper shoulder (instance). 
    PkX: noise frequency of the peak on roll (Hz). 
    PkY: noise frequency of the peak on pitch (Hz). 
    PkZ: noise frequency of the peak on yaw (Hz). 
    BwX: bandwidth of the peak frequency on roll where edges are determined by FFT_ATT_REF (Hz). 
    BwY: bandwidth of the peak frequency on pitch where edges are determined by FFT_ATT_REF (Hz). 
    BwZ: bandwidth of the peak frequency on yaw where edges are determined by FFT_ATT_REF (Hz). 
    SnX: signal-to-noise ratio on the roll axis. 
    SnY: signal-to-noise ratio on the pitch axis. 
    SnZ: signal-to-noise ratio on the yaw axis. 
    EnX: power spectral density bin energy of the peak on roll. 
    EnY: power spectral density bin energy of the peak on roll. 
    EnZ: power spectral density bin energy of the peak on roll. 

Extra Information:
This message provides a deeper dive into the vibration data summarized in FTN1. It pinpoints the exact frequencies where vibration is the strongest for each axis (roll, pitch, yaw). This is extremely useful for diagnosing the source of a vibration problem. For example, a peak at a specific frequency might correspond to the RPM of an unbalanced propeller.
"""

GPA = """
Table Description: GPS accuracy information. 

Fields:
    I: GPS instance number (μs). 
    TimeUS: Time since system startup (instance). 
    VDop: vertical dilution of precision. 
    HAcc: horizontal position accuracy (m). 
    VAcc: vertical position accuracy (m). 
    SAcc: speed accuracy (m/s). 
    YAcc: yaw accuracy (deg). 
    VV: true if vertical velocity is available. 
    SMS: time since system startup this sample was taken (ms). 
    Delta: system time delta between the last two reported positions (ms). 
    AEl: altitude above WGS-84 ellipsoid; INT32_MIN (-2147483648) if unknown (m). [cite: 170, 171]
    RTCMFU: RTCM fragments used. 
    RTCMFD: RTCM fragments discarded. 

Extra Information:
While the 'GPS' message tells you *where* the drone is, this 'GPA' message tells you how *confident* the GPS receiver is about that position. The 'HAcc' and 'VAcc' fields show the estimated position error in meters. Lower numbers are better. If these values are high, it means the GPS signal is poor, and the drone's ability to hold a position or navigate accurately will be degraded.
"""

GPS = """
GPS Table Description 

Fields:
    TimeUS: Time since system startup (μs). 
    I: GPS instance number (instance). 
    Status: GPS Fix type; 2D fix, 3D fix etc. (enum). 
    GMS: milliseconds since start of GPS Week (ms). 
    GWk: weeks since 5 Jan 1980. 
    NSats: number of satellites visible (satellites). 
    HDop: horizontal dilution of precision. 
    Lat: latitude (deglatitude). 
    Lng: longitude (deglongitude). 
    Alt: altitude (m). 
    Spd: ground speed (m/s). 
    GCrs: ground course (degheading). 
    VZ: vertical speed (m/s). 
    Yaw: vehicle yaw (degheading). 
    U: boolean value indicating whether this GPS is in use. 

Enums for 'Status' field:
    NO_GPS (0): No GPS connected/detected. 
    NO_FIX (1): Receiving valid GPS messages but no lock. 
    GPS_OK_FIX_2D (2): Receiving valid messages and 2D lock. 
    GPS_OK_FIX_3D (3): Receiving valid messages and 3D lock. 
    GPS_OK_FIX_3D_DGPS (4): Receiving valid messages and 3D lock with differential improvements. 
    GPS_OK_FIX_3D_RTK_FLOAT (5): Receiving valid messages and 3D RTK Float. 
    GPS_OK_FIX_3D_RTK_FIXED (6): Receiving valid messages and 3D RTK Fixed. 

Extra Information:
This message contains the fundamental position data from the GPS module. It tells you the drone's latitude, longitude, altitude, speed, and heading. Key things to check here are the 'NSats' (number of satellites) and 'Status'. A low number of satellites or a poor status (e.g., 'NO_FIX') will result in inaccurate positioning and unreliable navigation.
"""

HEAT = """
Table Description: IMU Heater data. 

Fields:
    TimeUS: Time since system startup. 
    Temp: Current IMU temperature. 
    Targ: Target IMU temperature. 
    P: Proportional portion of response. 
    I: Integral portion of response. 
    Out: Controller output to heating element. 

Extra Information:
High-end inertial sensors (IMUs) are sensitive to temperature changes. To ensure consistent performance, they are often equipped with a heater to maintain a stable operating temperature. This message shows if the heater is working correctly by comparing the actual 'Temp' to the 'Targ' (target) temperature. It's mostly relevant for professional systems flying in very cold conditions.
"""

IMU = """
Table Description: Inertial Measurement Unit data. 

Fields:
    TimeUS: Time since system startup (μs). 
    I: IMU sensor instance number (instance). 
    GyrX: measured rotation rate about X axis (rad/s). 
    GyrY: measured rotation rate about Y axis (rad/s). 
    GyrZ: measured rotation rate about Z axis (rad/s). 
    AccX: acceleration along X axis (m/s/s). 
    AccY: acceleration along Y axis (m/s/s). 
    AccZ: acceleration along Z axis (m/s/s). 
    EG: gyroscope error count. 
    EA: accelerometer error count. 
    T: IMU temperature (degC). 
    GH: gyroscope health. 
    AH: accelerometer health. 
    GHz: gyroscope measurement rate (Hz). 
    AHz: accelerometer measurement rate (Hz). 

Extra Information:
The IMU is the core of the drone's flight control system, providing the high-frequency motion data necessary for stable flight. The gyroscopes (GyrX/Y/Z) measure rotational velocity, while the accelerometers (AccX/Y/Z) measure linear acceleration, which includes both the drone's movement and the constant pull of gravity. The flight controller's primary task is to fuse these two sensor readings, typically using an Extended Kalman Filter (EKF), to produce an accurate, real-time estimate of the drone's attitude (its roll, pitch, and yaw orientation). This attitude estimate is the foundation for all autonomous and manual stabilization; the drone constantly compares its current attitude to the desired attitude (from the pilot or mission plan) and adjusts motor outputs to correct any errors. For post-flight analysis, this data is the most critical source for diagnosing flight problems. Excessive vibration, often caused by unbalanced propellers, a damaged frame, or failing motors, appears as high-frequency noise or "clipping" (where the sensor hits its maximum reading) in the accelerometer data. This noise can corrupt the attitude estimate, leading to poor flight performance, oscillations, and reduced efficiency.
"""

IOMC = """
Table Description: IOMCU diagnostic information. 

Fields:
    TimeUS: Time since system startup. 
    RSErr: Status Read error count (zeroed on successful read). 
    Mem: Free memory. 
    TS: IOMCU uptime. 
    NPkt: Number of packets received by IOMCU. 
    Nerr: Protocol failures on MCU side. 
    Nerr2: Reported number of failures on IOMCU side. 
    NDel: Number of delayed packets received by MCU.

Extra Information:
On some flight controllers, a separate "I/O" processor handles inputs and outputs. This message provides low-level diagnostic information about that specific chip. It is not used for normal flight analysis and is only relevant to hardware developers when debugging potential hardware failures. 
"""

ISBD = """
Table Description: InertialSensor Batch Logging Data. 

Fields:
    TimeUS: Time since system startup (μs). 
    N: batch sequence number. 
    seqno: sample sequence number. 
    x: x-axis sample value (m/s/s). 
    y: y-axis sample value (m/s/s). 
    z: z-axis sample value (m/s/s). 

Extra Information:
This message is part of a high-speed IMU logging system. It contains the actual sensor measurement data for a "batch" of readings defined in an 'ISBH' header message. This allows for very high-rate data capture, which is essential for advanced vibration analysis, but is generally too detailed for standard flight review.    
"""

ISBH = """
Table Description: InertialSensor Batch Logging Header. 

Fields:
    TimeUS: Time since system startup (μs). 
    N: batch sequence number. 
    type: indicates if this is accel or gyro data. 
    instance: IMU sensor instance. 
    mul: multiplier to be applied to samples in this batch. 
    smp_cnt: samples in this batch. 
    SampleUS: timestamp of first sample (μs). 
    smp_rate: rate at which samples have been collected (Hz). 

Extra Information:
This is the "header" message for a batch of high-speed IMU data. It defines how many samples are in the following 'ISBD' messages and at what rate they were captured. This system is designed for efficiency when logging sensor data thousands of times per second. A typical user would analyze the final vibration in the 'VIBE' message, while a developer might use these batch logs for deeper analysis.
"""

MAG = """
Table Description: Information received from compasses. 

Fields:
    TimeUS: Time since system startup (μs). 
    I: magnetometer sensor instance number (instance). 
    MagX: magnetic field strength in body frame (mGauss). 
    MagY: magnetic field strength in body frame (mGauss). 
    MagZ: magnetic field strength in body frame (mGauss). 
    OfsX: magnetic field offset in body frame (mGauss). 
    OfsY: magnetic field offset in body frame (mGauss). 
    OfsZ: magnetic field offset in body frame (mGauss). 
    MOX: motor interference magnetic field offset in body frame (mGauss). 
    MOY: motor interference magnetic field offset in body frame (mGauss). 
    MOZ: motor interference magnetic field offset in body frame (mGauss). 
    Health: true if the compass is considered healthy. 
    S: time measurement was taken (μs). 

Extra Information:
This message contains the raw data from the drone's compass (magnetometer). The compass is essential for determining the drone's heading (yaw). A common problem is magnetic interference from the drone's own power wires or motors. You would analyze this data to see if the magnetic field readings are stable or if they change erratically when the motors spin up, which would indicate an interference problem.
"""

MAV = """
Table Description: GCS MAVLink link statistics. 

Fields:
    TimeUS: Time since system startup (μs). 
    chan: mavlink channel number (instance). 
    txp: transmitted packet count. 
    rxp: received packet count. 
    rxdp: perceived number of packets we never received. 
    flags: compact representation of some state of the channel (bitmask). 
    ss: stream slowdown is the number of ms being added to each message to fit within bandwidth (ms). 
    tf: times buffer was full when a message was going to be sent. 
    mgs: time MAV_GCS_SYSID heartbeat (or manual control) last seen (ms). 

Enums for 'flags' field:
    USING_SIGNING (1). 
    ACTIVE (2). 
    STREAMING (4). 
    PRIVATE (8). 
    LOCKED (16). 

Extra Information:
This message provides statistics on the quality of the communication link between the drone and the ground control station (GCS). The 'rxdp' field (received dropped packets) is particularly important. A high number here indicates a poor or intermittent radio link, which could lead to a failsafe if communication is lost entirely.
"""

MAVC = """
Table Description: MAVLink command we have just executed. 

Fields:
    TimeUS: Time since system startup (μs). 
    TS: target system for command. 
    TC: target component for command. 
    SS: source system for command. 
    SC: source component for command. 
    Fr: command frame. 
    Cmd: mavlink command enum value. 
    P1: first parameter from mavlink packet. 
    P2: second parameter from mavlink packet. 
    P3: third parameter from mavlink packet. 
    P4: fourth parameter from mavlink packet. 
    X: X coordinate from mavlink packet. 
    Y: Y coordinate from mavlink packet. 
    Z: Z coordinate from mavlink packet. 
    Res: command result being returned from autopilot. 
    WL: true if this command arrived via a COMMAND_LONG rather than COMMAND_INT. 

Extra Information:
This message logs any commands sent to the drone from the ground station or another onboard computer. This is useful for verifying that the drone received and executed a command, such as "change mode," "set new waypoint," or "return to launch." It provides a record of external commands given to the vehicle during its flight.
"""

MODE = """
Table Description: vehicle control mode information. 

Fields:
    TimeUS: Time since system startup (μs). 
    Mode: vehicle-specific mode number. 
    ModeNum: alias for Mode. 
    Rsn: reason for entering this mode; enumeration value (enum). 

Enums for 'Rsn' field:
    UNKNOWN (0). 
    RC_COMMAND (1). 
    GCS_COMMAND (2). 
    RADIO_FAILSAFE (3). 
    BATTERY_FAILSAFE (4). 
    GCS_FAILSAFE (5). 
    EKF_FAILSAFE (6). 
    GPS_GLITCH (7). 
    MISSION_END (8). 
    THROTTLE_LAND_ESCAPE (9). 
    FENCE_BREACHED (10). 
    TERRAIN_FAILSAFE (11). 
    BRAKE_TIMEOUT (12). 
    FLIP_COMPLETE (13). 
    AVOIDANCE (14). 
    AVOIDANCE_RECOVERY (15). 
    THROW_COMPLETE (16). 
    TERMINATE (17). 
    TOY_MODE (18). 
    CRASH_FAILSAFE (19). 
    SOARING_FBW_B_WITH_MOTOR_RUNNING (20). 
    SOARING_THERMAL_DETECTED (21). 
    SOARING_THERMAL_ESTIMATE_DETERIORATED (22). 
    VTOL_FAILED_TRANSITION (23). 
    VTOL_FAILED_TAKEOFF (24). 
    FAILSAFE (25): general failsafes, prefer specific failsafes over this as much as possible. 
    INITIALISED (26). 
    SURFACE_COMPLETE (27). 
    BAD_DEPTH (28). 
    LEAK_FAILSAFE (29). 
    SERVOTEST (30). 
    STARTUP (31). 
    SCRIPTING (32). 
    UNAVAILABLE (33). 
    AUTOROTATION_START (34). 
    AUTOROTATION_BAILOUT (35). 
    SOARING_ALT_TOO_HIGH (36). 
    SOARING_ALT_TOO_LOW (37). 
    SOARING_DRIFT_EXCEEDED (38). 
    RTL_COMPLETE_SWITCHING_TO_VTOL_LAND_RTL (39). 
    RTL_COMPLETE_SWITCHING_TO_FIXEDWING_AUTOLAND (40). 
    MISSION_CMD (41). 
    FRSKY_COMMAND (42). 
    FENCE_RETURN_PREVIOUS_MODE (43). 
    QRTL_INSTEAD_OF_RTL (44). 
    AUTO_RTL_EXIT (45). 
    LOITER_ALT_REACHED_QLAND (46). 
    LOITER_ALT_IN_VTOL (47). 
    RADIO_FAILSAFE_RECOVERY (48). 
    QLAND_INSTEAD_OF_RTL (49). 
    DEADRECKON_FAILSAFE (50). 
    MODE_TAKEOFF_FAILSAFE (51). 
    DDS_COMMAND (52). 
    AUX_FUNCTION (53). 
    FIXED_WING_AUTOLAND (54). 
    FENCE_REENABLE (55). 

Extra Information:
This is a simple but very important message. It shows which flight mode the drone was in (e.g., Stabilize, Loiter, Auto, Return-to-Launch) at any given time. Unexpected mode changes are a huge clue when diagnosing a problem. The 'Rsn' (Reason) field is especially useful, as it explains *why* the mode changed, for example, due to a 'BATTERY_FAILSAFE'.
"""

MOTB = """
Table Description: Motor mixer information. 

Fields:
    TimeUS: Time since system startup (μs). 
    LiftMax: Maximum motor compensation gain. 
    BatVolt: Ratio between detected battery voltage and maximum battery voltage. 
    ThLimit: Throttle limit set due to battery current limitations. 
    ThrAvMx: Maximum average throttle that can be used to maintain attitude control, derived from throttle mix params. 
    ThrOut: Throttle output. 
    FailFlags: bit 0 motor failed, bit 1 motors balanced, should be 2 in normal flight. 

Extra Information:
This message provides insight into how the autopilot is managing power distribution to the motors. It's particularly useful for diagnosing power-related performance limits. For instance, the 'ThLimit' field shows if the system is intentionally reducing throttle to prevent excessive current draw from the battery. This can tell you if your drone is underpowered for the maneuvers it's attempting.
"""

MSG = """
Table Description: Textual messages. 

Fields:
    TimeUS: Time since system startup (μs). 
    Message: message text (char 64). 

Extra Information:
This is a human-readable log message. The software can print plain text status updates or warnings here, such as "GPS Glitch" or "EKF Initialised". It's often one of the easiest places to get a quick overview of the major events that occurred during a flight without needing to interpret complex data fields.
"""

MULT = """
Table Description: Message mapping from single character to numeric multiplier. 

Fields:
    TimeUS: Time since system startup (μs). 
    Id: character referenced by FMTU. 
    Mult: numeric multiplier. 

Extra Information:
This message is part of the log file's internal structure, working with 'FMT' and 'UNIT' to make the data self-describing. It defines multipliers that can be applied to raw data values to convert them to standard units. A user analyzing a log would not look at this message directly; it is used by the log parsing software.
"""

PARM = """
Table Description: parameter value. 

Fields:
    TimeUS: Time since system startup (μs). 
    Name: parameter name (char 16). 
    Value: parameter value. 
    Default: default parameter value for this board and config. 

Extra Information:
This message records the value of a specific configuration parameter at the beginning of the flight. This creates a snapshot of the drone's settings for that flight. It's extremely important for reproducibility and debugging, as it allows you to know the exact tuning and configuration that was active when a problem occurred.
"""

PIDA = """
Table Description: Proportional/Integral/Derivative gain values for vertical acceleration. 

Fields:
    TimeUS: Time since system startup (μs). 
    Tar: desired value. 
    Act: achieved value. 
    Err: error between target and achieved. 
    P: proportional part of PID. 
    I: integral part of PID. 
    D: derivative part of PID. 
    FF: controller feed-forward portion of response. 
    DFF: controller derivative feed-forward portion of response. 
    Dmod: scaler applied to D gain to reduce limit cycling. 
    SRate: slew rate used in slew limiter. 
    Flags: bitmask of PID state flags (bitmask). 

Enums for 'Flags' field:
    LIMIT (1): true if the output is saturated, I term anti windup is active. 
    PD_SUM_LIMIT (2): true if the PD sum limit is active. 
    RESET (4): true if the controller was reset. 
    I_TERM_SET (8): true if the I term has been set externally including reseting to 0. 

Extra Information:
This message (and the other PID messages) shows the performance of the drone's lowest-level control loops. This specific one is for vertical acceleration (throttle control). It compares the 'Tar' (target acceleration) with the 'Act' (actual acceleration). Flight control engineers analyze this data to tune the PID gains (P, I, D) to make the drone hold altitude smoothly and responsively.
"""

PIDE = """
Table Description: Proportional/Integral/Derivative gain values for East/West velocity. 

Fields:
    TimeUS: Time since system startup (μs). 
    Tar: desired value. 
    Act: achieved value. 
    Err: error between target and achieved. 
    P: proportional part of PID. 
    I: integral part of PID. 
    D: derivative part of PID. 
    FF: controller feed-forward portion of response. 
    DFF: controller derivative feed-forward portion of response. 
    Dmod: scaler applied to D gain to reduce limit cycling. 
    SRate: slew rate used in slew limiter. 
    Flags: bitmask of PID state flags (bitmask). 

Enums for 'Flags' field:
    LIMIT (1): true if the output is saturated, I term anti windup is active. 
    PD_SUM_LIMIT (2): true if the PD sum limit is active. 
    RESET (4): true if the controller was reset. 
    I_TERM_SET (8): true if the I term has been set externally including reseting to 0. 

Extra Information:
This message shows the performance of the position controller for East/West movement. It compares the drone's target velocity with its actual velocity along the East-West axis. It is used to tune how well the drone maintains its position and follows navigation commands in modes like Loiter or Auto.
"""

PIDN = """
Table Description: Proportional/Integral/Derivative gain values for North/South velocity. 

Fields:
    TimeUS: Time since system startup (μs). 
    Tar: desired value. 
    Act: achieved value. 
    Err: error between target and achieved. 
    P: proportional part of PID. 
    I: integral part of PID. 
    D: derivative part of PID. 
    FF: controller feed-forward portion of response. 
    DFF: controller derivative feed-forward portion of response. 
    Dmod: scaler applied to D gain to reduce limit cycling. 
    SRate: slew rate used in slew limiter. 
    Flags: bitmask of PID state flags (bitmask). 

Enums for 'Flags' field:
    LIMIT (1): true if the output is saturated, I term anti windup is active. 
    PD_SUM_LIMIT (2): true if the PD sum limit is active. 
    RESET (4): true if the controller was reset. 
    I_TERM_SET (8): true if the I term has been set externally including reseting to 0. 

Extra Information:
This message shows the performance of the position controller for North/South movement. It compares the drone's target velocity with its actual velocity along the North-South axis. Along with PIDE, it's used to tune how well the drone holds its position against wind and follows navigation waypoints.
"""

PIDP = """
Table Description: Proportional/Integral/Derivative gain values for Pitch rate. 

Fields:
    TimeUS: Time since system startup (μs). 
    Tar: desired value. 
    Act: achieved value. 
    Err: error between target and achieved. 
    P: proportional part of PID. 
    I: integral part of PID. 
    D: derivative part of PID. 
    FF: controller feed-forward portion of response. 
    DFF: controller derivative feed-forward portion of response. 
    Dmod: scaler applied to D gain to reduce limit cycling. 
    SRate: slew rate used in slew limiter. 
    Flags: bitmask of PID state flags (bitmask). 

Enums for 'Flags' field:
    LIMIT (1): true if the output is saturated, I term anti windup is active. 
    PD_SUM_LIMIT (2): true if the PD sum limit is active. 
    RESET (4): true if the controller was reset. 
    I_TERM_SET (8): true if the I term has been set externally including reseting to 0. 

Extra Information:
This message details the performance of the pitch stabilization controller. It compares the target pitch rotation rate ('Tar') with the actual rate measured by the gyro ('Act'). A large 'Err' or oscillations in the 'Act' value indicate that the pitch PID gains need tuning for better stability and responsiveness.
"""

PIDR = """
Table Description: Proportional/Integral/Derivative gain values for Roll rate. 

Fields:
    TimeUS: Time since system startup (μs). 
    Tar: desired value. 
    Act: achieved value. 
    Err: error between target and achieved. 
    P: proportional part of PID. 
    I: integral part of PID. 
    D: derivative part of PID. 
    FF: controller feed-forward portion of response. 
    DFF: controller derivative feed-forward portion of response. 
    Dmod: scaler applied to D gain to reduce limit cycling. 
    SRate: slew rate used in slew limiter. 
    Flags: bitmask of PID state flags (bitmask). 

Enums for 'Flags' field:
    LIMIT (1): true if the output is saturated, I term anti windup is active. 
    PD_SUM_LIMIT (2): true if the PD sum limit is active. 
    RESET (4): true if the controller was reset. 
    I_TERM_SET (8): true if the I term has been set externally including reseting to 0. 

Extra Information:
This message details the performance of the roll stabilization controller. It compares the target roll rotation rate ('Tar') with the actual rate measured by the gyro ('Act'). Along with PIDP, this is one of the most critical logs for tuning the core stability of a multirotor or plane to ensure it flies smoothly and without shaking.
"""

PIDY = """
Table Description: Proportional/Integral/Derivative gain values for Yaw rate. 

Fields:
    TimeUS: Time since system startup (μs). 
    Tar: desired value. 
    Act: achieved value. 
    Err: error between target and achieved. 
    P: proportional part of PID. 
    I: integral part of PID. 
    D: derivative part of PID. 
    FF: controller feed-forward portion of response. 
    DFF: controller derivative feed-forward portion of response. 
    Dmod: scaler applied to D gain to reduce limit cycling. 
    SRate: slew rate used in slew limiter. 
    Flags: bitmask of PID state flags (bitmask). 

Enums for 'Flags' field:
    LIMIT (1): true if the output is saturated, I term anti windup is active. 
    PD_SUM_LIMIT (2): true if the PD sum limit is active. 
    RESET (4): true if the controller was reset. 
    I_TERM_SET (8): true if the I term has been set externally including reseting to 0. 

Extra Information:
This message details the performance of the yaw (heading) stabilization controller. It compares the target yaw rotation rate with the actual rate. It's used to tune how well the drone holds its heading and responds to yaw commands from the pilot. Poor yaw tuning can lead to a "tail wag" or sluggish heading control.
"""

PM = """
Table Description: autopilot system performance and general data dumping ground. 

Fields:
    TimeUS: Time since system startup (μs). 
    LR: Main loop rate (Hz). 
    NLon: Number of long loops detected. 
    NL: Number of measurement loops for this message. 
    MaxT: Maximum loop time. 
    Mem: Free memory available (B). 
    Load: System processor load (d%). 
    InE: Internal error mask; which internal errors have been detected (bitmask). [cite: 296, 297]
    ErrL: Internal error line number; last line number on which a internal error was detected. [cite: 297, 298]
    ErC: Internal error count; how many internal errors have been detected. [cite: 298, 299]
    SPIC: Number of SPI transactions processed. 
    I2CC: Number of i2c transactions processed. 
    I2CI: Number of i2c interrupts serviced. 
    Ex: number of microseconds being added to each loop to address scheduler overruns (μs). 
    R: RTC time, time since Unix epoch (μs). 

Enums for 'InE' field:
    logger_mapfailure (1). 
    logger_missing_logstructure (2). 
    logger_logwrite_missingfmt (4). 
    logger_too_many_deletions (8). 
    logger_bad_getfilename (16). 
    panic (32). 
    logger_flushing_without_sem (64). 
    logger_bad_current_block (128). 
    logger_blockcount_mismatch (256). 
    logger_dequeue_failure (512). 
    constraining_nan (1024). 
    watchdog_reset (2048). 
    iomcu_reset (4096). 
    iomcu_fail (8192). 
    spi_fail (16384). 
    main_loop_stuck (32768). 
    gcs_bad_missionprotocol_link (65536). 
    bitmask_range (131072). 
    gcs_offset (262144). 
    i2c_isr (524288). 
    flow_of_control (1048576). 
    switch_full_sector_recursion (2097152). 
    bad_rotation (4194304). 
    stack_overflow (8388608). 
    imu_reset (16777216). 
    gpio_isr (33554432). 
    mem_guard (67108864). 
    dma_fail (134217728). 
    params_restored (268435456). 
    invalid_arg_or_result (536870912). 
    __LAST__ (1073741824). 

Extra Information:
This message acts like the drone's "Task Manager." It shows the health of the main flight computer, including its CPU load ('Load') and whether its main calculations are finishing on time ('NLon' - Number of Long Loops). If the CPU is overloaded or loops are taking too long, it can lead to unstable flight, so this is a key health indicator for the flight controller hardware.
"""

POS = """
Table Description: Canonical vehicle position. 

Fields:
    TimeUS: Time since system startup (μs). 
    Lat: Canonical vehicle latitude (deglatitude). 
    Lng: Canonical vehicle longitude (deglongitude). 
    Alt: Canonical vehicle altitude (m). 
    RelHomeAlt: Canonical vehicle altitude relative to home (m). 
    RelOriginAlt: Canonical vehicle altitude relative to navigation origin (m).

Extra Information:
This message provides the single "best guess" of the vehicle's true position. The flight controller's EKF (Extended Kalman Filter) combines data from GPS, barometer, and accelerometers to produce this final, filtered position estimate. When you want to plot the drone's flight path on a map, this is the data you should use.
"""

POWR = """
Table Description: System power information. 

Fields:
    TimeUS: Time since system startup (μs). 
    Vcc: Flight board voltage (V). 
    VServo: Servo rail voltage (V). 
    Flags: System power flags (bitmask). 
    AccFlags: Accumulated System power flags; all flags which have ever been set (bitmask). [cite: 310, 311]
    Safety: Hardware Safety Switch status. 

Enums for 'Flags' and 'AccFlags' fields:
    BRICK_VALID (1): main brick power supply valid. 
    SERVO_VALID (2): main servo power supply valid for FMU. 
    USB_CONNECTED (4): USB power is connected. 
    PERIPH_OVERCURRENT (8): peripheral supply is in over-current state. 
    PERIPH_HIPOWER_OVERCURRENT (16): hi-power peripheral supply is in over-current state. 
    CHANGED (32): Power status has changed since boot. 

Extra Information:
This message monitors the health of the flight controller's own power supply, not the main flight battery. It shows the board's internal voltage ('Vcc'). It's useful for diagnosing hardware problems, like a failing voltage regulator, or for confirming events like a USB connection. A drop in 'Vcc' can cause the processor to reset or behave erratically.
"""

PSCD = """
Table Description: Position Control Down. 

Fields:
    TimeUS: Time since system startup (μs). 
    DPD: Desired position relative to EKF origin + Offsets (m). 
    TPD: Target position relative to EKF origin (m). 
    PD: Position relative to EKF origin (m). 
    DVD: Desired velocity Down (m/s). 
    TVD: Target velocity Down (m/s). 
    VD: Velocity Down (m/s). 
    DAD: Desired acceleration Down (m/s/s). 
    TAD: Target acceleration Down (m/s/s). 
    AD: Acceleration Down (m/s/s). 

Extra Information:
This message provides a detailed look into how the autopilot is controlling its vertical position. It breaks down the desired vs. actual position, velocity, and acceleration along the Down axis. This is useful for analyzing how well the drone is holding its altitude or executing vertical movements in modes like 'Loiter' or 'Auto'.
"""

PSCE = """
Table Description: Position Control East. 

Fields:
    TimeUS: Time since system startup (μs). 
    DPE: Desired position relative to EKF origin + Offsets (m). 
    TPE: Target position relative to EKF origin (m). 
    PE: Position relative to EKF origin (m). 
    DVE: Desired velocity East (m/s). 
    TVE: Target velocity East (m/s). 
    VE: Velocity East (m/s). 
    DAE: Desired acceleration East (m/s/s). 
    TAE: Target acceleration East (m/s/s). 
    AE: Acceleration East (m/s/s). 

Extra Information:
This message provides a detailed look into how the autopilot is controlling its lateral position along the East-West axis. It breaks down the desired vs. actual position, velocity, and acceleration. This is useful for analyzing how well the drone is holding its position against wind or tracking a line during a mission.
"""

PSCN = """
Table Description: Position Control North. 

Fields:
    TimeUS: Time since system startup (μs). 
    DPN: Desired position relative to EKF origin (m). 
    TPN: Target position relative to EKF origin (m). 
    PN: Position relative to EKF origin (m). 
    DVN: Desired velocity North (m/s). 
    TVN: Target velocity North (m/s). 
    VN: Velocity North (m/s). 
    DAN: Desired acceleration North (m/s/s). 
    TAN: Target acceleration North (m/s/s). 
    AN: Acceleration North (m/s/s). 

Extra Information:
This message provides a detailed look into how the autopilot is controlling its lateral position along the North-South axis. It breaks down the desired vs. actual position, velocity, and acceleration. Together with PSCE, it gives a complete picture of the drone's horizontal navigation performance.
"""

RAD = """
Table Description: Telemetry radio statistics. 

Fields:
    TimeUS: Time since system startup (μs). 
    RSSI: RSSI. 
    RemRSSI: RSSI reported from remote radio. 
    TxBuf: number of bytes in radio ready to be sent. 
    Noise: local noise floor. 
    RemNoise: local noise floor reported from remote radio. 
    RxErrors: damaged packet count. 
    Fixed: fixed damaged packet count. 

Extra Information:
This message shows the status of the telemetry radio link, which is used for communication with the ground station. The 'RSSI' (Received Signal Strength Indicator) and 'RemRSSI' (Remote RSSI) are the most important fields. They tell you the signal strength at both the drone and the ground station. Low values indicate that the drone is far away or there is radio interference.
"""

RATE = """
Table Description: Desired and achieved vehicle attitude rates.  Not logged in Fixed Wing Plane modes. 

Fields:
    TimeUS: Time since system startup (μs). 
    RDes: vehicle desired roll rate (deg/s). 
    R: achieved vehicle roll rate (deg/s). 
    ROut: normalized output for Roll. 
    PDes: vehicle desired pitch rate (deg/s). 
    P: vehicle pitch rate (deg/s). 
    POut: normalized output for Pitch. 
    Y: achieved vehicle yaw rate (deg/s). 
    YOut: normalized output for Yaw (deg/s). 
    YDes: vehicle desired yaw rate. 
    ADes: desired vehicle vertical acceleration (cm/s/s). 
    A: achieved vehicle vertical acceleration (cm/s/s). 
    AOut: percentage of vertical thrust output current being used. 
    AOutSlew: vertical thrust output slew rate. 

Extra Information:
This message is crucial for tuning the drone's responsiveness and stability. It compares the desired rotation *speed* (e.g., how fast the pilot wants to roll) with the actual rotation speed measured by the gyros. If the actual rate doesn't track the desired rate well, it can make the drone feel sluggish or overly aggressive. The PIDR, PIDP, and PIDY logs show the underlying controller behavior that drives these rates.
"""

RCI2 = """
Table Description: (More) RC input channels to vehicle. 

Fields:
    TimeUS: Time since system startup (μs). 
    C15: channel 15 input (us). 
    C16: channel 16 input (us). 
    OMask: bitmask of RC channels being overridden by mavlink input. 
    Flags: bitmask of RC state flags (bitmask). 

Enums for 'Flags' field:
    HAS_VALID_INPUT (1): true if the system is receiving good RC values. 
    IN_RC_FAILSAFE (2): true if the system is current in RC failsafe. 

Extra Information:
This message is a continuation of the 'RCIN' message, providing data for radio control channels 15 and 16. It also contains important status flags, such as whether the RC receiver has a valid signal or if it has entered a failsafe state due to lost connection with the pilot's transmitter.
"""

RCIN = """
Table Description: RC input channels to vehicle. 

Fields:
    TimeUS: Time since system startup (μs). 
    C1: channel 1 input (us). 
    C2: channel 2 input (us). 
    C3: channel 3 input (us). 
    C4: channel 4 input (us). 
    C5: channel 5 input (us). 
    C6: channel 6 input (us). 
    C7: channel 7 input (us). 
    C8: channel 8 input (us). 
    C9: channel 9 input (us). 
    C10: channel 10 input (us). 
    C11: channel 11 input (us). 
    C12: channel 12 input (us). 
    C13: channel 13 input (us). 
    C14: channel 14 input (us).

Extra Information:
This is a direct recording of the commands sent from the pilot's remote control. C1-C4 typically correspond to roll, pitch, yaw, and throttle. When analyzing a crash or unexpected behavior, this is one of the most important logs to check, as it shows you exactly what the pilot was commanding the drone to do at the moment of the incident. 
"""

RCO2 = """
Table Name: RCO2

Table Description: Servo channel output values 15 to 18.

Fields:
    TimeUS: Time since system startup (μs).
    C15: channel 15 output (us). 
    C16: channel 16 output (us). 
    C17: channel 17 output (us). 
    C18: channel 18 output (us). 

Extra Information:
This message is a continuation of the RCOU message, showing the final command signals being sent out on channels 15 through 18. These higher channels are typically used for controlling auxiliary devices like cameras, grippers, or landing gear.
"""

RCOU = """
Table Name: RCOU

Table Description: Servo channel output values 1 to 14.

Fields:
    TimeUS: Time since system startup (μs). 
    C1: channel 1 output (us). 
    C2: channel 2 output (us). 
    C3: channel 3 output (us). 
    C4: channel 4 output (us). 
    C5: channel 5 output (us). 
    C6: channel 6 output (us). 
    C7: channel 7 output (us). 
    C8: channel 8 output (us). 
    C9: channel 9 output (us). 
    C10: channel 10 output (us). 
    C11: channel 11 output (us). 
    C12: channel 12 output (us). 
    C13: channel 13 output (us). 
    C14: channel 14 output (us). 

Extra Information:
This message shows the final command signals that the flight controller is sending to the motors (or servos on a plane). By comparing 'RCIN' (pilot's command) with 'RCOU' (motor output), you can see how the autopilot is translating the pilot's intent into action. In stabilized modes, these values will be constantly changing as the controller works to keep the drone level.
"""

STAK = """
Table Description: Stack information. 

Fields:
    TimeUS: Time since system startup (μs). 
    Id: thread ID (instance). 
    Pri: thread priority. 
    Total: total stack. 
    Free: free stack. 
    Name: thread name (char 16). 

Extra Information:
This is a low-level diagnostic message for software developers. It provides information about the memory usage (stack) for different software processes running on the flight controller. It is not used for analyzing flight characteristics but is crucial for debugging complex software issues like memory leaks or stack overflows.
"""

TSYN = """
Table Description: Time synchronisation response information. 

Fields:
    TimeUS: Time since system startup (μs). 
    SysID: system ID this data is for. 
    RTT: round trip time for this system (μs). 

Extra Information:
Think of this like checking if all the clocks in a network are set to the same time. In a drone, different components (like the flight controller and a companion computer) need to have a synchronized sense of time to correctly align their data. You'd look at this log if you suspect that data from different sources isn't lining up correctly, which could cause issues in advanced navigation or data analysis. A high RTT (Round Trip Time) might indicate a communication delay between components.
"""

UNIT = """
Table Description: Message mapping from single character to SI unit. 

Fields:
    TimeUS: Time since system startup (μs). 
    Id: character referenced by FMTU. 
    Label: Unit - SI where available (char 64). 

Extra Information:
This is essentially a legend or a key for other parts of the log. Other log messages might say a value is of type 'v', and this UNIT message tells you that 'v' means "Volts". It's a foundational message that helps software correctly interpret and display all the other data. You wouldn't typically look at this for flight diagnostics, but it's critical for any program that reads and analyzes the logs.
"""

VER = """
Table Description: Ardupilot version. 

Fields:
    TimeUS: Time since system startup (μs). 
    BT: Board type (enum). 
    BST: Board subtype (enum). 
    Maj: Major version number. 
    Min: Minor version number. 
    Pat: Patch number. 
    FWT: Firmware type. 
    GH: Github commit. 
    FWS: Firmware version string (char 64). 
    APJ: Board ID. 
    BU: Build vehicle type (enum). 
    FV: Filter version. 
    IMI: IOMCU MCU ID. 
    ICI: IOMCU CPU ID. 

Enums for 'BT' field:
    HAL_BOARD_SITL (3). 
    HAL_BOARD_LINUX (7). 
    HAL_BOARD_CHIBIOS (10). 
    HAL_BOARD_ESP32 (12). 
    HAL_BOARD_QURT (13). 
    HAL_BOARD_EMPTY (99). 

Enums for 'BST' field:
    HAL_BOARD_SUBTYPE_NONE (-1). 
    ... (and many other board subtypes) 

Enums for 'BU' field:
    APM_BUILD_Rover (1). 
    APM_BUILD_ArduCopter (2). 
    APM_BUILD_ArduPlane (3). 
    APM_BUILD_AntennaTracker (4). 
    APM_BUILD_UNKNOWN (5). 
    APM_BUILD_Replay (6). 
    APM_BUILD_ArduSub (7). 
    APM_BUILD_iofirmware (8). 
    APM_BUILD_AP_Periph (9). 
    APM_BUILD_AP_DAL_Standalone (10). 
    APM_BUILD_AP_Bootloader (11). 
    APM_BUILD_Blimp (12). 
    APM_BUILD_Heli (13). 

Extra Information:
This message is logged once at the beginning of the flight and provides a snapshot of the exact firmware version and hardware being used. It is one of the first things you should check when diagnosing a problem. Knowing the firmware version is crucial because bugs or changes in flight behavior are often specific to certain releases. It provides essential context before you dive deeper into other log data.
"""

VIBE = """
Table Description: Processed (acceleration) vibration information. 

Fields:
    TimeUS: Time since system startup (μs). 
    IMU: Vibration instance number (instance). 
    VibeX: Primary accelerometer filtered vibration, x-axis (m/s/s). 
    VibeY: Primary accelerometer filtered vibration, y-axis (m/s/s). 
    VibeZ: Primary accelerometer filtered vibration, z-axis (m/s/s). 
    Clip: Number of clipping events on 1st accelerometer. 

Extra Information:
Drones are sensitive to vibrations, which often come from motors and propellers. Excessive vibration can confuse the sensors, leading to unstable flight. Think of it like trying to read a book in a shaky car. This message tells you how much vibration the drone is experiencing. You'd check this log if the drone flies erratically or you get "high vibration" warnings. High values for VibeX/Y/Z or a non-zero Clip count are clear indicators that you need to check for unbalanced props, loose components, or improve your vibration damping.
"""

XKF1 = """
Table Description: EKF3 estimator outputs. 

Fields:
    TimeUS: Time since system startup (μs). 
    C: EKF3 core this data is for (instance). 
    Roll: Estimated roll (deg). 
    Pitch: Estimated pitch (deg). 
    Yaw: Estimated yaw (degheading). 
    VN: Estimated velocity (North component) (m/s). 
    VE: Estimated velocity (East component) (m/s). 
    VD: Estimated velocity (Down component) (m/s). 
    dPD: Filtered derivative of vertical position (down) (m/s). 
    PN: Estimated distance from origin (North component) (m). 
    PE: Estimated distance from origin (East component) (m). 
    PD: Estimated distance from origin (Down component) (m). 
    GX: Estimated gyro bias, X axis (deg/s). 
    GY: Estimated gyro bias, Y axis (deg/s). 
    GZ: Estimated gyro bias, Z axis (deg/s). 
    OH: Height of origin above WGS-84 (m). 

Extra Information:
This message contains the EKF's (Extended Kalman Filter) "best guess" of the drone's state. It fuses noisy data from multiple sensors (GPS, IMU, barometer) to produce a single, clean estimate of the drone's attitude, velocity, and position. This is one of the most important messages for post-flight analysis. You would plot these fields to visualize the actual flight path and orientation of the vehicle, and compare it to the pilot's commands or the autonomous mission plan to understand how the drone performed.
"""

XKF2 = """
Table Description: EKF3 estimator secondary outputs. 

Fields:
    TimeUS: Time since system startup (μs). 
    C: EKF3 core this data is for (instance). 
    AX: Estimated accelerometer X bias. 
    AY: Estimated accelerometer Y bias. 
    AZ: Estimated accelerometer Z bias. 
    VWN: Estimated wind velocity (moving-to-North component) (m/s). 
    VWE: Estimated wind velocity (moving-to-East component) (m/s). 
    MN: Magnetic field strength (North component) (mGauss). 
    ME: Magnetic field strength (East component) (mGauss). 
    MD: Magnetic field strength (Down component) (mGauss). 
    MX: Magnetic field strength (body X-axis) (mGauss). 
    MY: Magnetic field strength (body Y-axis) (mGauss). 
    MZ: Magnetic field strength (body Z-axis) (mGauss). 
    IDX: Innovation in vehicle drag acceleration (X-axis component) (m/s/s). 
    IDY: Innovation in vehicle drag acceleration (Y-axis component) (m/s/s). 
    IS: Innovation in vehicle sideslip (rad).

Extra Information:
This message provides insight into the corrections and external factors the EKF is estimating. The accelerometer biases (`AX`, `AY`, `AZ`) show how much the EKF is correcting for persistent errors in the accelerometer readings; large or unstable biases might suggest a need for recalibration. The wind velocity estimates (`VWN`, `VWE`) are very useful for explaining why a drone might be using more power or struggling to track a straight line in windy conditions.
"""

XKF3 = """
Table Description: EKF3 innovations. 

Fields:
    TimeUS: Time since system startup (μs). 
    C: EKF3 core this data is for (instance). 
    IVN: Innovation in velocity (North component) (m/s). 
    IVE: Innovation in velocity (East component) (m/s). 
    IVD: Innovation in velocity (Down component) (m/s). 
    IPN: Innovation in position (North component) (m). 
    IPE: Innovation in position (East component) (m). 
    IPD: Innovation in position (Down component) (m). 
    IMX: Innovation in magnetic field strength (X-axis component) (mGauss). 
    IMY: Innovation in magnetic field strength (Y-axis component) (mGauss). 
    IMZ: Innovation in magnetic field strength (Z-axis component) (mGauss). 
    IYAW: Innovation in vehicle yaw (deg). 
    IVT: Innovation in true-airspeed (UNKNOWN). 
    RErr: Accumulated relative error of this core with respect to active primary core. 
    ErSc: A consolidated error score where higher numbers are less healthy. 

Extra Information:
"Innovations" represent the difference between the sensor's measurement and what the EKF predicted that measurement would be. This message is extremely powerful for diagnosing sensor health. For example, if the GPS signal suddenly becomes noisy, the velocity innovations (`IVN`, `IVE`) will spike because the GPS readings are disagreeing with the EKF's predictions based on the IMU. Consistently high innovations for a particular sensor (e.g., magnetism `IMX`, `IMY`, `IMZ`) point directly to the source of a navigation problem. The `ErSc` (Error Score) is a great at-a-glance health indicator.
"""

XKF4 = """
Table Description: EKF3 variances. 
SV, SP, SH and SM are probably best described as ‘Squared Innovation Test Ratios’ where values <1 tells us the measurement was accepted and >1 tells us it was rejected.  They represent the square of the (innovation / maximum allowed innovation) where the innovation is the difference between predicted and measured value and the maximum allowed innovation is determined from the uncertainty of the measurement, uncertainty of the prediction and scaled using the number of standard deviations set by the innovation gate parameter for that measurement, eg EK3_MAG_I_GATE, EK3_HGT_I_GATE, etc. 

Fields:
    TimeUS: Time since system startup (μs). 
    C: EKF3 core this data is for (instance). 
    SV: Square root of the velocity variance. 
    SP: Square root of the position variance. 
    SH: Square root of the height variance. 
    SM: Magnetic field variance. 
    SVT: Square root of the total airspeed variance. 
    errRP: Filtered error in roll/pitch estimate. 
    OFN: Most recent position reset (North component) (m). 
    OFE: Most recent position reset (East component) (m). 
    FS: Filter fault status. 
    TS: Filter timeout status bitmask (0:position measurement, 1:velocity measurement, 2:height measurement, 3:magnetometer measurement, 4:airspeed measurement, 5:drag measurement). 
    SS: Filter solution status (bitmask). 
    GPS: Filter GPS status. 
    PI: Primary core index. 

Enums for 'SS' field:
    ATTITUDE_VALID (1): attitude estimate valid. 
    HORIZ_VEL (2): horizontal velocity estimate valid. 
    VERT_VEL (4): vertical velocity estimate valid. 
    HORIZ_POS_REL (8): relative horizontal position estimate valid. 
    HORIZ_POS_ABS (16): absolute horizontal position estimate valid. 
    VERT_POS (32): vertical position estimate valid. 
    TERRAIN_ALT (64): terrain height estimate valid. 
    CONST_POS_MODE (128): in constant position mode. 
    PRED_HORIZ_POS_REL (256): expected good relative horizontal position estimate - used before takeoff. 
    PRED_HORIZ_POS_ABS (512): expected good absolute horizontal position estimate - used before takeoff. 
    TAKEOFF_DETECTED (1024): optical flow takeoff has been detected. 
    TAKEOFF_EXPECTED (2048): compensating for baro errors during takeoff. 
    TOUCHDOWN_EXPECTED (4096): compensating for baro errors during touchdown. 
    USING_GPS (8192): using GPS position. 
    GPS_GLITCHING (16384): GPS glitching is affecting navigation accuracy. 
    GPS_QUALITY_GOOD (32768): can use GPS for navigation. 
    INITALIZED (65536): has ever been healthy. 
    REJECTING_AIRSPEED (131072): rejecting airspeed data. 
    DEAD_RECKONING (262144): dead reckoning (e.g. no position or velocity source). 

Extra Information:
This message reports on the EKF's internal health and confidence. The variance fields (`SV`, `SP`, `SH`) tell you how uncertain the EKF is about its own estimates; high values indicate low confidence. The most useful fields are the status bitmasks, `FS` and `SS`. By decoding these bitmasks, you can get a quick, definitive summary of the EKF's condition, such as whether it thinks the attitude is valid, if it's using GPS, or if it has detected a GPS glitch. This should be one of the first places you look to get a high-level overview of navigation health.
"""

XKF5 = """
Table Description: EKF3 Sensor innovations (primary core) and general dumping ground. 

Fields:
    TimeUS: Time since system startup (μs). 
    C: EKF3 core this data is for (instance). 
    NI: Normalised flow variance. 
    FIX: Optical flow LOS rate vector innovations from the main nav filter (X-axis). 
    FIY: Optical flow LOS rate vector innovations from the main nav filter (Y-axis). 
    AFI: Optical flow LOS rate innovation from terrain offset estimator. 
    HAGL: Height above ground level (m). 
    offset: Estimated vertical position of the terrain relative to the nav filter zero datum (UNKNOWN). 
    RI: Range finder innovations (UNKNOWN). 
    rng: Measured range (UNKNOWN). 
    Herr: Filter ground offset state error (m). 
    eAng: Magnitude of angular error (rad). 
    eVel: Magnitude of velocity error (m/s). 
    ePos: Magnitude of position error (m). 

Extra Information:
This message is a specialized version of the innovations message (XKF3), focusing on data from auxiliary sensors like optical flow and rangefinders. You would analyze this data when diagnosing issues with GPS-denied flight or precision landing systems. For example, high optical flow innovations (`FIX`, `FIY`) could indicate poor performance due to a low-contrast surface or flying too high. The `HAGL` (Height Above Ground Level) field is particularly useful, providing a direct estimate of the drone's altitude above the terrain below it, which is often more relevant than altitude above sea level.
"""

XKFM = """
Table Description: EKF3 diagnostic data for on-ground-and-not-moving check. 

Fields:
    TimeUS: Time since system startup (μs). 
    C: EKF core this message instance applies to (instance). 
    OGNM: True of on ground and not moving. 
    GLR: Gyroscope length ratio. 
    ALR: Accelerometer length ratio. 
    GDR: Gyroscope rate of change ratio. 
    ADR: Accelerometer rate of change ratio. 

Extra Information:
This is a simple diagnostic message that shows the status of the EKF's internal logic for determining if the vehicle is stationary on the ground. This logic is important because the EKF uses this 'on ground' state to perform sensor calibrations and checks before takeoff. You would typically only look at this message to confirm that the EKF correctly identified the pre-flight stationary condition before the flight began.
"""

XKFS = """
Table Description: EKF3 sensor selection. 

Fields:
    TimeUS: Time since system startup (μs). 
    C: EKF3 core this data is for (instance). 
    MI: compass selection index. 
    BI: barometer selection index. 
    GI: GPS selection index. 
    AI: airspeed selection index. 
    SS: Source Set (primary=0/secondary=1/tertiary=2). 
    GPS_GTA: GPS good to align. 
    GPS_CHK_WAIT: Waiting for GPS checks to pass. 
    MAG_FUSION: Magnetometer fusion (0=not fusing/1=fuse yaw/2=fuse mag). 

Extra Information:
This message is vital for vehicles equipped with redundant sensors (e.g., two GPS modules, multiple compasses). It shows which specific sensor the EKF is currently listening to. If a drone suddenly starts behaving erratically, checking this message can reveal if the EKF switched from a healthy primary sensor to a faulty secondary one. It provides a clear trace of the EKF's sensor fallback logic in action.
"""

XKQ = """
Table Description: EKF3 quaternion defining the rotation from NED to XYZ (autopilot) axes. 

Fields:
    TimeUS: Time since system startup (μs). 
    C: EKF3 core this data is for (instance). 
    Q1: Quaternion a term
    Q2: Quaternion b term  
    Q3: Quaternion c term 
    Q4: Quaternion d term 

Extra Information:
This message represents the vehicle's attitude (orientation in 3D space) using quaternions. While the XKF1 message provides attitude in human-readable Euler angles (roll, pitch, yaw), quaternions are the format used internally for calculations because they avoid a mathematical singularity problem known as "gimbal lock." You would typically use this message for advanced analysis, such as creating a 3D visualization of the flight or interfacing with robotics software that uses quaternions.
"""

XKT = """
Table Description: EKF3 timing information. 

Fields:
    TimeUS: Time since system startup (μs). 
    C: EKF core this message instance applies to (instance). 
    Cnt: count of samples used to create this message (s). 
    IMUMin: smallest IMU sample interval (s). 
    IMUMax: largest IMU sample interval (s). 
    EKFMin: low-passed achieved average time step rate for the EKF (minimum) (s). 
    EKFMax: low-passed achieved average time step rate for the EKF (maximum) (s). 
    AngMin: accumulated measurement time interval for the delta angle (minimum) (s). 
    AngMax: accumulated measurement time interval for the delta angle (maximum) (s). 
    VMin: accumulated measurement time interval for the delta velocity (minimum) (s). 
    VMax: accumulated measurement time interval for the delta velocity (maximum) (s). 

Extra Information:
This message is used for diagnosing performance issues with the flight controller's processor. It shows how much time is being spent on the EKF calculations and how consistently the sensor data is arriving. If the `EKFMax` value is very high or the `IMUMax` is much larger than the average, it could indicate that the processor is overloaded. An overloaded CPU can't keep up with the calculations needed for stable flight, leading to poor performance.
"""

XKV1 = """
Table Description: EKF3 State variances (primary core). 

Fields:
    TimeUS: Time since system startup (μs). 
    C: EKF3 core this data is for (instance). 
    V00: Variance for state 0 (attitude quaternion). 
    V01: Variance for state 1 (attitude quaternion). 
    V02: Variance for state 2 (attitude quaternion). 
    V03: Variance for state 3 (attitude quaternion). 
    V04: Variance for state 4 (velocity-north). 
    V05: Variance for state 5 (velocity-east). 
    V06: Variance for state 6 (velocity-down). 
    V07: Variance for state 7 (position-north). 
    V08: Variance for state 8 (position-east). 
    V09: Variance for state 9 (position-down). 
    V10: Variance for state 10 (delta-angle-bias-x). 
    V11: Variance for state 11 (delta-angle-bias-y). 

Extra Information:
This message, along with XKV2, offers a deep dive into the EKF's internal confidence for each specific state it estimates. Variance is a statistical measure of uncertainty. A low variance for a state (e.g., `V04` for north-velocity) means the EKF is very confident in its estimate for that value. These are the raw numbers behind the summarized variances in XKF4. You would analyze these fields for highly detailed, expert-level diagnostics to pinpoint exactly which part of the state estimate is uncertain.
"""

XKV2 = """
Table Description: more EKF3 State Variances (primary core). 

Fields:
    TimeUS: Time since system startup (μs). 
    C: EKF3 core this data is for (instance). 
    V12: Variance for state 12 (delta-angle-bias-z). 
    V13: Variance for state 13 (delta-velocity-bias-x). 
    V14: Variance for state 14 (delta-velocity-bias-y). 
    V15: Variance for state 15 (delta-velocity-bias-z). 
    V16: Variance for state 16 (Earth-frame mag-field-bias-x). 
    V17: Variance for state 17 (Earth-frame mag-field-bias-y). 
    V18: Variance for state 18 (Earth-frame mag-field-bias-z). 
    V19: Variance for state 19 (body-frame mag-field-bias-x). 
    V20: Variance for state 20 (body-frame mag-field-bias-y). 
    V21: Variance for state 21 (body-frame mag-field-bias-z). 
    V22: Variance for state 22 (wind-north). 
    V23: Variance for state 23 (wind-east). 

Extra Information:
This message is a continuation of XKV1, providing the EKF's internal uncertainty for the remaining states, particularly the sensor biases and wind estimates. For example, a high variance in the magnetometer bias states (`V16`, `V17`, `V18`) would indicate that the EKF is struggling to compensate for magnetic interference, which would likely lead to poor heading estimation. Analyzing these values is key for advanced debugging of sensor fusion issues.
"""


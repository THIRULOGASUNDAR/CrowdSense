# CrowdSense — Physical Device Appium Testing
# Complete Setup Guide (USB Cable Testing)
# ============================================

## What This Does

Just like **Selenium automatically opens Chrome** and tests a website,
**Appium automatically opens your CrowdSense app on your Android phone**
and tests every screen — fully automatic, no touching the phone needed.

- ✅ Plug phone into laptop via USB cable
- ✅ Run one `.bat` file
- ✅ Watch the app automatically open and test every screen on your phone
- ✅ Excel report is generated with full pass/fail results

---

## Step 1 — Install Required Software (One-Time Setup)

### 1A. Install Node.js
Download from: https://nodejs.org/  (choose LTS version)

Verify:
```
node --version
npm --version
```

### 1B. Install Appium 2.x
Open a terminal (PowerShell or CMD) and run:
```
npm install -g appium
```

Verify:
```
appium --version
```
Expected output: `2.x.x`

### 1C. Install UiAutomator2 Driver (for Android)
```
appium driver install uiautomator2
```

Verify it installed:
```
appium driver list --installed
```
You should see `uiautomator2` listed.

### 1D. Install Python Dependencies
Open a terminal in the `crowdsense` project folder and run:
```
pip install -r appium_physical_device_tests\requirements.txt
```

### 1E. Verify ADB is in PATH
ADB (Android Debug Bridge) comes with Android Studio.

Check if it works:
```
adb version
```

If **ADB not found**, add it to PATH:
1. Open Android Studio
2. Go to `File > Settings > Appearance & Behavior > System Settings > Android SDK`
3. Copy the SDK Location path (e.g. `C:\Users\thiru\AppData\Local\Android\Sdk`)
4. Add `<SDK_PATH>\platform-tools` to your Windows PATH:
   - Search "Environment Variables" in Windows
   - Edit `Path` under System Variables
   - Add the `platform-tools` folder path
5. Restart your terminal

---

## Step 2 — Enable USB Debugging on Your Android Phone

Do this **once** on your phone:

1. Go to **Settings → About Phone**
2. Tap **"Build Number"** exactly **7 times** until you see *"You are now a developer!"*
3. Go back to **Settings → Developer Options** (now visible)
4. Turn **ON** → **USB Debugging**
5. Turn **ON** → **Stay Awake** (optional, keeps screen on during testing)

---

## Step 3 — Connect Your Phone via USB

1. Use a **USB Data Cable** (not a charging-only cable)
2. Plug into your laptop
3. On your phone, a popup will appear: **"Allow USB Debugging?"**
4. Tap **"Always Allow from this computer"** → **OK**

Verify the phone is detected:
```
adb devices
```

You should see something like:
```
List of devices attached
RZ8N90XXXXX    device        ← This is your phone (not "emulator-5554")
```

If you see `unauthorized` instead of `device` — unlock your phone and tap "Allow" again.

---

## Step 4 — Build the Flutter APK

Open a terminal and run:
```
cd C:\Users\thiru\StudioProjects\crowdsense\frontend
flutter build apk --debug
```

This creates the APK at:
```
frontend\build\app\outputs\flutter-apk\app-debug.apk
```

> **Note:** The `run_physical_tests.bat` script will auto-build the APK if it's missing.

---

## Step 5 — Run the Tests

### Option A: Double-click the batch file (Easiest)
Navigate to:
```
C:\Users\thiru\StudioProjects\crowdsense\
```
Double-click **`run_physical_tests.bat`**

The script will:
1. ✅ Check Python, ADB, and device connection
2. ✅ Auto-start Appium server if not running
3. ✅ Install the APK directly onto your phone
4. ✅ **Your phone screen lights up — app opens automatically!**
5. ✅ Tests run — every screen is opened and tested one by one
6. ✅ Excel report saved to `appium_physical_device_tests\reports\`

### Option B: Command line with specific test groups
```bat
# Run ALL 100 tests (25-45 minutes)
run_physical_tests.bat

# Run only smoke tests — 10 tests, ~5 minutes (best for quick check)
run_physical_tests.bat smoke

# Run only authentication screen tests
run_physical_tests.bat auth

# Run only home & navigation tests
run_physical_tests.bat home

# Run only search & place tests
run_physical_tests.bat search

# Run only profile & settings tests
run_physical_tests.bat profile

# Run only travel planner & favorites tests
run_physical_tests.bat planner

# Check device + server only (no tests)
run_physical_tests.bat check
```

### Option C: Run directly with pytest
```bat
# Start Appium server first (in a separate terminal):
npx appium

# Then run tests (in another terminal):
cd C:\Users\thiru\StudioProjects\crowdsense
python -m pytest appium_physical_device_tests\ -v --tb=short
```

---

## Step 6 — View the Excel Report

After tests complete, open:
```
appium_physical_device_tests\reports\Physical_Device_E2E_Report_<timestamp>.xlsx
```

The report has **5 sheets**:

| Sheet | Contents |
|-------|----------|
| **Summary** | Overall stats + device info + category breakdown |
| **Passed Tests** | All tests that passed (green) |
| **Failed Tests** | All failed tests with error details (red) |
| **Execution Log** | Chronological log of every test run |
| **Test Details** | Full details including error messages |

---

## Folder Structure

```
crowdsense/
├── appium_physical_device_tests/    ← ALL physical device tests live here
│   ├── conftest.py                  ← USB device auto-detection + driver setup
│   ├── test_01_auth.py              ← PM001-PM022: Login, Register, Forgot Password
│   ├── test_02_home_navigation.py   ← PM023-PM040: Home screen, nav bar, tabs
│   ├── test_03_search_place.py      ← PM041-PM060: Search, Place Details, Crowd Report
│   ├── test_04_profile_settings.py  ← PM061-PM078: Profile, Settings screens
│   ├── test_05_travel_planner.py    ← PM079-PM090: Travel Planner, Favorites
│   ├── test_06_smoke.py             ← PM091-PM100: Critical path smoke tests
│   ├── pytest.ini                   ← Test configuration
│   ├── requirements.txt             ← Python dependencies
│   └── reports/                     ← Excel reports saved here (auto-created)
│
├── run_physical_tests.bat           ← ONE-CLICK runner for physical device
│
└── appium_tests/                    ← Original emulator tests (unchanged)
    └── run_appium_tests.bat         ← Emulator runner (unchanged)
```

---

## Key Differences: Physical Device vs Emulator

| Feature | Emulator Tests (`appium_tests/`) | Physical Device Tests (`appium_physical_device_tests/`) |
|---------|-----------------------------------|----------------------------------------------------------|
| **Device** | Android emulator (Pixel 3a AVD) | Real phone via USB cable |
| **ADB serial** | `emulator-5554` | Auto-detected (e.g. `RZ8N90XXXXX`) |
| **AVD launch** | Appium launches emulator | No emulator — phone already on |
| **Test IDs** | AM001–AM100 | PM001–PM100 |
| **Timeouts** | 10–12s per wait | 12–15s (real device latency) |
| **App restart** | 3s cold start | 5s cold start |
| **Report name** | `Appium_E2E_Report_*.xlsx` | `Physical_Device_E2E_Report_*.xlsx` |

---

## Troubleshooting

### "No USB device detected"
- Check cable: must be a **data cable**, not charge-only
- On phone: accept the "Allow USB Debugging?" popup
- Try: `adb devices` — should show your device
- Try: unplug and re-plug the USB cable

### "APK not found"
- Run: `cd frontend && flutter build apk --debug`
- Or let `run_physical_tests.bat` build it automatically

### "Appium connection refused"
- Start Appium manually: `npx appium` (in a separate terminal)
- Wait for: `"Appium REST http interface listener started on 0.0.0.0:4723"`

### "App install failed"
- Make sure **USB Debugging is ON** on your phone
- Try: `adb install frontend\build\app\outputs\flutter-apk\app-debug.apk`

### "Element not found" failures
- These usually mean a screen took longer to load on your device
- Real devices vary — increase `timeout` in `pytest.ini` if needed

### Set a specific device (if you have multiple phones connected)
```bat
set ANDROID_DEVICE_ID=YOUR_DEVICE_SERIAL
run_physical_tests.bat
```

### Change test credentials
```bat
set CROWDSENSE_EMAIL=your@email.com
set CROWDSENSE_PASSWORD=YourPassword
run_physical_tests.bat
```

---

## Quick Start Checklist

- [ ] Node.js installed (`node --version`)
- [ ] Appium installed (`appium --version`)  
- [ ] UiAutomator2 driver installed (`appium driver list --installed`)
- [ ] Python dependencies installed (`pip install -r requirements.txt`)
- [ ] ADB working (`adb version`)
- [ ] USB Debugging enabled on phone
- [ ] Phone connected via USB data cable
- [ ] Phone shows "device" in `adb devices` (not "unauthorized")
- [ ] APK built (`flutter build apk --debug`)
- [ ] Appium server running (`npx appium`)
- ✅ Run: `run_physical_tests.bat`

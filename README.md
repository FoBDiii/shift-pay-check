# Shift Pay Check

Android app for checking you've been paid correctly for every shift: clock in and out, log breaks, see when an automatic break needs removing, compare against your payslip, and send a weekly report to your manager or HR.

## Get the APK

Every push to `main` builds a new APK automatically.

1. Open the **Releases** section of this repository on your phone.
2. Download the latest `ShiftPayCheck-1.0.N.apk`.
3. Open it. The first time, Android asks you to allow installs from your browser or Files app.

New versions install over the old one and keep your shifts, because every build is signed with the same key (`app/signing.keystore`). That key is for this personal sideloaded app only; don't reuse it for anything published on Google Play.

## How it's built

- `web/shift-pay-check.html` is the app itself (the same page as the Claude artifact).
- `tools/build_web.py` turns it into `app/src/main/assets/index.html`, swapping online fonts and libraries for the bundled copies so the app works fully offline.
- `MainActivity.java` shows the page in a WebView and adds what a web page can't do on its own: storing data on the phone, saving PDFs and backups to `Downloads/Shift Pay Check`, the share sheet, and an ongoing notification while you're clocked in.
- `.github/workflows/build.yml` builds the APK and publishes it as a release.

## Updating the app

Edit `web/shift-pay-check.html`, commit, and push to `main`. The workflow rebuilds the APK.

## Data

Shifts are stored only on the phone. Use **Settings → Export backup** regularly, and **Import backup** to move data to a new phone or from the web version.

Bundled third-party files: jsPDF and jsPDF-AutoTable (MIT), and Bricolage Grotesque, Atkinson Hyperlegible and JetBrains Mono fonts (SIL Open Font License). Licence texts are in `app/src/main/assets/lib` and `app/src/main/assets/fonts`.

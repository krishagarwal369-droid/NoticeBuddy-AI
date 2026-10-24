# NoticeBuddy AI — Android App

This Android project opens the existing hosted NoticeBuddy AI website inside an Android WebView. The existing Streamlit server and AI features stay hosted at the same URL; API keys remain server-side.

## Included
- App shell and custom icon.
- JavaScript, DOM storage, and cookies for the Streamlit UI.
- Android file picker for notice/document uploads.
- Downloads through Android Download Manager.
- Back navigation through website history.
- Microphone permission is requested only when the website asks for voice capture.
- Branded loading and offline/retry screens.
- HTTPS-only network access; unrelated external links open in the phone browser.

## Build an APK
1. Install Android Studio and Android SDK Platform 35.
2. Open the android-app folder in Android Studio.
3. Use JDK 17 and allow Gradle sync.
4. Select Build → Build Bundle(s) / APK(s) → Build APK(s).
5. The APK appears at app/build/outputs/apk/debug/app-debug.apk.

An internet connection is required because this is an app wrapper, not an offline native rewrite. For Play Store release, create a signed release build and meet the current Play Console requirements.

package com.noticebuddy.ai

import android.Manifest
import android.app.Activity
import android.app.DownloadManager
import android.content.ActivityNotFoundException
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Color
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.os.Environment
import android.view.Gravity
import android.view.View
import android.view.ViewGroup
import android.webkit.CookieManager
import android.webkit.DownloadListener
import android.webkit.PermissionRequest
import android.webkit.ValueCallback
import android.webkit.WebChromeClient
import android.webkit.WebResourceError
import android.webkit.WebResourceRequest
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.Button
import android.widget.FrameLayout
import android.widget.LinearLayout
import android.widget.ProgressBar
import android.widget.TextView
import android.widget.Toast
import java.net.URI

class MainActivity : Activity() {
    private lateinit var webView: WebView
    private lateinit var loadingView: LinearLayout
    private lateinit var offlineView: LinearLayout
    private var fileCallback: ValueCallback<Array<Uri>>? = null
    private var pendingPermission: PermissionRequest? = null

    private val appUrl = "https://noticebuddy-ai-vfarf7vbc9r2mywkqfdt57.streamlit.app/"
    private val appHost = URI(appUrl).host
    private val filePickerRequest = 4102
    private val microphoneRequest = 4103

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        window.statusBarColor = Color.rgb(7, 11, 24)
        window.navigationBarColor = Color.rgb(7, 11, 24)
        buildUi()
        configureWebView()
        if (savedInstanceState != null) {
            webView.restoreState(savedInstanceState)
            setLoading(false)
        } else {
            loadSite()
        }
    }

    private fun buildUi() {
        val root = FrameLayout(this).apply { setBackgroundColor(Color.rgb(7, 11, 24)) }
        webView = WebView(this).apply {
            setBackgroundColor(Color.rgb(7, 11, 24))
            layoutParams = FrameLayout.LayoutParams(-1, -1)
        }
        root.addView(webView)

        loadingView = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER
            setBackgroundColor(Color.rgb(7, 11, 24))
            addView(ProgressBar(this@MainActivity).apply {
                indeterminateTintList = android.content.res.ColorStateList.valueOf(Color.rgb(69, 226, 245))
            }, LinearLayout.LayoutParams(dp(42), dp(42)))
            addView(TextView(this@MainActivity).apply {
                text = "NOTICEBUDDY AI"
                setTextColor(Color.rgb(235, 241, 255))
                textSize = 18f
                typeface = Typeface.create("sans-serif-medium", Typeface.BOLD)
                letterSpacing = 0.12f
                gravity = Gravity.CENTER
                setPadding(0, dp(20), 0, dp(6))
            })
            addView(TextView(this@MainActivity).apply {
                text = "Turning notices into action"
                setTextColor(Color.rgb(155, 169, 202))
                textSize = 13f
                gravity = Gravity.CENTER
            })
        }
        root.addView(loadingView, FrameLayout.LayoutParams(-1, -1))

        offlineView = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER
            setPadding(dp(28), dp(24), dp(28), dp(24))
            setBackgroundColor(Color.rgb(7, 11, 24))
            visibility = View.GONE
            addView(TextView(this@MainActivity).apply {
                text = "You're offline"
                setTextColor(Color.WHITE)
                textSize = 24f
                typeface = Typeface.create("sans-serif-medium", Typeface.BOLD)
                gravity = Gravity.CENTER
            })
            addView(TextView(this@MainActivity).apply {
                text = "NoticeBuddy needs internet to load your notices and AI tools. Check your connection, then try again."
                setTextColor(Color.rgb(169, 181, 211))
                textSize = 14f
                gravity = Gravity.CENTER
                setPadding(0, dp(12), 0, dp(22))
            })
            addView(Button(this@MainActivity).apply {
                text = "Try again"
                isAllCaps = false
                setTextColor(Color.WHITE)
                background = GradientDrawable(
                    GradientDrawable.Orientation.LEFT_RIGHT,
                    intArrayOf(Color.rgb(105, 83, 255), Color.rgb(37, 198, 225))
                ).apply { cornerRadius = dp(14).toFloat() }
                setPadding(dp(26), dp(10), dp(26), dp(10))
                setOnClickListener { loadSite() }
            })
        }
        root.addView(offlineView, FrameLayout.LayoutParams(-1, -1))
        setContentView(root)
    }

    @Suppress("SetJavaScriptEnabled")
    private fun configureWebView() {
        val settings = webView.settings
        settings.javaScriptEnabled = true
        settings.domStorageEnabled = true
        settings.databaseEnabled = true
        settings.loadsImagesAutomatically = true
        settings.javaScriptCanOpenWindowsAutomatically = true
        settings.setSupportMultipleWindows(false)
        settings.cacheMode = WebSettings.LOAD_DEFAULT
        settings.mediaPlaybackRequiresUserGesture = false
        settings.allowContentAccess = true
        settings.allowFileAccess = false
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) settings.safeBrowsingEnabled = true

        CookieManager.getInstance().setAcceptCookie(true)
        CookieManager.getInstance().setAcceptThirdPartyCookies(webView, true)

        webView.webViewClient = object : WebViewClient() {
            override fun onPageStarted(view: WebView?, url: String?, favicon: android.graphics.Bitmap?) {
                setLoading(true)
                offlineView.visibility = View.GONE
            }
            override fun onPageFinished(view: WebView?, url: String?) {
                setLoading(false)
                offlineView.visibility = View.GONE
            }
            override fun shouldOverrideUrlLoading(view: WebView, request: WebResourceRequest): Boolean =
                routeUrl(request.url)
            @Suppress("DEPRECATION")
            override fun shouldOverrideUrlLoading(view: WebView, url: String): Boolean =
                routeUrl(Uri.parse(url))
            override fun onReceivedError(view: WebView?, request: WebResourceRequest?, error: WebResourceError?) {
                super.onReceivedError(view, request, error)
                if (request?.isForMainFrame == true) {
                    setLoading(false)
                    offlineView.visibility = View.VISIBLE
                }
            }
        }

        webView.webChromeClient = object : WebChromeClient() {
            override fun onProgressChanged(view: WebView?, newProgress: Int) {
                if (newProgress >= 100) setLoading(false)
            }
            override fun onShowFileChooser(
                view: WebView?,
                callback: ValueCallback<Array<Uri>>?,
                params: FileChooserParams?
            ): Boolean {
                fileCallback?.onReceiveValue(null)
                fileCallback = callback
                return try {
                    val intent = params?.createIntent() ?: Intent(Intent.ACTION_OPEN_DOCUMENT).apply {
                        addCategory(Intent.CATEGORY_OPENABLE)
                        type = "*/*"
                    }
                    startActivityForResult(intent, filePickerRequest)
                    true
                } catch (_: ActivityNotFoundException) {
                    fileCallback = null
                    Toast.makeText(this@MainActivity, "No file picker available.", Toast.LENGTH_LONG).show()
                    false
                }
            }
            override fun onPermissionRequest(request: PermissionRequest) {
                runOnUiThread {
                    val requested = request.resources.toList()
                    val audioOnly = requested.contains(PermissionRequest.RESOURCE_AUDIO_CAPTURE) &&
                        requested.all { it == PermissionRequest.RESOURCE_AUDIO_CAPTURE }
                    if (!audioOnly) {
                        request.deny()
                    } else if (Build.VERSION.SDK_INT < Build.VERSION_CODES.M ||
                        checkSelfPermission(Manifest.permission.RECORD_AUDIO) == PackageManager.PERMISSION_GRANTED) {
                        request.grant(requested.toTypedArray())
                    } else {
                        pendingPermission = request
                        requestPermissions(arrayOf(Manifest.permission.RECORD_AUDIO), microphoneRequest)
                    }
                }
            }
            override fun onPermissionRequestCanceled(request: PermissionRequest) {
                if (pendingPermission == request) pendingPermission = null
            }
        }

        webView.setDownloadListener(DownloadListener { url, userAgent, disposition, mimeType, _ ->
            try {
                val name = disposition?.substringAfter("filename=", "")?.trim()?.trim('"')
                    ?.substringAfterLast('/')?.takeIf { it.isNotBlank() }
                    ?: if (mimeType == "application/pdf") "noticebuddy-document.pdf" else "noticebuddy-download"
                val req = DownloadManager.Request(Uri.parse(url)).apply {
                    setMimeType(mimeType)
                    addRequestHeader("User-Agent", userAgent)
                    CookieManager.getInstance().getCookie(url)?.let { addRequestHeader("Cookie", it) }
                    setTitle(name)
                    setDescription("Downloading document")
                    setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED)
                    setDestinationInExternalPublicDir(Environment.DIRECTORY_DOWNLOADS, name.replace(Regex("[^A-Za-z0-9._ -]"), "_"))
                    setAllowedOverMetered(true)
                    setAllowedOverRoaming(false)
                }
                (getSystemService(Context.DOWNLOAD_SERVICE) as DownloadManager).enqueue(req)
                Toast.makeText(this, "Download started", Toast.LENGTH_SHORT).show()
            } catch (_: Exception) {
                openExternal(Uri.parse(url))
            }
        })
    }

    private fun routeUrl(uri: Uri): Boolean {
        val scheme = uri.scheme?.lowercase()
        if (scheme == "https" || scheme == "http") {
            if (uri.host?.lowercase() == appHost) return false
            openExternal(uri)
            return true
        }
        if (scheme == "about" || scheme == "blob" || scheme == "data") return false
        openExternal(uri)
        return true
    }

    private fun openExternal(uri: Uri) {
        try {
            startActivity(Intent(Intent.ACTION_VIEW, uri))
        } catch (_: ActivityNotFoundException) {
            Toast.makeText(this, "No app can open this link.", Toast.LENGTH_SHORT).show()
        }
    }

    private fun loadSite() {
        offlineView.visibility = View.GONE
        setLoading(true)
        webView.loadUrl(appUrl)
    }

    private fun setLoading(show: Boolean) {
        if (::loadingView.isInitialized) loadingView.visibility = if (show) View.VISIBLE else View.GONE
    }

    @Suppress("DEPRECATION")
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == filePickerRequest) {
            val callback = fileCallback ?: return
            callback.onReceiveValue(
                if (resultCode == Activity.RESULT_OK) WebChromeClient.FileChooserParams.parseResult(resultCode, data) else null
            )
            fileCallback = null
        }
    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == microphoneRequest) {
            val request = pendingPermission
            pendingPermission = null
            if (request != null) {
                if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    request.grant(arrayOf(PermissionRequest.RESOURCE_AUDIO_CAPTURE))
                } else {
                    request.deny()
                    Toast.makeText(this, "Microphone permission is needed for voice input.", Toast.LENGTH_LONG).show()
                }
            }
        }
    }

    override fun onSaveInstanceState(outState: Bundle) {
        webView.saveState(outState)
        super.onSaveInstanceState(outState)
    }

    @Suppress("DEPRECATION")
    override fun onBackPressed() {
        if (::webView.isInitialized && webView.canGoBack()) webView.goBack() else super.onBackPressed()
    }

    override fun onDestroy() {
        fileCallback?.onReceiveValue(null)
        fileCallback = null
        pendingPermission?.deny()
        pendingPermission = null
        if (::webView.isInitialized) {
            webView.stopLoading()
            webView.webChromeClient = null
            webView.destroy()
        }
        super.onDestroy()
    }

    private fun dp(value: Int): Int = (value * resources.displayMetrics.density).toInt()
}

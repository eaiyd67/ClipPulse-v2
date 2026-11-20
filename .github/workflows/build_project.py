#!/usr/bin/env python3
"""ClipPulse v2.0.0 Complete Android Project Generator."""
import os
import sys

PKG = "app/src/main/java/com/clippulse/studio"


def w(path: str, content: str) -> None:
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content.lstrip("\n"))
    print(f"Wrote: {path}")


def write_gradle_and_manifest() -> None:
    sdk = os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT")
    if sdk:
        w("local.properties", "sdk.dir=" + sdk.replace("\\", "\\\\") + "\n")

    w("gradle.properties", r'''
org.gradle.jvmargs=-Xmx4096m -Dfile.encoding=UTF-8
android.useAndroidX=true
kotlin.code.style=official
android.nonTransitiveRClass=true
''')

    w("settings.gradle.kts", r'''
pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
        maven { url = uri("https://jitpack.io") }
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
        maven { url = uri("https://jitpack.io") }
    }
}
rootProject.name = "ClipPulse"
include(":app")
''')

    w("build.gradle.kts", r'''
plugins {
    id("com.android.application") version "8.7.2" apply false
    id("org.jetbrains.kotlin.android") version "2.0.21" apply false
    id("org.jetbrains.kotlin.plugin.compose") version "2.0.21" apply false
}
''')

    w("app/proguard-rules.pro", "-keep class com.yausername.** { *; }\n-dontwarn com.yausername.**\n")

    w("app/build.gradle.kts", r'''
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("org.jetbrains.kotlin.plugin.compose")
}
android {
    namespace = "com.clippulse.studio"
    compileSdk = 35
    defaultConfig {
        applicationId = "com.clippulse.studio"
        minSdk = 26
        targetSdk = 35
        versionCode = 4
        versionName = "2.0.0"
        ndk { abiFilters += listOf("arm64-v8a", "armeabi-v7a", "x86_64", "x86") }
    }
    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
        debug { isMinifyEnabled = false }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }
    buildFeatures { compose = true }
    packaging {
        jniLibs { useLegacyPackaging = true }
        resources { excludes += "/META-INF/{AL2.0,LGPL2.1}" }
    }
    lint {
        abortOnError = false
        checkReleaseBuilds = false
    }
}
dependencies {
    val composeBom = platform("androidx.compose:compose-bom:2024.10.01")
    implementation(composeBom)
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.material:material-icons-extended")
    debugImplementation("androidx.compose.ui:ui-tooling")
    implementation("androidx.activity:activity-compose:1.9.3")
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.8.7")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.8.7")
    implementation("androidx.lifecycle:lifecycle-runtime-compose:2.8.7")
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.9.0")
    implementation("com.squareup.okhttp3:okhttp:4.12.0")
    implementation("androidx.media3:media3-exoplayer:1.4.1")
    implementation("androidx.media3:media3-ui:1.4.1")
    implementation("androidx.media3:media3-datasource:1.4.1")
    implementation("io.github.junkfood02.youtubedl-android:library:0.18.1")
    implementation("io.github.junkfood02.youtubedl-android:ffmpeg:0.18.1")
    implementation("io.github.junkfood02.youtubedl-android:common:0.18.1")
}
''')

    w("app/src/main/AndroidManifest.xml", r'''
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE_DATA_SYNC" />
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
    <uses-permission android:name="android.permission.READ_MEDIA_VIDEO" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" android:maxSdkVersion="32" tools:node="replace" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" android:maxSdkVersion="29" tools:node="replace" />
    <application
        android:name=".ClipPulseApp"
        android:allowBackup="true"
        android:extractNativeLibs="true"
        android:icon="@drawable/ic_launcher"
        android:label="@string/app_name"
        android:requestLegacyExternalStorage="true"
        android:roundIcon="@drawable/ic_launcher"
        android:supportsRtl="true"
        android:theme="@style/Theme.ClipPulse"
        android:usesCleartextTraffic="true"
        tools:replace="android:extractNativeLibs">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:launchMode="singleTop"
            android:windowSoftInputMode="adjustResize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
            <intent-filter>
                <action android:name="android.intent.action.SEND" />
                <category android:name="android.intent.category.DEFAULT" />
                <data android:mimeType="text/plain" />
            </intent-filter>
        </activity>
        <service
            android:name=".service.ClipExportService"
            android:exported="false"
            android:foregroundServiceType="dataSync" />
        <provider
            android:name="androidx.core.content.FileProvider"
            android:authorities="${applicationId}.fileprovider"
            android:exported="false"
            android:grantUriPermissions="true">
            <meta-data
                android:name="android.support.FILE_PROVIDER_PATHS"
                android:resource="@xml/file_paths" />
        </provider>
    </application>
</manifest>
''')

    w("app/src/main/res/xml/file_paths.xml", r'''
<?xml version="1.0" encoding="utf-8"?>
<paths>
    <external-path name="external_files" path="." />
    <cache-path name="cache_files" path="." />
</paths>
''')

    w("app/src/main/res/drawable/ic_launcher.xml", r'''
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp" android:height="108dp" android:viewportWidth="108" android:viewportHeight="108">
    <path android:fillColor="#0B0B0F" android:pathData="M0,0h108v108h-108z" />
    <path android:fillColor="#16161D" android:pathData="M24,18h60c3.31,0 6,2.69 6,6v60c0,3.31 -2.69,6 -6,6h-60c-3.31,0 -6,-2.69 -6,-6v-60c0,-3.31 2.69,-6 6,-6z" />
    <path android:fillColor="#6366F1" android:pathData="M22,52h11l6,-18l8,36l8,-28l6,16l5,-6h20v6h-17l-9,11l-7,-18l-8,28l-8,-35l-4,14h-11z" />
    <path android:fillColor="#F59E0B" android:pathData="M78,24l2.2,4.8l5.3,0.6l-3.9,3.6l1.1,5.2l-4.7,-2.6l-4.7,2.6l1.1,-5.2l-3.9,-3.6l5.3,-0.6z" />
</vector>
''')
    w("app/src/main/res/values/strings.xml", '<?xml version="1.0" encoding="utf-8"?>\n<resources><string name="app_name">ClipPulse</string></resources>\n')
    w("app/src/main/res/values/themes.xml", '<?xml version="1.0" encoding="utf-8"?>\n<resources><style name="Theme.ClipPulse" parent="android:Theme.Material.NoActionBar"><item name="android:statusBarColor">#0B0B0F</item><item name="android:navigationBarColor">#0B0B0F</item><item name="android:windowBackground">#0B0B0F</item></style></resources>\n')


def write_core_kotlin() -> None:
    w(f"{PKG}/ClipPulseApp.kt", r'''
package com.clippulse.studio

import android.app.Application
import android.app.NotificationChannel
import android.app.NotificationManager
import android.os.Build
import com.clippulse.studio.engine.EngineInitializer
import com.clippulse.studio.service.ClipExportService
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.launch

class ClipPulseApp : Application() {
    private val appScope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
    override fun onCreate() {
        super.onCreate()
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val ch = NotificationChannel(ClipExportService.CHANNEL_ID, "ClipPulse Exports", NotificationManager.IMPORTANCE_LOW)
            getSystemService(NotificationManager::class.java)?.createNotificationChannel(ch)
        }
        appScope.launch {
            EngineInitializer.ensureInitialized(this@ClipPulseApp)
            // Automatically refresh yt-dlp binary once per day to prevent YouTube 403/SABR blocks
            EngineInitializer.autoUpdateIfStale(this@ClipPulseApp)
        }
    }
}
''')

    w(f"{PKG}/MainActivity.kt", r'''
package com.clippulse.studio

import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.SystemBarStyle
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import com.clippulse.studio.engine.UrlNormalizer
import com.clippulse.studio.ui.ClipPulseStudioScreen
import com.clippulse.studio.ui.theme.ClipPulseTheme
import com.clippulse.studio.viewmodel.ClipPulseViewModel

class MainActivity : ComponentActivity() {
    private val viewModel: ClipPulseViewModel by viewModels()
    override fun onCreate(savedInstanceState: Bundle?) {
        enableEdgeToEdge(
            statusBarStyle = SystemBarStyle.dark(android.graphics.Color.parseColor("#0B0B0F")),
            navigationBarStyle = SystemBarStyle.dark(android.graphics.Color.parseColor("#0B0B0F"))
        )
        super.onCreate(savedInstanceState)
        handleIntent(intent)
        setContent { ClipPulseTheme { ClipPulseStudioScreen(viewModel = viewModel) } }
    }
    override fun onNewIntent(intent: Intent) {
        super.onNewIntent(intent)
        setIntent(intent)
        handleIntent(intent)
    }
    private fun handleIntent(incoming: Intent?) {
        if (incoming?.action == Intent.ACTION_SEND && incoming.type == "text/plain") {
            val raw = incoming.getStringExtra(Intent.EXTRA_TEXT).orEmpty()
            val cleanUrl = UrlNormalizer.extractAndNormalize(raw)
            if (cleanUrl.isNotBlank()) viewModel.onSharedUrlReceived(cleanUrl)
        }
    }
}
''')

    w(f"{PKG}/model/ClipModels.kt", r'''
package com.clippulse.studio.model

import androidx.compose.ui.graphics.Color
import com.clippulse.studio.ui.theme.*
import java.util.Locale

enum class StudioTab(val label: String) {
    STUDIO("Clip Studio"),
    DOWNLOADS("Downloads")
}

enum class AiPreset(val displayName: String, val defaultBaseUrl: String, val defaultModel: String) {
    DEEPSEEK("DeepSeek", "https://api.deepseek.com/v1", "deepseek-chat"),
    GEMINI("Gemini", "https://generativelanguage.googleapis.com/v1beta/openai", "gemini-2.5-flash"),
    OPENROUTER("OpenRouter", "https://openrouter.ai/api/v1", "google/gemini-2.5-flash"),
    CUSTOM("Custom", "https://api.openai.com/v1", "gpt-4o-mini")
}

data class AiConfig(
    val preset: AiPreset = AiPreset.DEEPSEEK,
    val baseUrl: String = AiPreset.DEEPSEEK.defaultBaseUrl,
    val primaryKey: String = "",
    val backupKeys: List<String> = emptyList(),
    val selectedModel: String = AiPreset.DEEPSEEK.defaultModel,
    val availableModels: List<String> = listOf("deepseek-chat", "deepseek-reasoner", "gemini-2.5-flash", "gemini-2.5-pro", "google/gemini-2.5-flash", "gpt-4o-mini"),
    val smartPeakOnly: Boolean = true,
    val offlineNoAiMode: Boolean = false
) {
    fun orderedKeys(): List<String> = (listOf(primaryKey.trim()) + backupKeys.map { it.trim() }).filter { it.isNotBlank() }.distinct()
    fun canUseAi(): Boolean = !offlineNoAiMode && orderedKeys().isNotEmpty() && baseUrl.isNotBlank()
}

sealed class AiConnectionState {
    data object Idle : AiConnectionState()
    data object Testing : AiConnectionState()
    data class Connected(val latencyMs: Long, val model: String) : AiConnectionState()
    data class Error(val message: String) : AiConnectionState()
}

enum class DetectionMode(val label: String) {
    SMART_ALL("All Signals"), HEATMAP("Most Replayed"), SUPER_CHAT("Super Chats"),
    CHAT_HYPE("Chat Hype"), AUDIO_PEAKS("Audio Peaks"), AI_CUSTOM("AI Custom Prompt")
}

enum class SignalSource(val label: String, val badgeColor: Color) {
    SUPER_CHAT("Super Chat", ColorGold), HEATMAP("Heatmap", ColorCrimson),
    CHAT_HYPE("Chat Hype", ColorPurple), AI_PICK("AI Pick", ColorCyan),
    TRANSCRIPT_HOOK("Transcript Hook", ElectricIndigoLight), AUDIO_PEAK("Audio Peak", ColorEmerald)
}

enum class SuperChatThreshold(val label: String, val minUsd: Double) {
    ALL("All", 0.0), PLUS_5("$5+", 5.0), PLUS_10("$10+", 10.0), PLUS_25("$25+", 25.0)
}

enum class PaddingPreset(val label: String, val beforeSec: Double, val afterSec: Double) {
    TIGHT("-2s / +3s", 2.0, 3.0), BALANCED("-3s / +5s", 3.0, 5.0),
    WIDE("-5s / +8s", 5.0, 8.0), CONTEXT("-8s / +12s", 8.0, 12.0)
}

data class HeatmapPoint(val startSec: Double, val endSec: Double, val value: Double)
data class SuperChatEvent(val donor: String, val amountDisplay: String, val usdApprox: Double, val currency: String, val message: String, val offsetSec: Double)
data class TranscriptCue(val startSec: Double, val endSec: Double, val text: String)

data class ClipCandidate(
    val id: String, val title: String, val startSec: Double, val endSec: Double,
    val hypeScore: Int, val signals: List<SignalSource>, val isMultiSignal: Boolean,
    val superChat: SuperChatEvent? = null, val transcriptQuote: String = "",
    val reason: String = "", val viralTitle: String = "",
    val socialCaption: String = "", val hashtags: String = "#shorts #viral #clips",
    val selected: Boolean = true
) {
    val durationSec: Double get() = (endSec - startSec).coerceAtLeast(1.0)
    fun formattedSocialCopy(): String = buildString {
        appendLine(viralTitle.ifBlank { title })
        if (socialCaption.isNotBlank()) appendLine(socialCaption)
        append(hashtags.ifBlank { "#shorts #viral #clips" })
    }.trim()
}

data class VideoAnalysisResult(
    val sourceUrlOrUri: String, val isLocalFile: Boolean, val localFilePath: String?,
    val videoTitle: String, val channelName: String, val durationSec: Double,
    val heatmap: List<HeatmapPoint>, val clips: List<ClipCandidate>,
    val hasLiveChat: Boolean, val hasTranscript: Boolean, val analysisSummary: String,
    val scannedAtMillis: Long = System.currentTimeMillis()
)

enum class ExportMode(val label: String) { FAST_COPY("Fast Cut"), VERTICAL_CROP("9:16 Crop") }

enum class DownloadQuality(val label: String, val formatSelector: String) {
    Q_1080P("1080p HD", "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/b[height<=1080][ext=mp4]/bv*[height<=1080]+ba/b[height<=1080]/best"),
    Q_720P("720p HD", "bv*[height<=720][ext=mp4]+ba[ext=m4a]/b[height<=720][ext=mp4]/bv*[height<=720]+ba/b[height<=720]/best"),
    Q_480P("480p Saver", "bv*[height<=480][ext=mp4]+ba[ext=m4a]/b[height<=480][ext=mp4]/bv*[height<=480]+ba/b[height<=480]/best"),
    Q_BEST("Best Max", "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/bv*+ba/best")
}

data class ExportedClipRecord(
    val id: String, val title: String, val displayPath: String, val contentUriString: String,
    val durationSec: Double, val sizeBytes: Long, val qualityLabel: String,
    val modeLabel: String, val audioLeveled: Boolean, val exportedAtMillis: Long
)

sealed class ExportJobState {
    data object Idle : ExportJobState()
    data class Running(val currentIndex: Int, val total: Int, val currentTitle: String, val progressFraction: Float) : ExportJobState()
    data class Completed(val exportedCount: Int, val savedLocations: List<String>) : ExportJobState()
    data class Failed(val error: String) : ExportJobState()
}

object TimeFormatter {
    fun formatTimestamp(totalSeconds: Double): String {
        val s = totalSeconds.coerceAtLeast(0.0).toLong()
        val h = s / 3600L; val m = (s % 3600L) / 60L; val sec = s % 60L
        return if (h > 0L) String.format(Locale.US, "%02d:%02d:%02d", h, m, sec) else String.format(Locale.US, "%02d:%02d", m, sec)
    }
    fun formatFfmpegDuration(totalSeconds: Double): String {
        val c = totalSeconds.coerceAtLeast(0.0)
        return String.format(Locale.US, "%02d:%02d:%05.2f", (c / 3600.0).toInt(), ((c % 3600.0) / 60.0).toInt(), c % 60.0)
    }
    fun formatSectionTimestamp(totalSeconds: Double): String {
        val s = totalSeconds.coerceAtLeast(0.0).toLong()
        return String.format(Locale.US, "%02d:%02d:%02d", s / 3600L, (s % 3600L) / 60L, s % 60L)
    }
    fun parseTimestampToSec(raw: String): Double? {
        val parts = raw.trim().split(":").map { it.trim().toDoubleOrNull() ?: return null }
        return when (parts.size) {
            1 -> parts[0]
            2 -> parts[0] * 60.0 + parts[1]
            3 -> parts[0] * 3600.0 + parts[1] * 60.0 + parts[2]
            else -> null
        }
    }
    fun formatFileSize(bytes: Long): String {
        if (bytes <= 0L) return "MP4"
        return String.format(Locale.US, "%.1f MB", bytes.toDouble() / (1024.0 * 1024.0))
    }
}
''')

    w(f"{PKG}/data/AiConfigStore.kt", r'''
package com.clippulse.studio.data

import android.content.Context
import com.clippulse.studio.model.*
import org.json.JSONArray
import org.json.JSONObject
import java.io.File

data class DownloadSettings(
    val quality: DownloadQuality = DownloadQuality.Q_1080P,
    val exportMode: ExportMode = ExportMode.FAST_COPY,
    val burnSuperChatOverlay: Boolean = true,
    val loudnormEnabled: Boolean = true,
    val includeTxtNotes: Boolean = true
)

class AiConfigStore(context: Context) {
    private val appCtx = context.applicationContext
    private val prefs = appCtx.getSharedPreferences("clippulse_ai_prefs", Context.MODE_PRIVATE)

    fun load(): AiConfig {
        val preset = runCatching { AiPreset.valueOf(prefs.getString("preset", AiPreset.DEEPSEEK.name)!!) }.getOrDefault(AiPreset.DEEPSEEK)
        val savedModels = decodeList(prefs.getString("models", "[]") ?: "[]")
        return AiConfig(
            preset = preset,
            baseUrl = normalizeBaseUrl(prefs.getString("base_url", preset.defaultBaseUrl) ?: preset.defaultBaseUrl),
            primaryKey = prefs.getString("primary_key", "") ?: "",
            backupKeys = decodeList(prefs.getString("backup_keys", "[]") ?: "[]"),
            selectedModel = prefs.getString("selected_model", preset.defaultModel) ?: preset.defaultModel,
            availableModels = if (savedModels.isNotEmpty()) savedModels else AiConfig().availableModels,
            smartPeakOnly = prefs.getBoolean("smart_peak", true),
            offlineNoAiMode = prefs.getBoolean("offline_mode", false)
        )
    }

    fun save(c: AiConfig) {
        prefs.edit()
            .putString("preset", c.preset.name)
            .putString("base_url", normalizeBaseUrl(c.baseUrl))
            .putString("primary_key", c.primaryKey.trim())
            .putString("backup_keys", encodeList(c.backupKeys.filter { it.isNotBlank() }))
            .putString("selected_model", c.selectedModel.trim())
            .putString("models", encodeList(c.availableModels))
            .putBoolean("smart_peak", c.smartPeakOnly)
            .putBoolean("offline_mode", c.offlineNoAiMode)
            .apply()
    }

    // Persistent Cookies.txt Login Support
    fun getCookiesFile(): File? {
        val f = File(appCtx.filesDir, "yt_cookies.txt")
        return if (f.exists() && f.length() > 10L) f else null
    }

    fun saveCookiesText(rawCookies: String): Boolean {
        val clean = rawCookies.trim()
        if (clean.isEmpty()) return false
        File(appCtx.filesDir, "yt_cookies.txt").writeText(clean, Charsets.UTF_8)
        return true
    }

    fun clearCookies() {
        runCatching { File(appCtx.filesDir, "yt_cookies.txt").delete() }
    }

    fun loadDownloadSettings(): DownloadSettings {
        val q = runCatching { DownloadQuality.valueOf(prefs.getString("dl_quality", DownloadQuality.Q_1080P.name)!!) }.getOrDefault(DownloadQuality.Q_1080P)
        val m = runCatching { ExportMode.valueOf(prefs.getString("dl_mode", ExportMode.FAST_COPY.name)!!) }.getOrDefault(ExportMode.FAST_COPY)
        return DownloadSettings(
            quality = q,
            exportMode = m,
            burnSuperChatOverlay = prefs.getBoolean("dl_sc_overlay", true),
            loudnormEnabled = prefs.getBoolean("dl_loudnorm", true),
            includeTxtNotes = prefs.getBoolean("dl_txt", true)
        )
    }

    fun saveDownloadSettings(s: DownloadSettings) {
        prefs.edit()
            .putString("dl_quality", s.quality.name)
            .putString("dl_mode", s.exportMode.name)
            .putBoolean("dl_sc_overlay", s.burnSuperChatOverlay)
            .putBoolean("dl_loudnorm", s.loudnormEnabled)
            .putBoolean("dl_txt", s.includeTxtNotes)
            .apply()
    }

    // Persistent Scan History Cache
    fun saveScanToHistory(res: VideoAnalysisResult) {
        val existing = loadScanHistory().filterNot { it.sourceUrlOrUri == res.sourceUrlOrUri }.toMutableList()
        existing.add(0, res)
        val trimmed = existing.take(20)
        val arr = JSONArray()
        trimmed.forEach { item ->
            arr.put(JSONObject().apply {
                put("url", item.sourceUrlOrUri); put("local", item.isLocalFile); put("path", item.localFilePath ?: "")
                put("title", item.videoTitle); put("channel", item.channelName); put("dur", item.durationSec)
                put("hasChat", item.hasLiveChat); put("hasSub", item.hasTranscript); put("summary", item.analysisSummary)
                put("scannedAt", item.scannedAtMillis)
                put("heatmap", JSONArray().apply {
                    item.heatmap.forEach { h -> put(JSONObject().put("s", h.startSec).put("e", h.endSec).put("v", h.value)) }
                })
                put("clips", JSONArray().apply {
                    item.clips.forEach { c ->
                        put(JSONObject().apply {
                            put("id", c.id); put("title", c.title); put("s", c.startSec); put("e", c.endSec)
                            put("score", c.hypeScore); put("multi", c.isMultiSignal); put("quote", c.transcriptQuote)
                            put("reason", c.reason); put("vTitle", c.viralTitle); put("cap", c.socialCaption)
                            put("tags", c.hashtags); put("sel", c.selected)
                            put("sigs", JSONArray().apply { c.signals.forEach { put(it.name) } })
                            c.superChat?.let { sc ->
                                put("sc", JSONObject().put("donor", sc.donor).put("amt", sc.amountDisplay)
                                    .put("usd", sc.usdApprox).put("cur", sc.currency).put("msg", sc.message).put("off", sc.offsetSec))
                            }
                        })
                    }
                })
            })
        }
        File(appCtx.filesDir, "scan_history.json").writeText(arr.toString(), Charsets.UTF_8)
    }

    fun loadScanHistory(): List<VideoAnalysisResult> = runCatching {
        val f = File(appCtx.filesDir, "scan_history.json")
        if (!f.exists()) return emptyList()
        val arr = JSONArray(f.readText(Charsets.UTF_8))
        (0 until arr.length()).mapNotNull { i ->
            val o = arr.optJSONObject(i) ?: return@mapNotNull null
            val hmArr = o.optJSONArray("heatmap") ?: JSONArray()
            val hm = (0 until hmArr.length()).mapNotNull { j ->
                val h = hmArr.optJSONObject(j) ?: return@mapNotNull null
                HeatmapPoint(h.optDouble("s"), h.optDouble("e"), h.optDouble("v"))
            }
            val cArr = o.optJSONArray("clips") ?: JSONArray()
            val clips = (0 until cArr.length()).mapNotNull { j ->
                val c = cArr.optJSONObject(j) ?: return@mapNotNull null
                val sArr = c.optJSONArray("sigs") ?: JSONArray()
                val sigs = (0 until sArr.length()).mapNotNull { k -> runCatching { SignalSource.valueOf(sArr.optString(k)) }.getOrNull() }
                val scObj = c.optJSONObject("sc")
                val sc = scObj?.let {
                    SuperChatEvent(it.optString("donor"), it.optString("amt"), it.optDouble("usd"), it.optString("cur"), it.optString("msg"), it.optDouble("off"))
                }
                ClipCandidate(
                    id = c.optString("id"), title = c.optString("title"), startSec = c.optDouble("s"), endSec = c.optDouble("e"),
                    hypeScore = c.optInt("score"), signals = sigs.ifEmpty { listOf(SignalSource.HEATMAP) },
                    isMultiSignal = c.optBoolean("multi"), superChat = sc, transcriptQuote = c.optString("quote"),
                    reason = c.optString("reason"), viralTitle = c.optString("vTitle"),
                    socialCaption = c.optString("cap"), hashtags = c.optString("tags", "#shorts #viral"),
                    selected = c.optBoolean("sel", true)
                )
            }
            VideoAnalysisResult(
                sourceUrlOrUri = o.optString("url"), isLocalFile = o.optBoolean("local"),
                localFilePath = o.optString("path").takeIf { it.isNotBlank() && File(it).exists() },
                videoTitle = o.optString("title"), channelName = o.optString("channel"),
                durationSec = o.optDouble("dur", 1.0), heatmap = hm, clips = clips,
                hasLiveChat = o.optBoolean("hasChat"), hasTranscript = o.optBoolean("hasSub"),
                analysisSummary = o.optString("summary"), scannedAtMillis = o.optLong("scannedAt")
            )
        }
    }.getOrDefault(emptyList())

    fun clearScanHistory() {
        runCatching { File(appCtx.filesDir, "scan_history.json").delete() }
    }

    fun loadDownloadHistory(): List<ExportedClipRecord> = runCatching {
        val arr = JSONArray(prefs.getString("dl_history", "[]") ?: "[]")
        (0 until arr.length()).mapNotNull { i ->
            val o = arr.optJSONObject(i) ?: return@mapNotNull null
            ExportedClipRecord(
                id = o.optString("id"), title = o.optString("title"), displayPath = o.optString("displayPath"),
                contentUriString = o.optString("contentUriString"), durationSec = o.optDouble("durationSec", 10.0),
                sizeBytes = o.optLong("sizeBytes", 0L), qualityLabel = o.optString("qualityLabel", "1080p HD"),
                modeLabel = o.optString("modeLabel", "Fast Cut"), audioLeveled = o.optBoolean("audioLeveled", true),
                exportedAtMillis = o.optLong("exportedAtMillis", 0L)
            )
        }
    }.getOrDefault(emptyList())

    fun appendDownloadRecord(record: ExportedClipRecord) {
        val current = loadDownloadHistory().toMutableList()
        current.add(0, record)
        saveDownloadHistory(current.take(60))
    }

    fun saveDownloadHistory(items: List<ExportedClipRecord>) {
        val arr = JSONArray()
        items.forEach { r ->
            arr.put(JSONObject().apply {
                put("id", r.id); put("title", r.title); put("displayPath", r.displayPath)
                put("contentUriString", r.contentUriString); put("durationSec", r.durationSec)
                put("sizeBytes", r.sizeBytes); put("qualityLabel", r.qualityLabel)
                put("modeLabel", r.modeLabel); put("audioLeveled", r.audioLeveled)
                put("exportedAtMillis", r.exportedAtMillis)
            })
        }
        prefs.edit().putString("dl_history", arr.toString()).apply()
    }

    private fun encodeList(items: List<String>) = JSONArray().apply { items.forEach { put(it) } }.toString()
    private fun decodeList(raw: String): List<String> = runCatching {
        val a = JSONArray(raw)
        (0 until a.length()).mapNotNull { a.optString(it).trim().takeIf { s -> s.isNotEmpty() } }
    }.getOrDefault(emptyList())

    companion object {
        fun normalizeBaseUrl(rawUrl: String): String {
            var cleaned = rawUrl.trim().trimEnd('/')
            for (suffix in listOf("/chat/completions", "/completions", "/models")) {
                if (cleaned.endsWith(suffix, ignoreCase = true)) cleaned = cleaned.dropLast(suffix.length).trimEnd('/')
            }
            return cleaned
        }
    }
}
''')

def write_network_and_engines() -> None:
    w(f"{PKG}/network/UniversalAiClient.kt", r'''
package com.clippulse.studio.network

import android.net.Uri
import android.os.SystemClock
import com.clippulse.studio.data.AiConfigStore
import com.clippulse.studio.model.*
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONArray
import org.json.JSONObject
import java.util.Locale
import java.util.concurrent.TimeUnit

data class AiClipSuggestion(
    val startSec: Double, val endSec: Double, val title: String, val score: Int,
    val reason: String, val viralTitle: String, val socialCaption: String, val hashtags: String
)

class UniversalAiClient {
    private val client = OkHttpClient.Builder().connectTimeout(20, TimeUnit.SECONDS).readTimeout(60, TimeUnit.SECONDS).build()
    private val jsonType = "application/json; charset=utf-8".toMediaType()

    suspend fun fetchModels(config: AiConfig): Result<List<String>> = withContext(Dispatchers.IO) {
        val base = AiConfigStore.normalizeBaseUrl(config.baseUrl)
        val keys = config.orderedKeys()
        if (base.isBlank()) return@withContext Result.failure(IllegalArgumentException("Base URL required."))
        if (keys.isEmpty()) return@withContext Result.failure(IllegalArgumentException("Enter an API key first."))
        executeWithFailover(base, keys) { key ->
            Request.Builder().url("$base/models").get()
                .addHeader("Authorization", "Bearer $key").addHeader("HTTP-Referer", "https://clippulse.app").addHeader("X-Title", "ClipPulse").build()
        }.mapCatching { body ->
            val arr = JSONObject(body).optJSONArray("data") ?: throw IllegalStateException("Missing 'data' array.")
            val list = (0 until arr.length()).mapNotNull { arr.optJSONObject(it)?.optString("id")?.trim()?.takeIf { s -> s.isNotEmpty() } }.distinct().sorted()
            if (list.isEmpty()) throw IllegalStateException("Provider returned 0 models.")
            list
        }
    }

    suspend fun testConnection(config: AiConfig): AiConnectionState = withContext(Dispatchers.IO) {
        val base = AiConfigStore.normalizeBaseUrl(config.baseUrl)
        val keys = config.orderedKeys()
        val model = config.selectedModel.trim().ifBlank { config.preset.defaultModel }
        if (base.isBlank()) return@withContext AiConnectionState.Error("Base URL required.")
        if (keys.isEmpty()) return@withContext AiConnectionState.Error("No API key configured.")
        val payload = JSONObject().put("model", model).put("max_tokens", 16).put("temperature", 0.0)
            .put("messages", JSONArray().put(JSONObject().put("role", "user").put("content", "OK"))).toString()
        val t0 = SystemClock.elapsedRealtime()
        val res = executeWithFailover(base, keys) { key ->
            Request.Builder().url("$base/chat/completions").post(payload.toRequestBody(jsonType))
                .addHeader("Authorization", "Bearer $key").addHeader("Content-Type", "application/json")
                .addHeader("HTTP-Referer", "https://clippulse.app").addHeader("X-Title", "ClipPulse").build()
        }
        val ms = (SystemClock.elapsedRealtime() - t0).coerceAtLeast(1L)
        res.fold(onSuccess = { AiConnectionState.Connected(ms, model) }, onFailure = { AiConnectionState.Error(it.message ?: "Failed") })
    }

    suspend fun findViralAndCustomClips(
        config: AiConfig, videoTitle: String, durationSec: Double,
        cues: List<TranscriptCue>, peakCentersSec: List<Double>, customPrompt: String
    ): List<AiClipSuggestion> = withContext(Dispatchers.IO) {
        if (!config.canUseAi() || cues.isEmpty()) return@withContext emptyList()
        val selectedCues = if (config.smartPeakOnly && peakCentersSec.isNotEmpty()) {
            cues.filter { c -> peakCentersSec.any { p -> c.endSec >= p - 60.0 && c.startSec <= p + 60.0 } }
        } else cues
        val sb = StringBuilder()
        for (c in selectedCues) {
            val line = "[${String.format(Locale.US, "%.1f", c.startSec)}] ${c.text}\n"
            if (sb.length + line.length > 14000) break
            sb.append(line)
        }
        if (sb.isEmpty()) return@withContext emptyList()
        val goal = if (customPrompt.isNotBlank()) "Find moments matching: \"${customPrompt.trim()}\"." else "Find top 4 to 8 viral hooks, funny moments, or heated reactions."
        val sys = """Return STRICT JSON ONLY, no markdown or think tags: {"clips":[{"start":12.0,"end":40.0,"title":"Short label","score":88,"reason":"Why","viralTitle":"Click-worthy Shorts/Reels hook title","caption":"1-sentence engaging description","hashtags":"#shorts #viral #trending"}]}"""
        val usr = "Title: $videoTitle | Duration: ${TimeFormatter.formatTimestamp(durationSec)}\nTask: $goal\nTranscript:\n$sb"
        val raw = completeChat(config, sys, usr, 1100) ?: return@withContext emptyList()
        val jsonStr = extractJsonObject(raw) ?: return@withContext emptyList()
        runCatching {
            val arr = JSONObject(jsonStr).optJSONArray("clips") ?: return@runCatching emptyList()
            (0 until arr.length()).mapNotNull { i ->
                val o = arr.optJSONObject(i) ?: return@mapNotNull null
                val s = o.optDouble("start", Double.NaN); val e = o.optDouble("end", Double.NaN)
                if (s.isNaN() || e.isNaN()) return@mapNotNull null
                val safeS = s.coerceIn(0.0, (durationSec - 3.0).coerceAtLeast(0.0))
                val safeE = e.coerceIn(safeS + 4.0, durationSec.coerceAtLeast(safeS + 4.0))
                val t = o.optString("title").ifBlank { "AI Highlight #${i + 1}" }
                AiClipSuggestion(
                    startSec = safeS, endSec = safeE, title = t,
                    score = o.optInt("score", 82).coerceIn(1, 100),
                    reason = o.optString("reason").ifBlank { "AI viral pick" },
                    viralTitle = o.optString("viralTitle").ifBlank { t },
                    socialCaption = o.optString("caption").trim(),
                    hashtags = o.optString("hashtags").ifBlank { "#shorts #viral #clips" }
                )
            }
        }.getOrDefault(emptyList())
    }

    suspend fun alignSuperChatReactions(
        config: AiConfig, superChats: List<SuperChatEvent>, cues: List<TranscriptCue>, durationSec: Double
    ): Map<Double, Pair<Double, Double>> = withContext(Dispatchers.IO) {
        if (!config.canUseAi() || superChats.isEmpty() || cues.isEmpty()) return@withContext emptyMap()
        val entries = buildString {
            superChats.sortedByDescending { it.usdApprox }.take(8).forEachIndexed { idx, sc ->
                val txt = cues.filter { it.endSec >= sc.offsetSec - 15.0 && it.startSec <= sc.offsetSec + 65.0 }
                    .joinToString(" ") { "[${String.format(Locale.US, "%.1f", it.startSec)}s] ${it.text}" }.take(700)
                appendLine("Item $idx | offset=${String.format(Locale.US, "%.1f", sc.offsetSec)} | ${sc.donor} (${sc.amountDisplay}): \"${sc.message}\" | $txt")
            }
        }
        val sys = """Align Super Chat donations with streamer reaction. Return STRICT JSON ONLY: {"alignments":[{"offset":120.0,"start":116.0,"end":148.0}]}"""
        val raw = completeChat(config, sys, entries, 500) ?: return@withContext emptyMap()
        val jsonStr = extractJsonObject(raw) ?: return@withContext emptyMap()
        runCatching {
            val arr = JSONObject(jsonStr).optJSONArray("alignments") ?: return@runCatching emptyMap()
            val map = mutableMapOf<Double, Pair<Double, Double>>()
            for (i in 0 until arr.length()) {
                val o = arr.optJSONObject(i) ?: continue
                val off = o.optDouble("offset", Double.NaN); val s = o.optDouble("start", Double.NaN); val e = o.optDouble("end", Double.NaN)
                if (!off.isNaN() && !s.isNaN() && !e.isNaN() && e > s) {
                    val safeS = s.coerceIn(0.0, durationSec)
                    map[off] = safeS to e.coerceIn(safeS + 5.0, durationSec.coerceAtLeast(safeS + 5.0))
                }
            }
            map
        }.getOrDefault(emptyMap())
    }

    private fun completeChat(config: AiConfig, sys: String, usr: String, maxTokens: Int): String? {
        val base = AiConfigStore.normalizeBaseUrl(config.baseUrl)
        val keys = config.orderedKeys()
        val model = config.selectedModel.trim().ifBlank { config.preset.defaultModel }
        if (base.isBlank() || keys.isEmpty()) return null
        val payload = JSONObject().put("model", model).put("max_tokens", maxTokens).put("temperature", 0.2)
            .put("messages", JSONArray()
                .put(JSONObject().put("role", "system").put("content", sys))
                .put(JSONObject().put("role", "user").put("content", usr))).toString()
        val body = executeWithFailover(base, keys) { key ->
            Request.Builder().url("$base/chat/completions").post(payload.toRequestBody(jsonType))
                .addHeader("Authorization", "Bearer $key").addHeader("Content-Type", "application/json")
                .addHeader("HTTP-Referer", "https://clippulse.app").addHeader("X-Title", "ClipPulse").build()
        }.getOrNull() ?: return null
        return runCatching { JSONObject(body).getJSONArray("choices").getJSONObject(0).getJSONObject("message").getString("content").trim() }.getOrNull()
    }

    private fun extractJsonObject(raw: String): String? {
        val cleaned = raw.replace(Regex("""<think>[\s\S]*?</think>""", RegexOption.IGNORE_CASE), "")
            .replace("```json", "", ignoreCase = true).replace("```", "").trim()
        return Regex("""\{[\s\S]*\}""").find(cleaned)?.value
    }

    private fun executeWithFailover(baseUrl: String, keys: List<String>, reqFactory: (String) -> Request): Result<String> {
        var lastErr = "Request failed"
        val host = runCatching { Uri.parse(baseUrl).host }.getOrNull().orEmpty().ifBlank { baseUrl }
        for ((idx, key) in keys.withIndex()) {
            try {
                client.newCall(reqFactory(key)).execute().use { resp ->
                    val bodyStr = resp.body?.string().orEmpty()
                    if (resp.isSuccessful) return Result.success(bodyStr)
                    val msg = runCatching { JSONObject(bodyStr).optJSONObject("error")?.optString("message") }.getOrNull()?.takeIf { it.isNotBlank() } ?: resp.message
                    lastErr = if (resp.code == 402) {
                        "Key #${idx + 1} ($host): HTTP 402 ($msg) — check balance or switch preset (e.g. Gemini)"
                    } else {
                        "Key #${idx + 1} ($host): HTTP ${resp.code} ($msg)"
                    }
                    val rotatable = resp.code == 401 || resp.code == 402 || resp.code == 403 || resp.code == 429 || resp.code in 500..599
                    if (!rotatable || idx == keys.lastIndex) return Result.failure(IllegalStateException(lastErr))
                }
            } catch (e: Throwable) {
                lastErr = e.message ?: "Network error"
                if (idx == keys.lastIndex) return Result.failure(IllegalStateException(lastErr))
            }
        }
        return Result.failure(IllegalStateException(lastErr))
    }
}
''')

    w(f"{PKG}/engine/UrlNormalizer.kt", r'''
package com.clippulse.studio.engine

import android.net.Uri

object UrlNormalizer {
    fun extractAndNormalize(rawInput: String): String {
        val extracted = Regex("""https?://\S+""").find(rawInput.trim())?.value
            ?.trimEnd('.', ',', ')', ']', '"', '\'')
            ?: rawInput.trim()
        if (extracted.isBlank()) return ""

        val uri = runCatching { Uri.parse(extracted) }.getOrNull() ?: return extracted
        val host = uri.host?.lowercase().orEmpty()
        val segments = uri.pathSegments.orEmpty()

        val youtubeVideoId: String? = when {
            host == "youtu.be" || host.endsWith(".youtu.be") -> segments.firstOrNull()
            host.contains("youtube.com") -> when {
                segments.firstOrNull() == "watch" -> uri.getQueryParameter("v")
                segments.firstOrNull() == "live" && segments.size >= 2 -> segments[1]
                segments.firstOrNull() == "shorts" && segments.size >= 2 -> segments[1]
                segments.firstOrNull() == "embed" && segments.size >= 2 -> segments[1]
                else -> null
            }
            else -> null
        }

        return if (!youtubeVideoId.isNullOrBlank()) {
            val cleanId = youtubeVideoId.takeWhile { it.isLetterOrDigit() || it == '-' || it == '_' }
            if (cleanId.isNotBlank()) "https://www.youtube.com/watch?v=$cleanId" else extracted
        } else {
            extracted
        }
    }

    fun sanitizeErrorMessage(raw: String): String {
        // Strip massive 1500-char googlevideo.com URLs from yt-dlp/ffmpeg stderr
        val noLongUrls = raw.replace(Regex("""https?://\S{70,}"""), "[stream-url]")
        val lines = noLongUrls.lineSequence()
            .map { it.trim() }
            .filter { it.isNotEmpty() && !it.startsWith("WARNING: Your yt-dlp") && !it.startsWith("It is strongly") && !it.startsWith("Run \"yt-dlp") && !it.startsWith("To suppress") }
            .toList()
        val keyLine = lines.lastOrNull {
            it.contains("403", true) || it.contains("404", true) || it.contains("Sign in", true) ||
                it.contains("Private", true) || it.contains("ERROR:", true) || it.contains("failed", true)
        } ?: lines.lastOrNull() ?: "Operation failed"
        return keyLine.take(220)
    }
}
''')

    w(f"{PKG}/engine/EngineInitializer.kt", r'''
package com.clippulse.studio.engine

import android.content.Context
import com.yausername.ffmpeg.FFmpeg
import com.yausername.youtubedl_android.YoutubeDL

object EngineInitializer {
    @Volatile private var initialized = false
    private val lock = Any()

    fun ensureInitialized(context: Context): Result<Unit> {
        if (initialized) return Result.success(Unit)
        synchronized(lock) {
            if (initialized) return Result.success(Unit)
            return runCatching {
                val app = context.applicationContext
                YoutubeDL.getInstance().init(app)
                FFmpeg.getInstance().init(app)
                initialized = true
            }
        }
    }

    fun autoUpdateIfStale(context: Context) {
        runCatching {
            val prefs = context.applicationContext.getSharedPreferences("clippulse_ai_prefs", Context.MODE_PRIVATE)
            val lastCheck = prefs.getLong("ytdlp_last_update", 0L)
            val now = System.currentTimeMillis()
            if (now - lastCheck > 24L * 3600L * 1000L) {
                YoutubeDL.getInstance().updateYoutubeDL(context.applicationContext)
                prefs.edit().putLong("ytdlp_last_update", now).apply()
            }
        }
    }

    fun updateYtDlpEngine(context: Context): Result<String> = runCatching {
        ensureInitialized(context).getOrThrow()
        val res = YoutubeDL.getInstance().updateYoutubeDL(context.applicationContext)?.toString() ?: "UPDATED"
        context.applicationContext.getSharedPreferences("clippulse_ai_prefs", Context.MODE_PRIVATE)
            .edit().putLong("ytdlp_last_update", System.currentTimeMillis()).apply()
        res
    }
}
''')

    w(f"{PKG}/engine/StreamPreviewResolver.kt", r'''
package com.clippulse.studio.engine

import android.content.Context
import com.clippulse.studio.data.AiConfigStore
import com.yausername.youtubedl_android.YoutubeDL
import com.yausername.youtubedl_android.YoutubeDLRequest
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.util.concurrent.ConcurrentHashMap

data class PlayableStreamInfo(
    val url: String,
    val userAgent: String,
    val referer: String
)

object StreamPreviewResolver {
    const val DESKTOP_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    private val cache = ConcurrentHashMap<String, PlayableStreamInfo>()

    suspend fun resolvePlayableStream(context: Context, sourceUrl: String): Result<PlayableStreamInfo> = withContext(Dispatchers.IO) {
        val clean = UrlNormalizer.extractAndNormalize(sourceUrl)
        if (clean.isBlank()) return@withContext Result.failure(IllegalArgumentException("Empty URL"))
        cache[clean]?.let { return@withContext Result.success(it) }

        EngineInitializer.ensureInitialized(context).getOrThrow()
        val cookiesFile = AiConfigStore(context).getCookiesFile()

        // Try web-compatible clients first so ExoPlayer does not get a c=ANDROID token-locked URL (403 Forbidden)
        val clientProfiles = listOf("tv_embedded,mweb", "ios,web", "default")
        var lastError = "Could not load stream preview"

        for (clientArg in clientProfiles) {
            val attempt = runCatching {
                val req = YoutubeDLRequest(clean).apply {
                    addOption("-g")
                    addOption("-f", "18/b[height<=720][ext=mp4]/b[ext=mp4]/b[height<=720]/b")
                    addOption("--no-playlist")
                    addOption("--no-warnings")
                    addOption("--user-agent", DESKTOP_UA)
                    addOption("--referer", "https://www.youtube.com/")
                    if (clientArg != "default") {
                        addOption("--extractor-args", "youtube:player_client=$clientArg")
                    }
                    if (cookiesFile != null) {
                        addOption("--cookies", cookiesFile.absolutePath)
                    }
                }
                val resp = YoutubeDL.getInstance().execute(req)
                val streamUrl = resp.out.lineSequence()
                    .map { it.trim() }
                    .firstOrNull { (it.startsWith("http://") || it.startsWith("https://")) && !it.contains("c=ANDROID") }
                    ?: resp.out.lineSequence().map { it.trim() }.firstOrNull { it.startsWith("http://") || it.startsWith("https://") }
                    ?: throw IllegalStateException("No playable preview stream available")
                PlayableStreamInfo(streamUrl, DESKTOP_UA, "https://www.youtube.com/")
            }
            if (attempt.isSuccess) {
                val info = attempt.getOrThrow()
                cache[clean] = info
                return@withContext Result.success(info)
            } else {
                lastError = UrlNormalizer.sanitizeErrorMessage(attempt.exceptionOrNull()?.message.orEmpty())
            }
        }
        Result.failure(IllegalStateException(lastError))
    }

    fun clearCache() {
        cache.clear()
    }
}
''')

    w(f"{PKG}/engine/SuperChatOverlayRenderer.kt", r'''
package com.clippulse.studio.engine

import android.graphics.*
import com.clippulse.studio.model.SuperChatEvent
import java.io.File
import java.io.FileOutputStream

object SuperChatOverlayRenderer {
    /**
     * Renders a crisp YouTube-style tiered Super Chat card PNG for FFmpeg overlay compositing.
     */
    fun renderCardPng(sc: SuperChatEvent, outFile: File): File {
        val width = 680
        val hasMsg = sc.message.isNotBlank()
        val height = if (hasMsg) 156 else 92

        val (headerColor, bodyColor) = when {
            sc.usdApprox >= 100.0 -> Color.parseColor("#D00000") to Color.parseColor("#E62117")
            sc.usdApprox >= 50.0 -> Color.parseColor("#C2185B") to Color.parseColor("#E91E63")
            sc.usdApprox >= 20.0 -> Color.parseColor("#E65100") to Color.parseColor("#F57C00")
            sc.usdApprox >= 10.0 -> Color.parseColor("#F5B400") to Color.parseColor("#FFCA28")
            sc.usdApprox >= 5.0 -> Color.parseColor("#00BFA5") to Color.parseColor("#1DE9B6")
            else -> Color.parseColor("#1565C0") to Color.parseColor("#1E88E5")
        }
        val textColor = if (sc.usdApprox in 5.0..19.99) Color.parseColor("#111116") else Color.WHITE

        val bmp = Bitmap.createBitmap(width, height, Bitmap.Config.ARGB_8888)
        val canvas = Canvas(bmp)
        val paint = Paint(Paint.ANTI_ALIAS_FLAG)

        // Shadow & full card rounded background
        paint.color = if (hasMsg) bodyColor else headerColor
        canvas.drawRoundRect(RectF(4f, 4f, width - 4f, height - 4f), 22f, 22f, paint)

        // Header bar
        paint.color = headerColor
        canvas.drawRoundRect(RectF(4f, 4f, width - 4f, 84f), 22f, 22f, paint)
        if (hasMsg) {
            canvas.drawRect(RectF(4f, 60f, width - 4f, 84f), paint)
        }

        // Donor badge circle
        paint.color = Color.argb(55, 255, 255, 255)
        canvas.drawCircle(46f, 44f, 22f, paint)
        paint.color = textColor
        paint.textSize = 22f
        paint.typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD)
        val initial = sc.donor.firstOrNull()?.uppercaseChar()?.toString() ?: "$"
        canvas.drawText(initial, 39f, 52f, paint)

        // Donor name & donation amount
        paint.textSize = 23f
        canvas.drawText(sc.donor.take(24), 80f, 38f, paint)

        paint.textSize = 26f
        canvas.drawText(sc.amountDisplay, 80f, 70f, paint)

        // Super Chat message text
        if (hasMsg) {
            paint.typeface = Typeface.create(Typeface.DEFAULT, Typeface.NORMAL)
            paint.textSize = 22f
            val cleanMsg = sc.message.replace("\n", " ").trim()
            val line1 = cleanMsg.take(48)
            val line2 = if (cleanMsg.length > 48) cleanMsg.drop(48).take(46) + if (cleanMsg.length > 94) "..." else "" else ""
            canvas.drawText(line1, 24f, 114f, paint)
            if (line2.isNotEmpty()) {
                canvas.drawText(line2, 24f, 140f, paint)
            }
        }

        FileOutputStream(outFile).use { out ->
            bmp.compress(Bitmap.CompressFormat.PNG, 100, out)
        }
        bmp.recycle()
        return outFile
    }
}
''')

    w(f"{PKG}/engine/FfmpegRunner.kt", r'''
package com.clippulse.studio.engine

import android.content.Context
import java.io.BufferedReader
import java.io.File
import java.io.InputStreamReader
import java.nio.charset.StandardCharsets

object FfmpegRunner {
    fun run(context: Context, args: List<String>, onLine: ((String) -> Unit)? = null): Result<Unit> = runCatching {
        EngineInitializer.ensureInitialized(context).getOrThrow()
        val nativeDir = context.applicationInfo.nativeLibraryDir
        val bin = File(nativeDir, "libffmpeg.so").takeIf { it.exists() }
            ?: File(context.noBackupFilesDir, "youtubedl-android/packages/ffmpeg/usr/bin/ffmpeg").takeIf { it.exists() }
            ?: throw IllegalStateException("FFmpeg binary not found in $nativeDir")
        val cmd = ArrayList<String>(args.size + 1).apply { add(bin.absolutePath); addAll(args) }
        val pb = ProcessBuilder(cmd).apply {
            redirectErrorStream(true)
            val ld = environment()["LD_LIBRARY_PATH"].orEmpty()
            environment()["LD_LIBRARY_PATH"] = if (ld.isBlank()) nativeDir else "$nativeDir:$ld"
        }
        val proc = pb.start()
        val tail = ArrayDeque<String>(24)
        BufferedReader(InputStreamReader(proc.inputStream, StandardCharsets.UTF_8), 32768).use { r ->
            var line = r.readLine()
            while (line != null) {
                onLine?.invoke(line)
                if (tail.size >= 24) tail.removeFirst()
                tail.addLast(line)
                line = r.readLine()
            }
        }
        val code = proc.waitFor()
        if (code != 0) {
            val cleanErr = UrlNormalizer.sanitizeErrorMessage(tail.joinToString("\n"))
            throw IllegalStateException("FFmpeg error ($code): $cleanErr")
        }
    }
}
''')

    w(f"{PKG}/engine/SubtitleAndChatParser.kt", r'''
package com.clippulse.studio.engine

import com.clippulse.studio.model.ClipCandidate
import com.clippulse.studio.model.SignalSource
import com.clippulse.studio.model.SuperChatEvent
import com.clippulse.studio.model.TranscriptCue
import org.json.JSONObject
import java.io.BufferedReader
import java.io.File
import java.io.FileInputStream
import java.io.InputStreamReader
import java.nio.charset.StandardCharsets
import java.util.Locale
import java.util.UUID
import kotlin.math.sqrt

data class ChatVelocitySpike(val startSec: Double, val endSec: Double, val messageCount: Int, val multiplierOverAvg: Double)
data class LiveChatParseOutput(val superChats: List<SuperChatEvent>, val velocitySpikes: List<ChatVelocitySpike>, val totalMessagesParsed: Int)

object SubtitleAndChatParser {
    fun parseLiveChatStreaming(chatFile: File, durationSec: Double): LiveChatParseOutput {
        if (!chatFile.exists() || chatFile.length() == 0L) return LiveChatParseOutput(emptyList(), emptyList(), 0)
        val superChats = mutableListOf<SuperChatEvent>()
        val buckets = HashMap<Int, Int>()
        var total = 0
        BufferedReader(InputStreamReader(FileInputStream(chatFile), StandardCharsets.UTF_8), 65536).use { reader ->
            var line = reader.readLine()
            while (line != null) {
                val t = line.trim()
                if (t.startsWith("{")) total += parseChatLine(t, durationSec, superChats, buckets)
                line = reader.readLine()
            }
        }
        return LiveChatParseOutput(superChats.sortedBy { it.offsetSec }, detectSpikes(buckets, durationSec), total)
    }

    private fun parseChatLine(jsonLine: String, durationSec: Double, scOut: MutableList<SuperChatEvent>, buckets: MutableMap<Int, Int>): Int {
        return try {
            val replay = JSONObject(jsonLine).optJSONObject("replayChatItemAction") ?: return 0
            val offsetMs = replay.optString("videoOffsetTimeMsec", "").toLongOrNull() ?: return 0
            if (offsetMs < 0L) return 0
            val offsetSec = offsetMs / 1000.0
            if (durationSec > 0.0 && offsetSec > durationSec + 30.0) return 0
            val actions = replay.optJSONArray("actions") ?: return 0
            val bucket = (offsetSec / 10.0).toInt().coerceAtLeast(0)
            var count = 0
            for (i in 0 until actions.length()) {
                val item = actions.optJSONObject(i)?.optJSONObject("addChatItemAction")?.optJSONObject("item") ?: continue
                val paid = item.optJSONObject("liveChatPaidMessageRenderer")
                val sticker = item.optJSONObject("liveChatPaidStickerRenderer")
                val text = item.optJSONObject("liveChatTextMessageRenderer")
                val member = item.optJSONObject("liveChatMembershipItemRenderer")
                if (paid != null) {
                    count++; buckets[bucket] = (buckets[bucket] ?: 0) + 1
                    extractSuperChat(paid, offsetSec, false)?.let { scOut.add(it) }
                } else if (sticker != null) {
                    count++; buckets[bucket] = (buckets[bucket] ?: 0) + 1
                    extractSuperChat(sticker, offsetSec, true)?.let { scOut.add(it) }
                } else if (text != null || member != null) {
                    count++; buckets[bucket] = (buckets[bucket] ?: 0) + 1
                }
            }
            count
        } catch (_: Throwable) { 0 }
    }

    private fun extractSuperChat(r: JSONObject, offsetSec: Double, isSticker: Boolean): SuperChatEvent? {
        val donor = r.optJSONObject("authorName")?.optString("simpleText")?.trim()?.takeIf { it.isNotEmpty() } ?: "Supporter"
        val amt = r.optJSONObject("purchaseAmountText")?.optString("simpleText")?.trim()?.takeIf { it.isNotEmpty() } ?: return null
        val runs = r.optJSONObject("message")?.optJSONArray("runs")
        val msg = buildString { if (runs != null) for (i in 0 until runs.length()) append(runs.optJSONObject(i)?.optString("text").orEmpty()) }
            .trim().ifBlank { if (isSticker) "[Super Sticker]" else "" }
        val rawVal = Regex("""(\d+(?:\.\d+)?)""").find(amt.replace(",", ""))?.groupValues?.getOrNull(1)?.toDoubleOrNull() ?: 1.0
        val (cur, usd) = when {
            amt.contains("¥") || amt.contains("JPY", true) -> "JPY" to rawVal / 150.0
            amt.contains("₩") || amt.contains("KRW", true) -> "KRW" to rawVal / 1380.0
            amt.contains("₹") || amt.contains("INR", true) -> "INR" to rawVal / 84.0
            amt.contains("€") || amt.contains("EUR", true) -> "EUR" to rawVal * 1.08
            amt.contains("£") || amt.contains("GBP", true) -> "GBP" to rawVal * 1.27
            else -> "USD" to rawVal
        }
        return SuperChatEvent(donor, amt, usd, cur, msg, offsetSec)
    }

    private fun detectSpikes(buckets: Map<Int, Int>, durationSec: Double): List<ChatVelocitySpike> {
        if (buckets.size < 4) return emptyList()
        val vals = buckets.values.map { it.toDouble() }
        val mean = vals.average()
        val std = sqrt(vals.sumOf { (it - mean) * (it - mean) } / vals.size.toDouble())
        val threshold = maxOf(6.0, mean + 2.1 * std)
        val spiked = buckets.entries.filter { it.value.toDouble() >= threshold }.sortedBy { it.key }
        if (spiked.isEmpty()) return emptyList()
        val merged = mutableListOf<ChatVelocitySpike>()
        var sB = spiked.first().key; var eB = sB; var peak = spiked.first().value
        for (i in 1 until spiked.size) {
            val (b, c) = spiked[i]
            if (b <= eB + 2) { eB = b; if (c > peak) peak = c }
            else { merged.add(makeSpike(sB, eB, peak, mean, durationSec)); sB = b; eB = b; peak = c }
        }
        merged.add(makeSpike(sB, eB, peak, mean, durationSec))
        return merged.sortedByDescending { it.messageCount }.take(12)
    }

    private fun makeSpike(sB: Int, eB: Int, peak: Int, mean: Double, dur: Double): ChatVelocitySpike {
        val s = (sB * 10.0).coerceAtLeast(0.0)
        val rawE = (eB + 1) * 10.0
        val e = if (dur > 0.0) rawE.coerceAtMost(dur) else rawE
        return ChatVelocitySpike(s, e.coerceAtLeast(s + 10.0), peak, if (mean > 0.1) peak.toDouble() / mean else 3.0)
    }

    fun parseVttSubtitles(vttFile: File): List<TranscriptCue> {
        if (!vttFile.exists()) return emptyList()
        val raw = mutableListOf<TranscriptCue>()
        val timeRe = Regex("""(?:(\d+):)?(\d{2}):(\d{2}\.\d+)\s*-->\s*(?:(\d+):)?(\d{2}):(\d{2}\.\d+)""")
        val tagRe = Regex("""<[^>]+>""")
        var curS: Double? = null; var curE: Double? = null; val buf = StringBuilder()
        vttFile.forEachLine(StandardCharsets.UTF_8) { rawLine ->
            val line = rawLine.trim()
            val m = timeRe.find(line)
            if (m != null) {
                if (curS != null && curE != null && buf.isNotEmpty()) raw.add(TranscriptCue(curS!!, curE!!, buf.toString().trim()))
                buf.clear()
                curS = (m.groupValues[1].toDoubleOrNull() ?: 0.0) * 3600.0 + (m.groupValues[2].toDoubleOrNull() ?: 0.0) * 60.0 + (m.groupValues[3].toDoubleOrNull() ?: 0.0)
                curE = (m.groupValues[4].toDoubleOrNull() ?: 0.0) * 3600.0 + (m.groupValues[5].toDoubleOrNull() ?: 0.0) * 60.0 + (m.groupValues[6].toDoubleOrNull() ?: 0.0)
            } else if (line.isNotEmpty() && !line.startsWith("WEBVTT") && !line.startsWith("Kind:") && !line.startsWith("Language:") && line.toIntOrNull() == null) {
                val clean = line.replace(tagRe, "").replace("&amp;", "&").replace("&gt;", ">").replace("&lt;", "<").replace("&#39;", "'").replace("&quot;", "\"").trim()
                if (clean.isNotEmpty()) { if (buf.isNotEmpty()) buf.append(' '); buf.append(clean) }
            }
        }
        if (curS != null && curE != null && buf.isNotEmpty()) raw.add(TranscriptCue(curS!!, curE!!, buf.toString().trim()))
        val dedup = mutableListOf<TranscriptCue>()
        for (c in raw) {
            val prev = dedup.lastOrNull()
            if (prev != null && (prev.text == c.text || c.text.startsWith(prev.text))) dedup[dedup.lastIndex] = c.copy(startSec = prev.startSec)
            else dedup.add(c)
        }
        return dedup
    }

    fun detectTranscriptExcitementPeaks(cues: List<TranscriptCue>, durationSec: Double): List<ClipCandidate> {
        if (cues.isEmpty()) return emptyList()
        val windowSec = 25.0
        val bucketCount = ((durationSec / windowSec).toInt() + 1).coerceIn(1, 720)
        val windowText = Array(bucketCount) { StringBuilder() }
        val windowWords = IntArray(bucketCount)

        for (cue in cues) {
            val idx = (cue.startSec / windowSec).toInt().coerceIn(0, bucketCount - 1)
            val words = cue.text.split(Regex("""\s+""")).count { it.isNotBlank() }
            windowWords[idx] += words
            if (windowText[idx].length < 400) {
                if (windowText[idx].isNotEmpty()) windowText[idx].append(' ')
                windowText[idx].append(cue.text)
            }
        }

        val activeCounts = windowWords.filter { it > 0 }.map { it.toDouble() }
        if (activeCounts.isEmpty()) return emptyList()
        val avgWords = activeCounts.average().coerceAtLeast(8.0)

        val hypePhrases = listOf(
            "no way", "oh my god", "omg", "what the", "are you serious", "let's go", "lets go",
            "bro", "insane", "crazy", "unbelievable", "wait a minute", "hold on", "listen",
            "laugh", "applause", "cheer", "goal", "retired", "impossible", "secret", "truth"
        )

        data class ScoredWindow(val idx: Int, val energy: Double, val title: String, val reason: String)
        val scored = mutableListOf<ScoredWindow>()

        for (i in 0 until bucketCount) {
            val wCount = windowWords[i]
            if (wCount < 6) continue
            val text = windowText[i].toString()
            val lower = text.lowercase(Locale.US)
            val paceRatio = wCount.toDouble() / avgWords
            val exclCount = text.count { it == '!' || it == '?' }
            val bracketTags = Regex("""\[(?:laughter|applause|cheering|music)]""", RegexOption.IGNORE_CASE).findAll(text).count()
            val phraseHits = hypePhrases.count { lower.contains(it) }

            val energy = (paceRatio * 1.4) + (exclCount * 0.35) + (bracketTags * 1.2) + (phraseHits * 0.55)
            val snippet = text.replace(Regex("""\[[^\]]+]"""), "").trim().take(52)
            val title = if (snippet.length >= 12) "\"$snippet...\"" else "Spoken Excitement Spike #${i + 1}"
            val reason = String.format(Locale.US, "High vocal energy (%.1fx speech pace, %d hype cues)", paceRatio, phraseHits + bracketTags)
            scored.add(ScoredWindow(i, energy, title, reason))
        }

        if (scored.isEmpty()) return emptyList()
        val maxEnergy = scored.maxOf { it.energy }.coerceAtLeast(1.0)

        return scored.sortedByDescending { it.energy }.take(10).map { sw ->
            val start = (sw.idx * windowSec).coerceAtLeast(0.0)
            val end = ((sw.idx + 1) * windowSec + 5.0).coerceAtMost(durationSec)
            val norm = (sw.energy / maxEnergy).coerceIn(0.0, 1.0)
            val score = (68 + (norm * 26.0).toInt()).coerceIn(68, 94)
            ClipCandidate(
                id = UUID.randomUUID().toString(), title = sw.title, startSec = start,
                endSec = end.coerceAtLeast((start + 5.0).coerceAtMost(durationSec)),
                hypeScore = score, signals = listOf(SignalSource.TRANSCRIPT_HOOK),
                isMultiSignal = false, reason = sw.reason
            )
        }
    }

    fun extractQuoteAround(cues: List<TranscriptCue>, startSec: Double, endSec: Double): String =
        cues.filter { it.endSec >= startSec && it.startSec <= endSec }.joinToString(" ") { it.text }.trim().take(220)
}
''')

    w(f"{PKG}/engine/VideoAnalysisEngine.kt", r'''
package com.clippulse.studio.engine

import android.content.Context
import android.media.MediaMetadataRetriever
import android.net.Uri
import android.provider.OpenableColumns
import com.clippulse.studio.data.AiConfigStore
import com.clippulse.studio.model.*
import com.clippulse.studio.network.UniversalAiClient
import com.yausername.youtubedl_android.YoutubeDL
import com.yausername.youtubedl_android.YoutubeDLRequest
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.io.File
import java.io.FileOutputStream
import java.util.Locale
import java.util.UUID
import kotlin.math.sqrt

class VideoAnalysisEngine(private val aiClient: UniversalAiClient = UniversalAiClient()) {

    suspend fun analyzeRemoteUrl(
        context: Context, rawUrl: String, mode: DetectionMode, superChatThreshold: SuperChatThreshold,
        paddingPreset: PaddingPreset, customAiPrompt: String, aiConfig: AiConfig, onProgress: (Float, String) -> Unit
    ): Result<VideoAnalysisResult> = withContext(Dispatchers.IO) {
        try {
            val cleanUrl = UrlNormalizer.extractAndNormalize(rawUrl)
            if (cleanUrl.isBlank()) return@withContext Result.failure(IllegalArgumentException("Enter a valid YouTube or Facebook link."))

            onProgress(0.10f, "Initializing yt-dlp zero-download engine...")
            EngineInitializer.ensureInitialized(context).getOrThrow()
            val cookiesFile = AiConfigStore(context).getCookiesFile()
            val workDir = File(context.cacheDir, "analysis_${System.currentTimeMillis()}").apply { mkdirs() }
            try {
                onProgress(0.24f, "Fetching metadata, heatmap & captions (zero download)...")
                fetchMetadataAndCaptions(cleanUrl, workDir, cookiesFile)

                val infoFile = workDir.listFiles()?.firstOrNull { it.name.endsWith(".info.json") }
                    ?: return@withContext Result.failure(IllegalStateException("Could not read video metadata. Add cookies.txt or tap 'Update yt-dlp' in Settings."))

                onProgress(0.42f, "Tracing Smart Valley-to-Valley heatmap boundaries...")
                val info = JSONObject(infoFile.readText(Charsets.UTF_8))
                val title = info.optString("title").ifBlank { "Untitled Video" }
                val channel = info.optString("uploader").ifBlank { info.optString("channel").ifBlank { "Creator" } }
                val duration = info.optDouble("duration", 0.0).coerceAtLeast(1.0)
                val wasLive = info.optBoolean("was_live", false) || info.optString("live_status") in listOf("was_live", "post_live")

                val heatmap = parseHeatmap(info)
                val raw = mutableListOf<ClipCandidate>()
                if (heatmap.isNotEmpty()) raw.addAll(detectValleyToValleyHeatmapPeaks(heatmap, duration))
                else raw.addAll(detectChaptersAndDesc(info, duration))

                var allSc = emptyList<SuperChatEvent>()
                var chatFile: File? = null
                if (wasLive || mode == DetectionMode.SUPER_CHAT || mode == DetectionMode.CHAT_HYPE || mode == DetectionMode.SMART_ALL) {
                    onProgress(0.56f, "Scanning live chat replay & Super Chats...")
                    runCatching {
                        val chatReq = YoutubeDLRequest(cleanUrl).apply {
                            addOption("--skip-download"); addOption("--write-subs"); addOption("--sub-langs", "live_chat")
                            addOption("--no-playlist"); addOption("--no-warnings"); addOption("--ignore-errors")
                            addOption("--user-agent", StreamPreviewResolver.DESKTOP_UA)
                            if (cookiesFile != null) addOption("--cookies", cookiesFile.absolutePath)
                            addOption("-o", File(workDir, "chat.%(ext)s").absolutePath)
                        }
                        YoutubeDL.getInstance().execute(chatReq)
                    }
                    chatFile = workDir.listFiles()?.firstOrNull { it.name.endsWith(".live_chat.json") }
                    if (chatFile != null) {
                        val out = SubtitleAndChatParser.parseLiveChatStreaming(chatFile, duration)
                        allSc = out.superChats
                        for (sp in out.velocitySpikes) {
                            raw.add(ClipCandidate(UUID.randomUUID().toString(), "Chat Hype Surge (${sp.messageCount} msgs/10s)",
                                (sp.startSec - 4.0).coerceAtLeast(0.0), (sp.endSec + 10.0).coerceAtMost(duration),
                                (70 + (sp.multiplierOverAvg * 6.0).toInt()).coerceIn(65, 96), listOf(SignalSource.CHAT_HYPE), false,
                                reason = String.format(Locale.US, "Chat spiked %.1fx above average", sp.multiplierOverAvg)))
                        }
                    }
                }

                onProgress(0.70f, "Indexing transcript cues...")
                val vttFile = workDir.listFiles()?.firstOrNull { it.name.endsWith(".vtt") }
                val cues = if (vttFile != null) SubtitleAndChatParser.parseVttSubtitles(vttFile) else emptyList()

                val filteredSc = allSc.filter { it.usdApprox >= superChatThreshold.minUsd }
                val aligned = if (aiConfig.canUseAi() && filteredSc.isNotEmpty() && cues.isNotEmpty()) {
                    onProgress(0.78f, "AI-aligning Super Chat donor reactions...")
                    aiClient.alignSuperChatReactions(aiConfig, filteredSc, cues, duration)
                } else emptyMap()

                for (sc in filteredSc) {
                    val rng = aligned[sc.offsetSec]
                    val s = rng?.first ?: (sc.offsetSec - 4.0).coerceAtLeast(0.0)
                    val e = rng?.second ?: (sc.offsetSec + 22.0).coerceAtMost(duration)
                    val score = when { sc.usdApprox >= 50.0 -> 95; sc.usdApprox >= 25.0 -> 90; sc.usdApprox >= 10.0 -> 84; sc.usdApprox >= 5.0 -> 78; else -> 72 }
                    raw.add(ClipCandidate(UUID.randomUUID().toString(), "${sc.donor} • ${sc.amountDisplay}", s, e, score,
                        listOf(SignalSource.SUPER_CHAT), false, superChat = sc, reason = "Super Chat highlight (${sc.amountDisplay})"))
                }

                if (aiConfig.canUseAi() && cues.isNotEmpty() && (mode == DetectionMode.SMART_ALL || mode == DetectionMode.AI_CUSTOM)) {
                    onProgress(0.86f, "Generating AI viral hooks, titles & hashtags...")
                    val picks = aiClient.findViralAndCustomClips(aiConfig, title, duration, cues, raw.map { (it.startSec + it.endSec) / 2.0 },
                        if (mode == DetectionMode.AI_CUSTOM) customAiPrompt else "")
                    for (p in picks) {
                        raw.add(ClipCandidate(
                            id = UUID.randomUUID().toString(), title = p.title, startSec = p.startSec, endSec = p.endSec,
                            hypeScore = p.score, signals = listOf(SignalSource.AI_PICK), isMultiSignal = false,
                            reason = p.reason, viralTitle = p.viralTitle, socialCaption = p.socialCaption, hashtags = p.hashtags
                        ))
                    }
                }

                if (cues.isNotEmpty() && raw.size < 3) {
                    onProgress(0.91f, "Scanning transcript for excitement & speech spikes...")
                    raw.addAll(SubtitleAndChatParser.detectTranscriptExcitementPeaks(cues, duration))
                }

                onProgress(0.96f, "Merging multi-signal consensus clips...")
                val modeFiltered = when (mode) {
                    DetectionMode.SMART_ALL -> raw
                    DetectionMode.HEATMAP -> raw.filter { SignalSource.HEATMAP in it.signals }
                    DetectionMode.SUPER_CHAT -> raw.filter { SignalSource.SUPER_CHAT in it.signals }
                    DetectionMode.CHAT_HYPE -> raw.filter { SignalSource.CHAT_HYPE in it.signals }
                    DetectionMode.AUDIO_PEAKS -> raw.filter { SignalSource.AUDIO_PEAK in it.signals }
                    DetectionMode.AI_CUSTOM -> raw.filter { SignalSource.AI_PICK in it.signals }
                }
                val effectiveList = if (modeFiltered.isNotEmpty()) modeFiltered else raw
                val consensus = runConsensus(effectiveList, title, channel, cues, paddingPreset, duration)

                val summary = buildString {
                    append("${consensus.size} clips found")
                    if (heatmap.isNotEmpty()) append(" • Heatmap")
                    if (allSc.isNotEmpty()) append(" • ${allSc.size} Super Chats")
                    if (cues.isNotEmpty()) append(" • Transcript")
                    if (modeFiltered.isEmpty() && raw.isNotEmpty()) append(" (auto-fallback)")
                }
                val result = VideoAnalysisResult(cleanUrl, false, null, title, channel, duration, heatmap, consensus, chatFile != null, cues.isNotEmpty(), summary)
                AiConfigStore(context).saveScanToHistory(result)
                onProgress(1.0f, "Done!")
                Result.success(result)
            } finally { workDir.deleteRecursively() }
        } catch (t: Throwable) {
            Result.failure(IllegalStateException(UrlNormalizer.sanitizeErrorMessage(t.message ?: "Analysis failed")))
        }
    }

    private fun fetchMetadataAndCaptions(cleanUrl: String, workDir: File, cookiesFile: File?) {
        val outPath = File(workDir, "meta.%(ext)s").absolutePath
        val profiles = listOf("tv_embedded,mweb", "ios,web", "default")
        var lastErr: Throwable? = null
        for (clientArg in profiles) {
            val attempt = runCatching {
                val req = YoutubeDLRequest(cleanUrl).apply {
                    addOption("--skip-download"); addOption("--write-info-json")
                    addOption("--write-auto-sub"); addOption("--write-subs"); addOption("--sub-langs", "en.*,en")
                    addOption("--user-agent", StreamPreviewResolver.DESKTOP_UA)
                    addOption("--referer", "https://www.youtube.com/")
                    if (clientArg != "default") addOption("--extractor-args", "youtube:player_client=$clientArg")
                    if (cookiesFile != null) addOption("--cookies", cookiesFile.absolutePath)
                    addOption("--no-playlist"); addOption("--no-warnings"); addOption("--ignore-errors")
                    addOption("-o", outPath)
                }
                YoutubeDL.getInstance().execute(req)
            }
            if (workDir.listFiles()?.any { it.name.endsWith(".info.json") } == true) return
            lastErr = attempt.exceptionOrNull()
        }
        if (lastErr != null) throw lastErr
    }

    suspend fun analyzeLocalVideo(context: Context, uri: Uri, paddingPreset: PaddingPreset, onProgress: (Float, String) -> Unit): Result<VideoAnalysisResult> = withContext(Dispatchers.IO) {
        try {
            onProgress(0.15f, "Staging local video...")
            val localDir = File(context.cacheDir, "local_videos").apply { mkdirs(); listFiles()?.forEach { it.delete() } }
            val name = context.contentResolver.query(uri, arrayOf(OpenableColumns.DISPLAY_NAME), null, null, null)?.use { c ->
                if (c.moveToFirst()) c.getString(0) else null
            } ?: "local_input.mp4"
            val staged = File(localDir, name)
            context.contentResolver.openInputStream(uri)?.use { inp -> FileOutputStream(staged).use { out -> inp.copyTo(out, 65536) } }
                ?: return@withContext Result.failure(IllegalStateException("Cannot read selected local video."))
            val retriever = MediaMetadataRetriever()
            val duration = try {
                retriever.setDataSource(staged.absolutePath)
                (retriever.extractMetadata(MediaMetadataRetriever.METADATA_KEY_DURATION)?.toLongOrNull() ?: 0L) / 1000.0
            } finally { runCatching { retriever.release() } }.coerceAtLeast(1.0)

            onProgress(0.50f, "Scanning audio RMS energy spikes with FFmpeg...")
            val ptsRe = Regex("""pts_time:(\d+(?:\.\d+)?)"""); val rmsRe = Regex("""RMS level dB:\s*(-?\d+(?:\.\d+)?)""")
            val samples = mutableListOf<Pair<Double, Double>>(); var latestPts = 0.0
            FfmpegRunner.run(context, listOf("-hide_banner", "-i", staged.absolutePath, "-af", "astats=metadata=1:reset=1", "-f", "null", "-")) { line ->
                ptsRe.find(line)?.groupValues?.getOrNull(1)?.toDoubleOrNull()?.let { latestPts = it }
                rmsRe.find(line)?.groupValues?.getOrNull(1)?.toDoubleOrNull()?.let { db -> if (db.isFinite() && db > -90.0) samples.add(latestPts to db) }
            }
            onProgress(0.85f, "Building acoustic energy peaks...")
            val (heatmap, peaks) = buildAudioPeaks(samples, duration)
            val consensus = runConsensus(peaks, staged.nameWithoutExtension, "Local Device Video", emptyList(), paddingPreset, duration)
            val result = VideoAnalysisResult(uri.toString(), true, staged.absolutePath, staged.nameWithoutExtension, "Local Device Video", duration, heatmap, consensus, false, false, "${consensus.size} audio peaks")
            AiConfigStore(context).saveScanToHistory(result)
            onProgress(1.0f, "Done!")
            Result.success(result)
        } catch (t: Throwable) { Result.failure(t) }
    }

    private fun parseHeatmap(info: JSONObject): List<HeatmapPoint> {
        val arr = info.optJSONArray("heatmap") ?: return emptyList()
        return (0 until arr.length()).mapNotNull { i ->
            val o = arr.optJSONObject(i) ?: return@mapNotNull null
            val s = o.optDouble("start_time", Double.NaN); val e = o.optDouble("end_time", Double.NaN); val v = o.optDouble("value", Double.NaN)
            if (!s.isNaN() && !e.isNaN() && !v.isNaN()) HeatmapPoint(s, e, v.coerceIn(0.0, 1.0)) else null
        }
    }

    /**
     * Smart Valley-to-Valley Heatmap Boundaries:
     * Traces backward from each peak to the local valley (setup) and forward to the next valley (punchline).
     */
    private fun detectValleyToValleyHeatmapPeaks(hm: List<HeatmapPoint>, dur: Double): List<ClipCandidate> {
        if (hm.size < 3) return emptyList()
        val out = mutableListOf<ClipCandidate>()
        for (i in 1 until hm.lastIndex) {
            val peakVal = hm[i].value
            if (peakVal >= 0.60 && peakVal >= hm[i - 1].value && peakVal >= hm[i + 1].value) {
                var leftIdx = i - 1
                while (leftIdx > 0 && hm[leftIdx - 1].value <= hm[leftIdx].value && (hm[i].startSec - hm[leftIdx].startSec) < 35.0) {
                    leftIdx--
                }
                var rightIdx = i + 1
                while (rightIdx < hm.lastIndex && hm[rightIdx + 1].value <= hm[rightIdx].value && (hm[rightIdx].endSec - hm[i].endSec) < 35.0) {
                    rightIdx++
                }
                val start = hm[leftIdx].startSec.coerceAtLeast(0.0)
                val end = hm[rightIdx].endSec.coerceAtMost(dur).coerceAtLeast((start + 8.0).coerceAtMost(dur))
                out.add(ClipCandidate(
                    id = UUID.randomUUID().toString(),
                    title = "Most Replayed Valley-to-Valley (${(peakVal * 100.0).toInt()}%)",
                    startSec = start,
                    endSec = end,
                    hypeScore = (62 + (peakVal * 36.0).toInt()).coerceIn(62, 98),
                    signals = listOf(SignalSource.HEATMAP),
                    isMultiSignal = false,
                    reason = "Valley-to-valley retention arc (${(peakVal * 100.0).toInt()}% peak)"
                ))
            }
        }
        return out.sortedByDescending { it.hypeScore }.take(12)
    }

    private fun detectChaptersAndDesc(info: JSONObject, dur: Double): List<ClipCandidate> {
        val chs = info.optJSONArray("chapters")
        if (chs != null && chs.length() > 0) {
            return (0 until chs.length().coerceAtMost(12)).mapNotNull { i ->
                val o = chs.optJSONObject(i) ?: return@mapNotNull null
                val s = o.optDouble("start_time", Double.NaN); val e = o.optDouble("end_time", Double.NaN)
                if (!s.isNaN() && !e.isNaN() && e > s) ClipCandidate(UUID.randomUUID().toString(), o.optString("title").ifBlank { "Chapter #${i + 1}" },
                    s.coerceAtLeast(0.0), minOf(e, s + 45.0).coerceAtMost(dur), 74, listOf(SignalSource.HEATMAP), false, reason = "Chapter marker") else null
            }
        }
        return Regex("""(?m)^(?:(\d{1,2}):)?(\d{1,2}):(\d{2})\s+(.+)$""").findAll(info.optString("description")).take(10).map { m ->
            val s = ((m.groupValues[1].toDoubleOrNull() ?: 0.0) * 3600.0 + (m.groupValues[2].toDoubleOrNull() ?: 0.0) * 60.0 + (m.groupValues[3].toDoubleOrNull() ?: 0.0)).coerceIn(0.0, (dur - 5.0).coerceAtLeast(0.0))
            ClipCandidate(UUID.randomUUID().toString(), m.groupValues[4].trim().take(60), s, (s + 30.0).coerceAtMost(dur), 72, listOf(SignalSource.HEATMAP), false, reason = "Description timestamp")
        }.toList()
    }

    private fun buildAudioPeaks(samples: List<Pair<Double, Double>>, dur: Double): Pair<List<HeatmapPoint>, List<ClipCandidate>> {
        if (samples.isEmpty()) return emptyList<HeatmapPoint>() to listOf(ClipCandidate(UUID.randomUUID().toString(), "Opening Highlight", 0.0, minOf(25.0, dur), 70, listOf(SignalSource.AUDIO_PEAK), false, reason = "Default segment"))
        val count = 40; val bSize = (dur / count.toDouble()).coerceAtLeast(1.0); val maxDb = DoubleArray(count) { -60.0 }
        for ((t, db) in samples) { val idx = (t / bSize).toInt().coerceIn(0, count - 1); if (db > maxDb[idx]) maxDb[idx] = db }
        val minV = maxDb.minOrNull() ?: -60.0; val maxV = maxDb.maxOrNull() ?: -10.0; val span = (maxV - minV).coerceAtLeast(1.0)
        val hm = (0 until count).map { i -> HeatmapPoint(i * bSize, minOf((i + 1) * bSize, dur), ((maxDb[i] - minV) / span).coerceIn(0.05, 1.0)) }
        val mean = maxDb.average(); val thresh = mean + 1.15 * sqrt(maxDb.sumOf { (it - mean) * (it - mean) } / count.toDouble())
        val peaks = (0 until count).filter { maxDb[it] >= thresh }.map { i ->
            val c = (i + 0.5) * bSize; val norm = ((maxDb[i] - minV) / span).coerceIn(0.0, 1.0)
            ClipCandidate(UUID.randomUUID().toString(), String.format(Locale.US, "Audio Peak (%.1f dB)", maxDb[i]),
                (c - 8.0).coerceAtLeast(0.0), (c + 14.0).coerceAtMost(dur), (68 + (norm * 29.0).toInt()).coerceIn(68, 97),
                listOf(SignalSource.AUDIO_PEAK), false, reason = String.format(Locale.US, "+%.1f dB above baseline", maxDb[i] - mean))
        }.sortedByDescending { it.hypeScore }.take(12)
        return hm to peaks
    }

    private fun runConsensus(cands: List<ClipCandidate>, videoTitle: String, channelName: String, cues: List<TranscriptCue>, pad: PaddingPreset, dur: Double): List<ClipCandidate> {
        if (cands.isEmpty()) return emptyList()
        val sorted = cands.sortedBy { it.startSec }; val merged = mutableListOf<ClipCandidate>(); var cur = sorted.first()
        for (i in 1 until sorted.size) {
            val nxt = sorted[i]
            if (nxt.startSec - cur.endSec <= 18.0) {
                val sigs = (cur.signals + nxt.signals).distinct(); val multi = sigs.size >= 2
                val score = if (multi) (maxOf(cur.hypeScore, nxt.hypeScore) + 11 * (sigs.size - 1)).coerceIn(1, 100) else maxOf(cur.hypeScore, nxt.hypeScore)
                val sc = cur.superChat ?: nxt.superChat
                val title = when { sc != null -> "${sc.donor} • ${sc.amountDisplay}"; nxt.hypeScore > cur.hypeScore -> nxt.title; else -> cur.title }
                val vTitle = cur.viralTitle.ifBlank { nxt.viralTitle }
                val sCap = cur.socialCaption.ifBlank { nxt.socialCaption }
                val tags = if (cur.hashtags != "#shorts #viral #clips") cur.hashtags else nxt.hashtags
                cur = cur.copy(
                    title = title, startSec = minOf(cur.startSec, nxt.startSec), endSec = maxOf(cur.endSec, nxt.endSec),
                    hypeScore = score, signals = sigs, isMultiSignal = multi, superChat = sc,
                    viralTitle = vTitle, socialCaption = sCap, hashtags = tags,
                    reason = listOf(cur.reason, nxt.reason).filter { it.isNotBlank() }.distinct().joinToString(" + ")
                )
            } else { merged.add(finalizeClip(cur, videoTitle, channelName, cues, pad, dur)); cur = nxt }
        }
        merged.add(finalizeClip(cur, videoTitle, channelName, cues, pad, dur))
        return merged.sortedWith(compareByDescending<ClipCandidate> { it.isMultiSignal }.thenByDescending { it.hypeScore }.thenBy { it.startSec })
    }

    private fun finalizeClip(c: ClipCandidate, videoTitle: String, channelName: String, cues: List<TranscriptCue>, pad: PaddingPreset, dur: Double): ClipCandidate {
        val s = (c.startSec - pad.beforeSec).coerceAtLeast(0.0)
        val e = (c.endSec + pad.afterSec).coerceAtMost(dur).coerceAtLeast((s + 3.0).coerceAtMost(dur))
        val quote = SubtitleAndChatParser.extractQuoteAround(cues, s, e)
        val cleanChannelTag = "#" + channelName.replace(Regex("""[^a-zA-Z0-9]"""), "").lowercase(Locale.US).take(18).ifBlank { "creator" }
        val autoViralTitle = c.viralTitle.ifBlank {
            when {
                c.superChat != null -> "${c.superChat.donor} Drops ${c.superChat.amountDisplay} Live Reaction! \uD83D\uDD25"
                quote.length >= 16 -> quote.take(58).trimEnd() + "..."
                else -> "${c.title} (${videoTitle.take(28)})"
            }
        }
        val autoCaption = c.socialCaption.ifBlank {
            if (quote.isNotBlank()) "\"${quote.take(120)}\" — via $channelName"
            else "Highlight moment from $videoTitle ($channelName)."
        }
        val autoTags = if (c.hashtags != "#shorts #viral #clips") c.hashtags else "#shorts #viral $cleanChannelTag #highlights #fyp"
        return c.copy(startSec = s, endSec = e, transcriptQuote = quote, viralTitle = autoViralTitle, socialCaption = autoCaption, hashtags = autoTags)
    }
}
''')

def write_exporter_service_and_ui() -> None:
    w(f"{PKG}/engine/ClipExporter.kt", r'''
package com.clippulse.studio.engine

import android.content.ContentValues
import android.content.Context
import android.media.MediaScannerConnection
import android.net.Uri
import android.os.Build
import android.os.Environment
import android.provider.MediaStore
import androidx.core.content.FileProvider
import com.clippulse.studio.data.AiConfigStore
import com.clippulse.studio.model.*
import com.yausername.youtubedl_android.YoutubeDL
import com.yausername.youtubedl_android.YoutubeDLRequest
import java.io.File
import java.io.FileInputStream
import java.io.FileOutputStream
import java.nio.charset.StandardCharsets
import java.util.Locale
import java.util.UUID

object ClipExporter {
    fun exportSingleClip(
        context: Context, sourceUrlOrUri: String, isLocalFile: Boolean, localFilePath: String?,
        videoTitle: String, clip: ClipCandidate, clipIndex: Int,
        quality: DownloadQuality, exportMode: ExportMode, burnSuperChat: Boolean, loudnormEnabled: Boolean, includeTxtNotes: Boolean
    ): Result<ExportedClipRecord> = runCatching {
        EngineInitializer.ensureInitialized(context).getOrThrow()
        val cookiesFile = AiConfigStore(context).getCookiesFile()
        val workDir = File(context.cacheDir, "export_${System.currentTimeMillis()}_$clipIndex").apply { mkdirs() }
        try {
            val safe = clip.title.replace(Regex("""[^a-zA-Z0-9._-]+"""), "_").trim('_').take(40).ifBlank { "Clip_${clipIndex + 1}" }
            val baseName = "ClipPulse_${clipIndex + 1}_$safe"
            val rawFile = File(workDir, "raw.mp4")
            val outMp4 = File(workDir, "$baseName.mp4")

            val overlayPng: File? = if (burnSuperChat && clip.superChat != null) {
                SuperChatOverlayRenderer.renderCardPng(clip.superChat, File(workDir, "sc_overlay.png"))
            } else null

            if (isLocalFile && !localFilePath.isNullOrBlank()) {
                val ss = TimeFormatter.formatFfmpegDuration(clip.startSec)
                val dur = TimeFormatter.formatFfmpegDuration(clip.durationSec)
                renderWithFfmpeg(context, localFilePath, outMp4.absolutePath, ss, dur, exportMode, overlayPng, loudnormEnabled)
            } else {
                val cleanUrl = UrlNormalizer.extractAndNormalize(sourceUrlOrUri)
                downloadSectionResilient(cleanUrl, quality, clip.startSec, clip.endSec, rawFile, cookiesFile)
                val dl = workDir.listFiles()?.firstOrNull { it.extension.equals("mp4", true) || it.name.startsWith("raw") }
                    ?: throw IllegalStateException("Section download produced no file.")
                renderWithFfmpeg(context, dl.absolutePath, outMp4.absolutePath, null, null, exportMode, overlayPng, loudnormEnabled)
            }

            if (!outMp4.exists() || outMp4.length() == 0L) throw IllegalStateException("Rendered MP4 is empty.")
            val fileSize = outMp4.length()
            val (displayPath, contentUri) = saveVideo(context, outMp4, "$baseName.mp4")
            if (includeTxtNotes) saveTxt(context, "$baseName.txt", buildNotes(videoTitle, sourceUrlOrUri, clip, quality, exportMode, loudnormEnabled))

            ExportedClipRecord(
                id = UUID.randomUUID().toString(), title = clip.viralTitle.ifBlank { clip.title },
                displayPath = displayPath, contentUriString = contentUri.toString(),
                durationSec = clip.durationSec, sizeBytes = fileSize, qualityLabel = quality.label,
                modeLabel = exportMode.label, audioLeveled = loudnormEnabled, exportedAtMillis = System.currentTimeMillis()
            )
        } finally { workDir.deleteRecursively() }
    }.recoverCatching { err ->
        throw IllegalStateException(UrlNormalizer.sanitizeErrorMessage(err.message ?: "Export failed"))
    }

    private fun downloadSectionResilient(
        cleanUrl: String, quality: DownloadQuality, startSec: Double, endSec: Double, outFile: File, cookiesFile: File?
    ) {
        val sectionSpec = "*${TimeFormatter.formatSectionTimestamp(startSec)}-${TimeFormatter.formatSectionTimestamp(endSec)}"
        // Use web-friendly clients + desktop headers so external FFmpeg section cutting never gets HTTP 403
        val profiles = listOf("tv_embedded,mweb", "ios,web", "default")
        var lastError: Throwable? = null

        for (clientArg in profiles) {
            val attempt = runCatching {
                val req = YoutubeDLRequest(cleanUrl).apply {
                    addOption("-f", quality.formatSelector)
                    addOption("--merge-output-format", "mp4")
                    addOption("--download-sections", sectionSpec)
                    addOption("--force-keyframes-at-cuts")
                    addOption("--no-playlist")
                    addOption("--user-agent", StreamPreviewResolver.DESKTOP_UA)
                    addOption("--referer", "https://www.youtube.com/")
                    if (clientArg != "default") {
                        addOption("--extractor-args", "youtube:player_client=$clientArg")
                    }
                    if (cookiesFile != null) {
                        addOption("--cookies", cookiesFile.absolutePath)
                    }
                    addOption("-o", outFile.absolutePath)
                }
                YoutubeDL.getInstance().execute(req)
            }
            if (attempt.isSuccess) return
            lastError = attempt.exceptionOrNull()
        }
        throw lastError ?: IllegalStateException("Section download failed (403 Forbidden)")
    }

    private fun renderWithFfmpeg(
        context: Context, inputPath: String, outputPath: String,
        ss: String?, dur: String?, mode: ExportMode, overlayPng: File?, loudnorm: Boolean
    ) {
        val baseInput = buildList {
            add("-y")
            if (ss != null) { add("-ss"); add(ss) }
            add("-i"); add(inputPath)
            if (dur != null) { add("-t"); add(dur) }
            if (overlayPng != null && overlayPng.exists()) {
                add("-i"); add(overlayPng.absolutePath)
            }
        }

        val hasOverlay = overlayPng != null && overlayPng.exists()
        if (mode == ExportMode.FAST_COPY && !loudnorm && !hasOverlay) {
            FfmpegRunner.run(context, baseInput + listOf("-c", "copy", "-movflags", "+faststart", outputPath)).getOrThrow()
            return
        }

        val vArgs = when {
            hasOverlay && mode == ExportMode.VERTICAL_CROP -> listOf(
                "-filter_complex", "[0:v]crop=ih*9/16:ih[bg];[1:v]scale=min(iw\\,520):-1[ov];[bg][ov]overlay=(W-w)/2:H-h-90",
                "-c:v", "libx264", "-preset", "ultrafast", "-crf", "22", "-threads", "2"
            )
            hasOverlay -> listOf(
                "-filter_complex", "[1:v]scale=min(iw\\,560):-1[ov];[0:v][ov]overlay=28:H-h-28",
                "-c:v", "libx264", "-preset", "ultrafast", "-crf", "22", "-threads", "2"
            )
            mode == ExportMode.VERTICAL_CROP -> listOf(
                "-vf", "crop=ih*9/16:ih", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "22", "-threads", "2"
            )
            else -> listOf("-c:v", "copy")
        }

        if (loudnorm) {
            val normArgs = baseInput + vArgs + listOf("-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", outputPath)
            if (FfmpegRunner.run(context, normArgs).isSuccess) return
        }

        val fallbackAArgs = if (mode == ExportMode.VERTICAL_CROP || hasOverlay) listOf("-c:a", "aac", "-b:a", "128k") else listOf("-c:a", "copy")
        FfmpegRunner.run(context, baseInput + vArgs + fallbackAArgs + listOf("-movflags", "+faststart", outputPath)).getOrThrow()
    }

    private fun saveVideo(context: Context, src: File, name: String): Pair<String, Uri> {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            val r = context.contentResolver
            val v = ContentValues().apply {
                put(MediaStore.Video.Media.DISPLAY_NAME, name); put(MediaStore.Video.Media.MIME_TYPE, "video/mp4")
                put(MediaStore.Video.Media.RELATIVE_PATH, "${Environment.DIRECTORY_MOVIES}/ClipPulse"); put(MediaStore.Video.Media.IS_PENDING, 1)
            }
            val uri = r.insert(MediaStore.Video.Media.EXTERNAL_CONTENT_URI, v) ?: throw IllegalStateException("MediaStore URI failed.")
            r.openOutputStream(uri)?.use { out -> FileInputStream(src).use { it.copyTo(out, 65536) } }
            v.clear(); v.put(MediaStore.Video.Media.IS_PENDING, 0); r.update(uri, v, null, null)
            return "Movies/ClipPulse/$name" to uri
        }
        val dir = File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_MOVIES), "ClipPulse").apply { mkdirs() }
        val dst = File(dir, name); FileInputStream(src).use { inp -> FileOutputStream(dst).use { inp.copyTo(it, 65536) } }
        MediaScannerConnection.scanFile(context, arrayOf(dst.absolutePath), arrayOf("video/mp4"), null)
        val uri = FileProvider.getUriForFile(context, "${context.packageName}.fileprovider", dst)
        return "Movies/ClipPulse/$name" to uri
    }

    private fun saveTxt(context: Context, name: String, content: String) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            val r = context.contentResolver
            val v = ContentValues().apply {
                put(MediaStore.MediaColumns.DISPLAY_NAME, name); put(MediaStore.MediaColumns.MIME_TYPE, "text/plain")
                put(MediaStore.MediaColumns.RELATIVE_PATH, "${Environment.DIRECTORY_DOCUMENTS}/ClipPulse"); put(MediaStore.MediaColumns.IS_PENDING, 1)
            }
            val uri = r.insert(MediaStore.Files.getContentUri("external"), v) ?: return
            r.openOutputStream(uri)?.use { it.write(content.toByteArray(StandardCharsets.UTF_8)) }
            v.clear(); v.put(MediaStore.MediaColumns.IS_PENDING, 0); r.update(uri, v, null, null)
        } else {
            val dir = File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOCUMENTS), "ClipPulse").apply { mkdirs() }
            File(dir, name).writeText(content, StandardCharsets.UTF_8)
        }
    }

    private fun buildNotes(videoTitle: String, url: String, clip: ClipCandidate, quality: DownloadQuality, mode: ExportMode, loudnorm: Boolean) = buildString {
        appendLine("ClipPulse Studio Export Pack")
        appendLine("============================")
        appendLine("Viral Title : ${clip.viralTitle.ifBlank { clip.title }}")
        if (clip.socialCaption.isNotBlank()) appendLine("Caption     : ${clip.socialCaption}")
        appendLine("Hashtags    : ${clip.hashtags}")
        appendLine("Source      : $videoTitle ($url)")
        appendLine(String.format(Locale.US, "Range       : %s - %s (%.1fs)", TimeFormatter.formatTimestamp(clip.startSec), TimeFormatter.formatTimestamp(clip.endSec), clip.durationSec))
        appendLine("Hype Score  : ${clip.hypeScore}/100 | Quality: ${quality.label} | Mode: ${mode.label} | Audio Leveling: ${if (loudnorm) "ON" else "OFF"}")
        clip.superChat?.let { appendLine("Super Chat  : ${it.donor} (${it.amountDisplay}) — ${it.message}") }
        if (clip.reason.isNotBlank()) appendLine("Signals     : ${clip.reason}")
        if (clip.transcriptQuote.isNotBlank()) appendLine("\nTranscript Quote:\n\"${clip.transcriptQuote}\"")
    }
}
''')

    w(f"{PKG}/service/ClipExportService.kt", r'''
package com.clippulse.studio.service

import android.app.Service
import android.content.Context
import android.content.Intent
import android.content.pm.ServiceInfo
import android.os.Build
import android.os.IBinder
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import androidx.core.app.ServiceCompat
import androidx.core.content.ContextCompat
import com.clippulse.studio.data.AiConfigStore
import com.clippulse.studio.engine.ClipExporter
import com.clippulse.studio.model.*
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

object ExportProgressBus {
    private val _state = MutableStateFlow<ExportJobState>(ExportJobState.Idle)
    val state: StateFlow<ExportJobState> = _state.asStateFlow()
    private val _historyVersion = MutableStateFlow(0)
    val historyVersion: StateFlow<Int> = _historyVersion.asStateFlow()

    @Volatile var pendingClips: List<ClipCandidate> = emptyList()
    fun update(s: ExportJobState) { _state.value = s }
    fun bumpHistory() { _historyVersion.value += 1 }
    fun reset() { _state.value = ExportJobState.Idle }
}

class ClipExportService : Service() {
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
    private var activeJob: Job? = null

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        if (intent?.action == ACTION_CANCEL) {
            activeJob?.cancel()
            ExportProgressBus.update(ExportJobState.Failed("Export canceled by user."))
            stopForeground(STOP_FOREGROUND_REMOVE)
            stopSelf()
            return START_NOT_STICKY
        }

        val url = intent?.getStringExtra("url").orEmpty()
        val isLocal = intent?.getBooleanExtra("local", false) ?: false
        val localPath = intent?.getStringExtra("path")
        val title = intent?.getStringExtra("title").orEmpty()
        val quality = runCatching { DownloadQuality.valueOf(intent?.getStringExtra("quality") ?: "") }.getOrDefault(DownloadQuality.Q_1080P)
        val mode = runCatching { ExportMode.valueOf(intent?.getStringExtra("mode") ?: "") }.getOrDefault(ExportMode.FAST_COPY)
        val burnSc = intent?.getBooleanExtra("burnSc", true) ?: true
        val loudnorm = intent?.getBooleanExtra("loudnorm", true) ?: true
        val txt = intent?.getBooleanExtra("txt", true) ?: true
        val clips = ExportProgressBus.pendingClips

        val fgType = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) ServiceInfo.FOREGROUND_SERVICE_TYPE_DATA_SYNC else 0
        ServiceCompat.startForeground(this, 4102, buildNotif("ClipPulse Exporting", "Preparing ${clips.size} clip(s)...", 0, clips.size.coerceAtLeast(1), true), fgType)

        if (clips.isEmpty() || url.isBlank()) {
            ExportProgressBus.update(ExportJobState.Failed("No clips selected."))
            stopSelf()
            return START_NOT_STICKY
        }

        val store = AiConfigStore(applicationContext)
        activeJob?.cancel()
        activeJob = scope.launch {
            val saved = mutableListOf<String>()
            var err: String? = null
            for ((i, c) in clips.withIndex()) {
                if (!isActive) break
                ExportProgressBus.update(ExportJobState.Running(i + 1, clips.size, c.viralTitle.ifBlank { c.title }, i.toFloat() / clips.size))
                notifySafe(4102, "Exporting ${i + 1}/${clips.size}", c.title, i, clips.size, true)
                ClipExporter.exportSingleClip(applicationContext, url, isLocal, localPath, title, c, i, quality, mode, burnSc, loudnorm, txt)
                    .fold(
                        onSuccess = { rec ->
                            saved.add(rec.displayPath)
                            store.appendDownloadRecord(rec)
                            ExportProgressBus.bumpHistory()
                        },
                        onFailure = { err = it.message }
                    )
            }
            if (isActive) {
                if (saved.isNotEmpty()) {
                    ExportProgressBus.update(ExportJobState.Completed(saved.size, saved))
                    notifySafe(4103, "Export Complete", "Saved ${saved.size} clip(s) to Movies/ClipPulse", 0, 0, false)
                } else {
                    ExportProgressBus.update(ExportJobState.Failed(err ?: "Export failed"))
                    notifySafe(4103, "Export Failed", err ?: "Export failed", 0, 0, false)
                }
            }
            stopForeground(STOP_FOREGROUND_DETACH)
            stopSelf()
        }
        return START_NOT_STICKY
    }

    override fun onDestroy() { scope.cancel(); super.onDestroy() }

    private fun buildNotif(title: String, text: String, prog: Int, max: Int, ongoing: Boolean) =
        NotificationCompat.Builder(this, CHANNEL_ID).setSmallIcon(android.R.drawable.stat_sys_download)
            .setContentTitle(title).setContentText(text).setOnlyAlertOnce(true).setOngoing(ongoing)
            .apply { if (ongoing) setProgress(max, prog, false) else setAutoCancel(true) }.build()

    private fun notifySafe(id: Int, title: String, text: String, prog: Int, max: Int, ongoing: Boolean) {
        try { NotificationManagerCompat.from(this).notify(id, buildNotif(title, text, prog, max, ongoing)) } catch (_: SecurityException) {}
    }

    companion object {
        const val CHANNEL_ID = "clippulse_export_channel"
        private const val ACTION_CANCEL = "com.clippulse.studio.ACTION_CANCEL_EXPORT"

        fun startExport(
            ctx: Context, url: String, isLocal: Boolean, localPath: String?, title: String,
            clips: List<ClipCandidate>, quality: DownloadQuality, mode: ExportMode, burnSc: Boolean, loudnorm: Boolean, txt: Boolean
        ) {
            ExportProgressBus.pendingClips = clips
            ContextCompat.startForegroundService(ctx, Intent(ctx, ClipExportService::class.java).apply {
                putExtra("url", url); putExtra("local", isLocal); putExtra("path", localPath)
                putExtra("title", title); putExtra("quality", quality.name); putExtra("mode", mode.name)
                putExtra("burnSc", burnSc); putExtra("loudnorm", loudnorm); putExtra("txt", txt)
            })
        }

        fun cancelExport(ctx: Context) {
            runCatching { ctx.startService(Intent(ctx, ClipExportService::class.java).apply { action = ACTION_CANCEL }) }
            ExportProgressBus.update(ExportJobState.Failed("Export canceled."))
        }
    }
}
''')

    w(f"{PKG}/viewmodel/ClipPulseViewModel.kt", r'''
package com.clippulse.studio.viewmodel

import android.app.Application
import android.net.Uri
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.clippulse.studio.data.AiConfigStore
import com.clippulse.studio.data.DownloadSettings
import com.clippulse.studio.engine.*
import com.clippulse.studio.model.*
import com.clippulse.studio.network.UniversalAiClient
import com.clippulse.studio.service.ClipExportService
import com.clippulse.studio.service.ExportProgressBus
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import java.nio.charset.StandardCharsets
import java.util.UUID
import kotlin.math.abs

data class StudioUiState(
    val activeTab: StudioTab = StudioTab.STUDIO,
    val sourceInput: String = "", val detectionMode: DetectionMode = DetectionMode.SMART_ALL,
    val customAiPrompt: String = "", val superChatThreshold: SuperChatThreshold = SuperChatThreshold.ALL,
    val paddingPreset: PaddingPreset = PaddingPreset.BALANCED, val isAnalyzing: Boolean = false,
    val analysisProgress: Float = 0f, val analysisStatus: String = "", val analysisError: String? = null,
    val analysisResult: VideoAnalysisResult? = null, val activeSignalFilter: SignalSource? = null,
    val expandedClipId: String? = null, val focusedClipId: String? = null,
    val resolvedStreamInfo: PlayableStreamInfo? = null, val isResolvingPreview: Boolean = false, val previewError: String? = null,
    val scanHistory: List<VideoAnalysisResult> = emptyList(),
    val hasCookiesLoaded: Boolean = false,
    val downloadSettings: DownloadSettings = DownloadSettings(),
    val downloadHistory: List<ExportedClipRecord> = emptyList(),
    val aiConfig: AiConfig = AiConfig(), val aiConnectionState: AiConnectionState = AiConnectionState.Idle,
    val isFetchingModels: Boolean = false, val modelFetchError: String? = null,
    val isAiSheetOpen: Boolean = false, val isUpdatingYtDlp: Boolean = false, val ytDlpUpdateStatus: String? = null
)

class ClipPulseViewModel(app: Application) : AndroidViewModel(app) {
    private val store = AiConfigStore(app)
    private val aiClient = UniversalAiClient()
    private val engine = VideoAnalysisEngine(aiClient)
    private val _ui = MutableStateFlow(
        StudioUiState(
            aiConfig = store.load(),
            downloadSettings = store.loadDownloadSettings(),
            downloadHistory = store.loadDownloadHistory(),
            scanHistory = store.loadScanHistory(),
            hasCookiesLoaded = store.getCookiesFile() != null
        )
    )
    val uiState: StateFlow<StudioUiState> = _ui.asStateFlow()
    val exportState: StateFlow<ExportJobState> = ExportProgressBus.state

    init {
        viewModelScope.launch {
            ExportProgressBus.historyVersion.collect {
                _ui.update { it.copy(downloadHistory = store.loadDownloadHistory()) }
            }
        }
    }

    fun selectTab(tab: StudioTab) = _ui.update { it.copy(activeTab = tab) }
    fun updateSourceInput(v: String) = _ui.update { it.copy(sourceInput = v, analysisError = null) }
    fun pasteAndNormalize(raw: String) {
        val clean = UrlNormalizer.extractAndNormalize(raw)
        if (clean.isNotBlank()) _ui.update { it.copy(sourceInput = clean, analysisError = null) }
    }
    fun onSharedUrlReceived(u: String) = _ui.update { it.copy(activeTab = StudioTab.STUDIO, sourceInput = UrlNormalizer.extractAndNormalize(u), analysisError = null) }
    fun setDetectionMode(m: DetectionMode) = _ui.update { it.copy(detectionMode = m) }
    fun setCustomAiPrompt(p: String) = _ui.update { it.copy(customAiPrompt = p) }
    fun setSuperChatThreshold(t: SuperChatThreshold) = _ui.update { it.copy(superChatThreshold = t) }
    fun setPaddingPreset(p: PaddingPreset) = _ui.update { it.copy(paddingPreset = p) }
    fun setSignalFilter(s: SignalSource?) = _ui.update { it.copy(activeSignalFilter = s) }
    fun dismissExportStatus() = ExportProgressBus.reset()
    fun setAiSheetOpen(open: Boolean) = _ui.update { it.copy(isAiSheetOpen = open) }

    fun toggleClipExpanded(id: String) {
        val opening = _ui.value.expandedClipId != id
        _ui.update { it.copy(expandedClipId = if (opening) id else null, previewError = null) }
        if (opening) ensureLiveStreamPreviewUrl()
    }

    private fun ensureLiveStreamPreviewUrl() {
        val res = _ui.value.analysisResult ?: return
        if (res.isLocalFile) return
        if (_ui.value.resolvedStreamInfo != null || _ui.value.isResolvingPreview) return
        viewModelScope.launch {
            _ui.update { it.copy(isResolvingPreview = true, previewError = null) }
            StreamPreviewResolver.resolvePlayableStream(getApplication(), res.sourceUrlOrUri).fold(
                onSuccess = { info -> _ui.update { it.copy(resolvedStreamInfo = info, isResolvingPreview = false) } },
                onFailure = { err -> _ui.update { it.copy(isResolvingPreview = false, previewError = err.message ?: "Preview unavailable") } }
            )
        }
    }

    fun focusClipAtTime(sec: Double) {
        val clips = _ui.value.analysisResult?.clips ?: return
        val nearest = clips.minByOrNull { abs(((it.startSec + it.endSec) / 2.0) - sec) } ?: return
        _ui.update { it.copy(focusedClipId = nearest.id, expandedClipId = nearest.id) }
        ensureLiveStreamPreviewUrl()
    }

    fun toggleClipSelected(id: String) = _ui.update { st ->
        val r = st.analysisResult ?: return@update st
        val updated = r.copy(clips = r.clips.map { if (it.id == id) it.copy(selected = !it.selected) else it })
        store.saveScanToHistory(updated)
        st.copy(analysisResult = updated, scanHistory = store.loadScanHistory())
    }

    fun selectAllClips(sel: Boolean) = _ui.update { st ->
        val r = st.analysisResult ?: return@update st
        val f = st.activeSignalFilter
        val updated = r.copy(clips = r.clips.map { if (f == null || f in it.signals) it.copy(selected = sel) else it })
        store.saveScanToHistory(updated)
        st.copy(analysisResult = updated, scanHistory = store.loadScanHistory())
    }

    fun updateClipRange(id: String, newStartSec: Double, newEndSec: Double) = _ui.update { st ->
        val r = st.analysisResult ?: return@update st
        val maxD = r.durationSec.coerceAtLeast(2.0)
        val safeS = newStartSec.coerceIn(0.0, (maxD - 2.0).coerceAtLeast(0.0))
        val safeE = newEndSec.coerceIn((safeS + 2.0).coerceAtMost(maxD), maxD)
        val updated = r.copy(clips = r.clips.map { if (it.id == id) it.copy(startSec = safeS, endSec = safeE) else it })
        store.saveScanToHistory(updated)
        st.copy(analysisResult = updated, scanHistory = store.loadScanHistory())
    }

    fun nudgeClipStart(id: String, delta: Double) {
        val clip = _ui.value.analysisResult?.clips?.firstOrNull { it.id == id } ?: return
        updateClipRange(id, clip.startSec + delta, clip.endSec)
    }

    fun nudgeClipEnd(id: String, delta: Double) {
        val clip = _ui.value.analysisResult?.clips?.firstOrNull { it.id == id } ?: return
        updateClipRange(id, clip.startSec, clip.endSec + delta)
    }

    fun addManualClip(startRaw: String, endRaw: String, customTitle: String) {
        val r = _ui.value.analysisResult ?: return
        val s = TimeFormatter.parseTimestampToSec(startRaw) ?: return
        val e = TimeFormatter.parseTimestampToSec(endRaw) ?: return
        val maxD = r.durationSec.coerceAtLeast(5.0)
        val safeS = s.coerceIn(0.0, (maxD - 2.0).coerceAtLeast(0.0))
        val safeE = e.coerceIn((safeS + 2.0).coerceAtMost(maxD), maxD)
        val title = customTitle.trim().ifBlank { "Manual Clip (${TimeFormatter.formatTimestamp(safeS)})" }
        val newClip = ClipCandidate(
            id = UUID.randomUUID().toString(), title = title, startSec = safeS, endSec = safeE,
            hypeScore = 90, signals = listOf(SignalSource.AI_PICK), isMultiSignal = false,
            reason = "Custom timestamp selection", viralTitle = title,
            socialCaption = "Watch this highlight from ${r.videoTitle}", hashtags = "#shorts #viral #clips", selected = true
        )
        val updated = r.copy(clips = listOf(newClip) + r.clips)
        store.saveScanToHistory(updated)
        _ui.update {
            it.copy(analysisResult = updated, scanHistory = store.loadScanHistory(), expandedClipId = newClip.id, focusedClipId = newClip.id)
        }
        ensureLiveStreamPreviewUrl()
    }

    // Scan History Actions
    fun loadCachedScan(scan: VideoAnalysisResult) {
        val firstId = scan.clips.firstOrNull()?.id
        _ui.update {
            it.copy(
                activeTab = StudioTab.STUDIO,
                sourceInput = scan.sourceUrlOrUri,
                analysisResult = scan,
                analysisError = null,
                activeSignalFilter = null,
                expandedClipId = firstId,
                focusedClipId = firstId,
                resolvedStreamInfo = null,
                previewError = null
            )
        }
        if (firstId != null && !scan.isLocalFile) ensureLiveStreamPreviewUrl()
    }

    fun clearScanHistory() {
        store.clearScanHistory()
        _ui.update { it.copy(scanHistory = emptyList()) }
    }

    // Cookies.txt Login Actions
    fun importCookiesUri(uri: Uri) {
        viewModelScope.launch(Dispatchers.IO) {
            val ok = runCatching {
                getApplication<Application>().contentResolver.openInputStream(uri)?.use { inp ->
                    store.saveCookiesText(inp.bufferedReader(StandardCharsets.UTF_8).readText())
                } ?: false
            }.getOrDefault(false)
            if (ok) {
                StreamPreviewResolver.clearCache()
                _ui.update { it.copy(hasCookiesLoaded = true, ytDlpUpdateStatus = "Login cookies.txt imported successfully!") }
            } else {
                _ui.update { it.copy(ytDlpUpdateStatus = "Could not read selected cookies file.") }
            }
        }
    }

    fun clearCookies() {
        store.clearCookies()
        StreamPreviewResolver.clearCache()
        _ui.update { it.copy(hasCookiesLoaded = false, ytDlpUpdateStatus = "Login cookies cleared.") }
    }

    // Download Settings Controls
    private fun saveDl(fn: (DownloadSettings) -> DownloadSettings) = _ui.update { st ->
        val u = fn(st.downloadSettings); store.saveDownloadSettings(u); st.copy(downloadSettings = u)
    }
    fun setDownloadQuality(q: DownloadQuality) = saveDl { it.copy(quality = q) }
    fun setExportMode(m: ExportMode) = saveDl { it.copy(exportMode = m) }
    fun toggleBurnSuperChatOverlay() = saveDl { it.copy(burnSuperChatOverlay = !it.burnSuperChatOverlay) }
    fun toggleLoudnorm() = saveDl { it.copy(loudnormEnabled = !it.loudnormEnabled) }
    fun toggleIncludeTxtNotes() = saveDl { it.copy(includeTxtNotes = !it.includeTxtNotes) }
    fun clearDownloadHistory() {
        store.saveDownloadHistory(emptyList())
        _ui.update { it.copy(downloadHistory = emptyList()) }
    }

    fun analyzeRemoteUrl() {
        val normalized = UrlNormalizer.extractAndNormalize(_ui.value.sourceInput)
        if (normalized.isBlank()) { _ui.update { it.copy(analysisError = "Paste a YouTube or Facebook link first.") }; return }
        if (_ui.value.isAnalyzing) return
        viewModelScope.launch {
            _ui.update {
                it.copy(
                    sourceInput = normalized, isAnalyzing = true, analysisProgress = 0.05f,
                    analysisStatus = "Starting zero-download scan...", analysisError = null,
                    resolvedStreamInfo = null, previewError = null
                )
            }
            val s = _ui.value
            engine.analyzeRemoteUrl(getApplication(), normalized, s.detectionMode, s.superChatThreshold, s.paddingPreset, s.customAiPrompt, s.aiConfig) { p, msg ->
                _ui.update { it.copy(analysisProgress = p, analysisStatus = msg) }
            }.fold(
                onSuccess = { res ->
                    val firstId = res.clips.firstOrNull()?.id
                    _ui.update {
                        it.copy(
                            isAnalyzing = false, analysisProgress = 1f, analysisResult = res,
                            scanHistory = store.loadScanHistory(), activeSignalFilter = null,
                            expandedClipId = firstId, focusedClipId = firstId
                        )
                    }
                    if (firstId != null) ensureLiveStreamPreviewUrl()
                },
                onFailure = { err -> _ui.update { it.copy(isAnalyzing = false, analysisError = err.message ?: "Analysis failed") } }
            )
        }
    }

    fun analyzeLocalVideoUri(uri: Uri) {
        if (_ui.value.isAnalyzing) return
        viewModelScope.launch {
            _ui.update {
                it.copy(
                    sourceInput = uri.toString(), isAnalyzing = true, analysisProgress = 0.05f,
                    analysisStatus = "Loading local video...", analysisError = null,
                    resolvedStreamInfo = null, previewError = null
                )
            }
            engine.analyzeLocalVideo(getApplication(), uri, _ui.value.paddingPreset) { p, msg ->
                _ui.update { it.copy(analysisProgress = p, analysisStatus = msg) }
            }.fold(
                onSuccess = { res ->
                    val firstId = res.clips.firstOrNull()?.id
                    _ui.update {
                        it.copy(
                            isAnalyzing = false, analysisProgress = 1f, analysisResult = res,
                            scanHistory = store.loadScanHistory(), activeSignalFilter = null,
                            expandedClipId = firstId, focusedClipId = firstId
                        )
                    }
                },
                onFailure = { err -> _ui.update { it.copy(isAnalyzing = false, analysisError = err.message ?: "Local scan failed") } }
            )
        }
    }

    fun exportSelectedClips() {
        val s = _ui.value; val r = s.analysisResult ?: return
        val chosen = r.clips.filter { it.selected }
        if (chosen.isNotEmpty()) {
            val dl = s.downloadSettings
            ClipExportService.startExport(
                getApplication(), r.sourceUrlOrUri, r.isLocalFile, r.localFilePath, r.videoTitle,
                chosen, dl.quality, dl.exportMode, dl.burnSuperChatOverlay, dl.loudnormEnabled, dl.includeTxtNotes
            )
            _ui.update { it.copy(activeTab = StudioTab.DOWNLOADS) }
        }
    }

    fun cancelActiveExport() = ClipExportService.cancelExport(getApplication())

    private fun saveCfg(fn: (AiConfig) -> AiConfig) = _ui.update { st -> val u = fn(st.aiConfig); store.save(u); st.copy(aiConfig = u, modelFetchError = null) }
    fun selectAiPreset(p: AiPreset) = saveCfg { it.copy(preset = p, baseUrl = p.defaultBaseUrl, selectedModel = p.defaultModel) }
    fun updateAiBaseUrl(u: String) = saveCfg { it.copy(baseUrl = u) }
    fun updatePrimaryApiKey(k: String) = saveCfg { it.copy(primaryKey = k) }
    fun addBackupApiKey(k: String) { if (k.isNotBlank()) saveCfg { it.copy(backupKeys = (it.backupKeys + k.trim()).distinct()) } }
    fun removeBackupApiKey(k: String) = saveCfg { it.copy(backupKeys = it.backupKeys.filterNot { x -> x == k }) }
    fun selectAiModel(m: String) = saveCfg { it.copy(selectedModel = m) }
    fun setSmartPeakOnly(e: Boolean) = saveCfg { it.copy(smartPeakOnly = e) }
    fun setOfflineNoAiMode(e: Boolean) = saveCfg { it.copy(offlineNoAiMode = e) }

    fun fetchAvailableModels() {
        val cfg = _ui.value.aiConfig.copy(baseUrl = AiConfigStore.normalizeBaseUrl(_ui.value.aiConfig.baseUrl))
        store.save(cfg)
        viewModelScope.launch {
            _ui.update { it.copy(aiConfig = cfg, isFetchingModels = true, modelFetchError = null) }
            aiClient.fetchModels(cfg).fold(
                onSuccess = { models ->
                    val u = cfg.copy(availableModels = models, selectedModel = if (cfg.selectedModel in models) cfg.selectedModel else models.first())
                    store.save(u); _ui.update { it.copy(aiConfig = u, isFetchingModels = false) }
                },
                onFailure = { e -> _ui.update { it.copy(isFetchingModels = false, modelFetchError = e.message) } }
            )
        }
    }

    fun testAiConnection() {
        val cfg = _ui.value.aiConfig.copy(baseUrl = AiConfigStore.normalizeBaseUrl(_ui.value.aiConfig.baseUrl))
        store.save(cfg)
        viewModelScope.launch {
            _ui.update { it.copy(aiConfig = cfg, aiConnectionState = AiConnectionState.Testing) }
            _ui.update { it.copy(aiConnectionState = aiClient.testConnection(cfg)) }
        }
    }

    fun updateYtDlpBinary() {
        if (_ui.value.isUpdatingYtDlp) return
        viewModelScope.launch(Dispatchers.IO) {
            _ui.update { it.copy(isUpdatingYtDlp = true, ytDlpUpdateStatus = "Updating yt-dlp...") }
            EngineInitializer.updateYtDlpEngine(getApplication()).fold(
                onSuccess = { st -> StreamPreviewResolver.clearCache(); _ui.update { it.copy(isUpdatingYtDlp = false, ytDlpUpdateStatus = "yt-dlp: $st") } },
                onFailure = { e -> _ui.update { it.copy(isUpdatingYtDlp = false, ytDlpUpdateStatus = "Error: ${e.message}") } }
            )
        }
    }
}
''')

    w(f"{PKG}/ui/theme/Theme.kt", r'''
package com.clippulse.studio.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

val ObsidianBg = Color(0xFF0B0B0F)
val MatteSlate = Color(0xFF16161D)
val ElevatedSlate = Color(0xFF1F1F29)
val HairlineBorder = Color(0xFF262633)
val ElectricIndigo = Color(0xFF6366F1)
val ElectricIndigoLight = Color(0xFF818CF8)
val ColorGold = Color(0xFFF59E0B)
val ColorCrimson = Color(0xFFEF4444)
val ColorPurple = Color(0xFFA855F7)
val ColorCyan = Color(0xFF06B6D4)
val ColorEmerald = Color(0xFF10B981)
val TextPrimary = Color(0xFFF4F4F8)
val TextSecondary = Color(0xFF9CA3AF)
val TextMuted = Color(0xFF6B7280)

@Composable
fun ClipPulseTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = darkColorScheme(
            primary = ElectricIndigo, onPrimary = Color.White, secondary = ColorCyan,
            background = ObsidianBg, onBackground = TextPrimary, surface = MatteSlate,
            onSurface = TextPrimary, surfaceVariant = ElevatedSlate, onSurfaceVariant = TextSecondary,
            outline = HairlineBorder, error = ColorCrimson
        ),
        content = content
    )
}
''')

    w(f"{PKG}/ui/components/StudioComponents.kt", r'''
@file:OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class, androidx.media3.common.util.UnstableApi::class)

package com.clippulse.studio.ui.components

import android.net.Uri
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.*
import androidx.compose.foundation.gestures.detectHorizontalDragGestures
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.*
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.media3.common.MediaItem
import androidx.media3.common.Player
import androidx.media3.datasource.DefaultDataSource
import androidx.media3.datasource.DefaultHttpDataSource
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.exoplayer.source.DefaultMediaSourceFactory
import androidx.media3.ui.PlayerView
import com.clippulse.studio.data.AiConfigStore
import com.clippulse.studio.engine.PlayableStreamInfo
import com.clippulse.studio.engine.StreamPreviewResolver
import com.clippulse.studio.model.*
import com.clippulse.studio.ui.theme.*
import kotlinx.coroutines.delay
import java.io.File
import java.util.Locale

@Composable
fun ClipPulseLogo(modifier: Modifier = Modifier.size(34.dp)) {
    Canvas(modifier = modifier) {
        val w = size.width; val h = size.height
        drawRoundRect(MatteSlate, size = Size(w, h), cornerRadius = CornerRadius(w * 0.24f, h * 0.24f))
        drawRoundRect(Brush.linearGradient(listOf(ElectricIndigo, ColorCyan)), size = Size(w, h), cornerRadius = CornerRadius(w * 0.24f, h * 0.24f), style = Stroke(w * 0.06f))
        val p = Path().apply {
            moveTo(w * 0.16f, h * 0.54f); lineTo(w * 0.30f, h * 0.54f); lineTo(w * 0.39f, h * 0.28f)
            lineTo(w * 0.50f, h * 0.76f); lineTo(w * 0.61f, h * 0.34f); lineTo(w * 0.70f, h * 0.58f); lineTo(w * 0.84f, h * 0.54f)
        }
        drawPath(p, Brush.horizontalGradient(listOf(ElectricIndigo, ColorCyan)), style = Stroke(w * 0.085f, cap = StrokeCap.Round, join = StrokeJoin.Round))
        drawCircle(ColorGold, radius = w * 0.08f, center = Offset(w * 0.78f, h * 0.24f))
    }
}

@Composable
fun InteractiveHeatmapTimeline(durationSec: Double, heatmap: List<HeatmapPoint>, clips: List<ClipCandidate>, focusedClipId: String?, onJumpToTime: (Double) -> Unit) {
    val safeDur = durationSec.coerceAtLeast(1.0)
    Surface(modifier = Modifier.fillMaxWidth(), color = MatteSlate, shape = RoundedCornerShape(16.dp), border = BorderStroke(1.dp, HairlineBorder)) {
        Column(modifier = Modifier.padding(14.dp)) {
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                Text("REPLAY HEATMAP & TIMELINE", color = TextSecondary, fontSize = 11.sp, fontWeight = FontWeight.SemiBold)
                Text("Tap to jump", color = TextMuted, fontSize = 11.sp)
            }
            Spacer(Modifier.height(8.dp))
            Canvas(modifier = Modifier.fillMaxWidth().height(82.dp)
                .pointerInput(safeDur, clips) { detectTapGestures { onJumpToTime((it.x / size.width).coerceIn(0f, 1f) * safeDur) } }
                .pointerInput(safeDur, clips) { detectHorizontalDragGestures { ch, _ -> onJumpToTime((ch.position.x / size.width).coerceIn(0f, 1f) * safeDur) } }
            ) {
                val w = size.width; val h = size.height
                drawRoundRect(ElevatedSlate, size = Size(w, h))
                if (heatmap.size >= 2) {
                    val line = Path(); val fill = Path()
                    heatmap.forEachIndexed { i, pt ->
                        val x = (((pt.startSec + pt.endSec) / 2.0 / safeDur).toFloat().coerceIn(0f, 1f)) * w
                        val y = h - (pt.value.toFloat().coerceIn(0.05f, 1f) * (h * 0.82f)) - (h * 0.06f)
                        if (i == 0) { line.moveTo(0f, y); fill.moveTo(0f, h); fill.lineTo(0f, y) }
                        line.lineTo(x, y); fill.lineTo(x, y)
                        if (i == heatmap.lastIndex) { line.lineTo(w, y); fill.lineTo(w, y); fill.lineTo(w, h); fill.close() }
                    }
                    drawPath(fill, Brush.verticalGradient(listOf(ColorCrimson.copy(alpha = 0.34f), ElectricIndigo.copy(alpha = 0.06f))))
                    drawPath(line, Brush.horizontalGradient(listOf(ElectricIndigo, ColorCrimson, ColorGold)), style = Stroke(2.2.dp.toPx(), cap = StrokeCap.Round))
                }
                for (c in clips) {
                    val sx = ((c.startSec / safeDur).toFloat().coerceIn(0f, 1f)) * w
                    val ex = ((c.endSec / safeDur).toFloat().coerceIn(0f, 1f)) * w
                    val col = if (c.isMultiSignal) ColorGold else c.signals.firstOrNull()?.badgeColor ?: ElectricIndigo
                    val foc = c.id == focusedClipId
                    drawRect(col.copy(alpha = if (foc) 0.34f else 0.16f), topLeft = Offset(sx, 0f), size = Size((ex - sx).coerceAtLeast(3.dp.toPx()), h))
                    drawLine(if (foc) TextPrimary else col, Offset(sx, 0f), Offset(sx, h), strokeWidth = if (foc) 2.5.dp.toPx() else 1.5.dp.toPx())
                }
            }
            Spacer(Modifier.height(4.dp))
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                Text("00:00", color = TextMuted, fontSize = 11.sp)
                Text(TimeFormatter.formatTimestamp(safeDur / 2.0), color = TextMuted, fontSize = 11.sp)
                Text(TimeFormatter.formatTimestamp(safeDur), color = TextMuted, fontSize = 11.sp)
            }
        }
    }
}

@Composable
fun LiveClipPreviewPlayer(
    mediaUri: Uri,
    startSec: Double,
    endSec: Double,
    totalDurationSec: Double,
    isOnlineStream: Boolean,
    onRangeDragged: (Double, Double) -> Unit
) {
    val ctx = LocalContext.current
    var playing by remember { mutableStateOf(false) }
    var currentSec by remember { mutableStateOf(startSec) }

    // Drag-to-Trim RangeSlider window (±25s around the clip inside total video bounds)
    val safeTotal = totalDurationSec.coerceAtLeast(endSec + 5.0).coerceAtLeast(10.0)
    val windowMin = (startSec - 25.0).coerceAtLeast(0.0).toFloat()
    val windowMax = (endSec + 25.0).coerceAtMost(safeTotal).coerceAtLeast(windowMin + 5f).toFloat()
    var sliderRange by remember(startSec, endSec) { mutableStateOf(startSec.toFloat()..endSec.toFloat()) }

    val player = remember(mediaUri) {
        val httpFactory = DefaultHttpDataSource.Factory()
            .setUserAgent(StreamPreviewResolver.DESKTOP_UA)
            .setDefaultRequestProperties(mapOf("Referer" to "https://www.youtube.com/"))
            .setAllowCrossProtocolRedirects(true)
        val dataSourceFactory = DefaultDataSource.Factory(ctx, httpFactory)
        ExoPlayer.Builder(ctx)
            .setMediaSourceFactory(DefaultMediaSourceFactory(dataSourceFactory))
            .build()
            .apply {
                setMediaItem(MediaItem.fromUri(mediaUri))
                prepare()
                seekTo((startSec * 1000.0).toLong())
            }
    }

    LaunchedEffect(startSec) {
        player.seekTo((startSec * 1000.0).toLong())
        currentSec = startSec
    }

    LaunchedEffect(player, startSec, endSec) {
        while (true) {
            delay(220L)
            val posSec = player.currentPosition / 1000.0
            currentSec = posSec
            if (player.isPlaying && posSec >= endSec) {
                player.pause()
                player.seekTo((startSec * 1000.0).toLong())
            }
        }
    }

    DisposableEffect(player) {
        val l = object : Player.Listener {
            override fun onIsPlayingChanged(p: Boolean) { playing = p }
        }
        player.addListener(l)
        onDispose { player.removeListener(l); player.release() }
    }

    Surface(modifier = Modifier.fillMaxWidth(), color = ElevatedSlate, shape = RoundedCornerShape(12.dp), border = BorderStroke(1.dp, HairlineBorder)) {
        Column(Modifier.padding(8.dp)) {
            AndroidView(
                factory = { c -> PlayerView(c).apply { this.player = player; useController = false } },
                modifier = Modifier.fillMaxWidth().height(175.dp)
            )
            Spacer(Modifier.height(4.dp))
            val frac = (((currentSec - startSec) / (endSec - startSec).coerceAtLeast(0.5)).toFloat()).coerceIn(0f, 1f)
            LinearProgressIndicator(progress = { frac }, color = ElectricIndigo, trackColor = MatteSlate, modifier = Modifier.fillMaxWidth())

            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    IconButton(onClick = {
                        if (player.isPlaying) player.pause()
                        else {
                            if (player.currentPosition >= (endSec * 1000.0).toLong() || player.currentPosition < (startSec * 1000.0).toLong()) {
                                player.seekTo((startSec * 1000.0).toLong())
                            }
                            player.play()
                        }
                    }) {
                        Icon(if (playing) Icons.Rounded.Pause else Icons.Rounded.PlayArrow, "Play", tint = ElectricIndigoLight)
                    }
                    IconButton(onClick = { player.seekTo((startSec * 1000.0).toLong()); player.play() }) {
                        Icon(Icons.Rounded.Refresh, "Replay", tint = TextSecondary)
                    }
                    Text(if (isOnlineStream) "LIVE PREVIEW" else "LOCAL PREVIEW", color = ColorCyan, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                }
                Text("${TimeFormatter.formatTimestamp(currentSec.coerceIn(startSec, endSec))} / ${TimeFormatter.formatTimestamp(endSec)}", color = TextSecondary, fontSize = 11.sp)
            }

            // Drag-to-Trim RangeSlider directly on the video preview
            Text(
                text = "DRAG TO TRIM: ${TimeFormatter.formatTimestamp(sliderRange.start.toDouble())} – ${TimeFormatter.formatTimestamp(sliderRange.endInclusive.toDouble())}",
                color = ColorGold,
                fontSize = 10.sp,
                fontWeight = FontWeight.Bold
            )
            RangeSlider(
                value = sliderRange,
                onValueChange = { range ->
                    if (range.endInclusive - range.start >= 2f) {
                        sliderRange = range
                    }
                },
                onValueChangeFinished = {
                    onRangeDragged(sliderRange.start.toDouble(), sliderRange.endInclusive.toDouble())
                    player.seekTo((sliderRange.start * 1000f).toLong())
                },
                valueRange = windowMin..windowMax,
                colors = SliderDefaults.colors(
                    thumbColor = ColorGold,
                    activeTrackColor = ElectricIndigo,
                    inactiveTrackColor = MatteSlate
                ),
                modifier = Modifier.fillMaxWidth().height(32.dp)
            )
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun ClipCard(
    clip: ClipCandidate, totalDurationSec: Double, isExpanded: Boolean, isFocused: Boolean,
    localVideoPath: String?, resolvedStreamInfo: PlayableStreamInfo?, isResolvingPreview: Boolean, previewError: String?,
    onToggleSelect: () -> Unit, onToggleExpand: () -> Unit, onNudgeStart: (Double) -> Unit, onNudgeEnd: (Double) -> Unit,
    onRangeDragged: (Double, Double) -> Unit
) {
    val clipboard = LocalClipboardManager.current
    var copiedSocial by remember { mutableStateOf(false) }
    val border = when { isFocused -> ElectricIndigo; clip.isMultiSignal -> ColorGold.copy(alpha = 0.55f); else -> HairlineBorder }

    Surface(modifier = Modifier.fillMaxWidth(), color = MatteSlate, shape = RoundedCornerShape(16.dp), border = BorderStroke(if (isFocused) 1.5.dp else 1.dp, border)) {
        Column(Modifier.padding(12.dp)) {
            Row(modifier = Modifier.fillMaxWidth().clickable { onToggleExpand() }, verticalAlignment = Alignment.CenterVertically) {
                Checkbox(checked = clip.selected, onCheckedChange = { onToggleSelect() }, colors = CheckboxDefaults.colors(checkedColor = ElectricIndigo))
                Column(Modifier.weight(1f)) {
                    FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                        if (clip.isMultiSignal) BadgePill("\uD83D\uDD25 Multi-Signal", ColorGold)
                        clip.signals.forEach { BadgePill(it.label, it.badgeColor) }
                    }
                    Spacer(Modifier.height(5.dp))
                    Text(clip.viralTitle.ifBlank { clip.title }, color = TextPrimary, fontSize = 15.sp, fontWeight = FontWeight.SemiBold, maxLines = 2, overflow = TextOverflow.Ellipsis)
                    Text(String.format(Locale.US, "%s - %s • %.1fs", TimeFormatter.formatTimestamp(clip.startSec), TimeFormatter.formatTimestamp(clip.endSec), clip.durationSec), color = ElectricIndigoLight, fontSize = 12.sp)
                }
                Column(horizontalAlignment = Alignment.End) {
                    val hc = when { clip.hypeScore >= 88 -> ColorGold; clip.hypeScore >= 76 -> ColorEmerald; else -> ElectricIndigoLight }
                    Surface(color = hc.copy(alpha = 0.16f), shape = RoundedCornerShape(10.dp), border = BorderStroke(1.dp, hc.copy(alpha = 0.45f))) {
                        Column(Modifier.padding(horizontal = 9.dp, vertical = 4.dp), horizontalAlignment = Alignment.CenterHorizontally) {
                            Text("${clip.hypeScore}", color = hc, fontSize = 15.sp, fontWeight = FontWeight.Bold)
                            Text("HYPE", color = hc, fontSize = 9.sp, fontWeight = FontWeight.SemiBold)
                        }
                    }
                    Icon(if (isExpanded) Icons.Rounded.ExpandLess else Icons.Rounded.ExpandMore, "Expand", tint = TextSecondary)
                }
            }
            clip.superChat?.let { sc ->
                Spacer(Modifier.height(8.dp))
                Surface(modifier = Modifier.fillMaxWidth(), color = ColorGold.copy(alpha = 0.12f), shape = RoundedCornerShape(10.dp), border = BorderStroke(1.dp, ColorGold.copy(alpha = 0.4f))) {
                    Row(Modifier.padding(9.dp), verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Rounded.Paid, "Super Chat", tint = ColorGold, modifier = Modifier.size(18.dp))
                        Spacer(Modifier.width(8.dp))
                        Column {
                            Text("${sc.donor} • ${sc.amountDisplay}", color = ColorGold, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                            if (sc.message.isNotBlank()) Text(sc.message, color = TextPrimary, fontSize = 12.sp)
                        }
                    }
                }
            }
            if (clip.transcriptQuote.isNotBlank()) {
                Spacer(Modifier.height(6.dp))
                Text("\"${clip.transcriptQuote}\"", color = TextSecondary, fontSize = 12.sp, fontStyle = FontStyle.Italic, maxLines = if (isExpanded) 5 else 2, overflow = TextOverflow.Ellipsis)
            }
            AnimatedVisibility(visible = isExpanded) {
                Column(Modifier.padding(top = 10.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    HorizontalDivider(color = HairlineBorder)

                    when {
                        !localVideoPath.isNullOrBlank() -> {
                            LiveClipPreviewPlayer(Uri.fromFile(File(localVideoPath)), clip.startSec, clip.endSec, totalDurationSec, isOnlineStream = false, onRangeDragged = onRangeDragged)
                        }
                        resolvedStreamInfo != null -> {
                            LiveClipPreviewPlayer(Uri.parse(resolvedStreamInfo.url), clip.startSec, clip.endSec, totalDurationSec, isOnlineStream = true, onRangeDragged = onRangeDragged)
                        }
                        isResolvingPreview -> {
                            Surface(modifier = Modifier.fillMaxWidth(), color = ElevatedSlate, shape = RoundedCornerShape(12.dp)) {
                                Row(Modifier.padding(12.dp), verticalAlignment = Alignment.CenterVertically) {
                                    CircularProgressIndicator(modifier = Modifier.size(16.dp), strokeWidth = 2.dp, color = ColorCyan)
                                    Spacer(Modifier.width(10.dp))
                                    Text("Loading authenticated stream preview...", color = ColorCyan, fontSize = 12.sp)
                                }
                            }
                        }
                        previewError != null -> {
                            Text("Preview note: $previewError", color = TextMuted, fontSize = 11.sp)
                        }
                    }

                    Surface(modifier = Modifier.fillMaxWidth(), color = ElevatedSlate, shape = RoundedCornerShape(12.dp), border = BorderStroke(1.dp, ColorCyan.copy(alpha = 0.35f))) {
                        Column(Modifier.padding(10.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                Text("VIRAL TITLE & HASHTAG PACK", color = ColorCyan, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                                OutlinedButton(
                                    onClick = { clipboard.setText(AnnotatedString(clip.formattedSocialCopy())); copiedSocial = true },
                                    shape = RoundedCornerShape(8.dp), contentPadding = PaddingValues(horizontal = 8.dp, vertical = 2.dp), modifier = Modifier.height(26.dp)
                                ) {
                                    Icon(Icons.Rounded.ContentCopy, "Copy", modifier = Modifier.size(12.dp), tint = ColorCyan)
                                    Spacer(Modifier.width(4.dp))
                                    Text(if (copiedSocial) "Copied!" else "Copy Post", color = ColorCyan, fontSize = 10.sp)
                                }
                            }
                            Text(clip.viralTitle.ifBlank { clip.title }, color = TextPrimary, fontSize = 13.sp, fontWeight = FontWeight.SemiBold)
                            if (clip.socialCaption.isNotBlank()) Text(clip.socialCaption, color = TextSecondary, fontSize = 11.sp)
                            Text(clip.hashtags, color = ElectricIndigoLight, fontSize = 11.sp, fontWeight = FontWeight.Medium)
                        }
                    }

                    Surface(modifier = Modifier.fillMaxWidth(), color = ElevatedSlate, shape = RoundedCornerShape(12.dp), border = BorderStroke(1.dp, HairlineBorder)) {
                        Column(Modifier.padding(10.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                Text("Start: ${TimeFormatter.formatTimestamp(clip.startSec)}", color = TextPrimary, fontSize = 12.sp)
                                Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                                    NudgeBtn("-2s") { onNudgeStart(-2.0) }; NudgeBtn("+2s") { onNudgeStart(2.0) }
                                }
                            }
                            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                Text("End: ${TimeFormatter.formatTimestamp(clip.endSec)}", color = TextPrimary, fontSize = 12.sp)
                                Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                                    NudgeBtn("-2s") { onNudgeEnd(-2.0) }; NudgeBtn("+2s") { onNudgeEnd(2.0) }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun BadgePill(label: String, c: Color) {
    Surface(color = c.copy(alpha = 0.16f), shape = RoundedCornerShape(6.dp), border = BorderStroke(1.dp, c.copy(alpha = 0.45f))) {
        Text(label, color = c, fontSize = 10.sp, fontWeight = FontWeight.SemiBold, modifier = Modifier.padding(horizontal = 7.dp, vertical = 2.dp))
    }
}

@Composable
private fun NudgeBtn(label: String, onClick: () -> Unit) {
    OutlinedButton(onClick = onClick, shape = RoundedCornerShape(8.dp), border = BorderStroke(1.dp, HairlineBorder), contentPadding = PaddingValues(horizontal = 10.dp, vertical = 2.dp), modifier = Modifier.height(28.dp)) {
        Text(label, color = ElectricIndigoLight, fontSize = 11.sp, fontWeight = FontWeight.SemiBold)
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun AiManagerSheet(
    config: AiConfig, connectionState: AiConnectionState, isFetchingModels: Boolean, modelFetchError: String?,
    hasCookiesLoaded: Boolean, isUpdatingYtDlp: Boolean, ytDlpUpdateStatus: String?,
    onDismiss: () -> Unit, onSelectPreset: (AiPreset) -> Unit, onUpdateBaseUrl: (String) -> Unit,
    onUpdatePrimaryKey: (String) -> Unit, onAddBackupKey: (String) -> Unit, onRemoveBackupKey: (String) -> Unit,
    onSelectModel: (String) -> Unit, onFetchModels: () -> Unit, onTestConnect: () -> Unit,
    onToggleSmartPeakOnly: (Boolean) -> Unit, onToggleOfflineMode: (Boolean) -> Unit,
    onPickCookiesFile: () -> Unit, onClearCookies: () -> Unit, onUpdateYtDlp: () -> Unit
) {
    val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    var showKey by remember { mutableStateOf(false) }
    var backupInput by remember { mutableStateOf("") }
    var expanded by remember { mutableStateOf(false) }
    var filter by remember { mutableStateOf("") }

    ModalBottomSheet(onDismissRequest = onDismiss, sheetState = sheetState, containerColor = MatteSlate, contentColor = TextPrimary) {
        Column(modifier = Modifier.fillMaxWidth().verticalScroll(rememberScrollState()).padding(horizontal = 18.dp, vertical = 8.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Text("Universal AI API & Login Manager", color = TextPrimary, fontSize = 18.sp, fontWeight = FontWeight.Bold)
            FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                AiPreset.entries.forEach { p ->
                    FilterChip(selected = config.preset == p, onClick = { onSelectPreset(p) }, label = { Text(p.displayName, fontSize = 12.sp) })
                }
            }
            OutlinedTextField(value = config.baseUrl, onValueChange = onUpdateBaseUrl, label = { Text("Base URL") }, singleLine = true, modifier = Modifier.fillMaxWidth())
            Text("Normalized: ${AiConfigStore.normalizeBaseUrl(config.baseUrl)}", color = TextMuted, fontSize = 11.sp)
            OutlinedTextField(
                value = config.primaryKey, onValueChange = onUpdatePrimaryKey, label = { Text("Primary API Key") }, singleLine = true,
                visualTransformation = if (showKey) VisualTransformation.None else PasswordVisualTransformation(),
                trailingIcon = { IconButton(onClick = { showKey = !showKey }) { Icon(if (showKey) Icons.Rounded.VisibilityOff else Icons.Rounded.Visibility, "Show") } },
                modifier = Modifier.fillMaxWidth()
            )
            Surface(modifier = Modifier.fillMaxWidth(), color = ElevatedSlate, shape = RoundedCornerShape(12.dp), border = BorderStroke(1.dp, HairlineBorder)) {
                Column(Modifier.padding(10.dp)) {
                    Text("BACKUP FAILOVER KEYS (${config.backupKeys.size})", color = TextSecondary, fontSize = 11.sp, fontWeight = FontWeight.SemiBold)
                    Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                        OutlinedTextField(value = backupInput, onValueChange = { backupInput = it }, placeholder = { Text("Add backup key", fontSize = 12.sp) }, singleLine = true, modifier = Modifier.weight(1f))
                        IconButton(onClick = { onAddBackupKey(backupInput); backupInput = "" }) { Icon(Icons.Rounded.Add, "Add", tint = ElectricIndigoLight) }
                    }
                    config.backupKeys.forEachIndexed { idx, k ->
                        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                            Text("Key #${idx + 1}: ${if (k.length > 10) "${k.take(6)}••••${k.takeLast(4)}" else "••••"}", color = TextPrimary, fontSize = 12.sp)
                            IconButton(onClick = { onRemoveBackupKey(k) }, modifier = Modifier.size(28.dp)) { Icon(Icons.Rounded.Delete, "Del", tint = ColorCrimson, modifier = Modifier.size(16.dp)) }
                        }
                    }
                }
            }
            ExposedDropdownMenuBox(expanded = expanded, onExpandedChange = { expanded = !expanded }) {
                OutlinedTextField(
                    value = config.selectedModel, onValueChange = { onSelectModel(it); filter = it }, label = { Text("Model ID") }, singleLine = true,
                    trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) },
                    modifier = Modifier.menuAnchor(MenuAnchorType.PrimaryEditable, enabled = true).fillMaxWidth()
                )
                val matches = config.availableModels.filter { filter.isBlank() || it.contains(filter, ignoreCase = true) }
                ExposedDropdownMenu(expanded = expanded && matches.isNotEmpty(), onDismissRequest = { expanded = false }, modifier = Modifier.heightIn(max = 200.dp)) {
                    matches.forEach { id -> DropdownMenuItem(text = { Text(id, fontSize = 13.sp) }, onClick = { onSelectModel(id); filter = ""; expanded = false }) }
                }
            }
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                OutlinedButton(onClick = onFetchModels, enabled = !isFetchingModels, modifier = Modifier.weight(1f)) {
                    if (isFetchingModels) CircularProgressIndicator(Modifier.size(16.dp), strokeWidth = 2.dp) else Icon(Icons.Rounded.Refresh, "Fetch", Modifier.size(16.dp))
                    Spacer(Modifier.width(6.dp)); Text("Fetch Models", fontSize = 12.sp)
                }
                Button(onClick = onTestConnect, enabled = connectionState !is AiConnectionState.Testing, colors = ButtonDefaults.buttonColors(containerColor = ElectricIndigo), modifier = Modifier.weight(1f)) {
                    if (connectionState is AiConnectionState.Testing) CircularProgressIndicator(color = TextPrimary, modifier = Modifier.size(16.dp), strokeWidth = 2.dp) else Icon(Icons.Rounded.Bolt, "Connect", Modifier.size(16.dp))
                    Spacer(Modifier.width(6.dp)); Text("Connect", fontSize = 12.sp)
                }
            }
            if (modelFetchError != null) Text(modelFetchError, color = ColorCrimson, fontSize = 12.sp)
            when (connectionState) {
                is AiConnectionState.Connected -> Text("\u2713 Connected (${connectionState.latencyMs} ms) • ${connectionState.model}", color = ColorEmerald, fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
                is AiConnectionState.Error -> Text(connectionState.message, color = ColorCrimson, fontSize = 12.sp)
                else -> Unit
            }
            HorizontalDivider(color = HairlineBorder)
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text("Smart Peak-Only Mode (~85% token savings)", color = TextPrimary, fontSize = 13.sp, modifier = Modifier.weight(1f))
                Switch(checked = config.smartPeakOnly, onCheckedChange = onToggleSmartPeakOnly)
            }
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text("100% Offline / No-AI Mode", color = TextPrimary, fontSize = 13.sp, modifier = Modifier.weight(1f))
                Switch(checked = config.offlineNoAiMode, onCheckedChange = onToggleOfflineMode)
            }
            HorizontalDivider(color = HairlineBorder)

            // Login Support (cookies.txt importer)
            Text("YOUTUBE / FACEBOOK LOGIN COOKIES (cookies.txt)", color = TextSecondary, fontSize = 11.sp, fontWeight = FontWeight.Bold)
            Text("Bypass HTTP 403 anti-bot checks, age-restricted videos & members-only streams.", color = TextMuted, fontSize = 11.sp)
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                OutlinedButton(onClick = onPickCookiesFile, modifier = Modifier.weight(1f)) {
                    Icon(Icons.Rounded.VpnKey, "Cookies", Modifier.size(16.dp))
                    Spacer(Modifier.width(6.dp))
                    Text(if (hasCookiesLoaded) "\u2713 Replace cookies.txt" else "Import cookies.txt", fontSize = 12.sp)
                }
                if (hasCookiesLoaded) {
                    OutlinedButton(onClick = onClearCookies, border = BorderStroke(1.dp, ColorCrimson)) {
                        Text("Remove", color = ColorCrimson, fontSize = 12.sp)
                    }
                }
            }

            OutlinedButton(onClick = onUpdateYtDlp, enabled = !isUpdatingYtDlp, modifier = Modifier.fillMaxWidth()) {
                Icon(Icons.Rounded.Update, "Update", Modifier.size(16.dp)); Spacer(Modifier.width(8.dp))
                Text("Update yt-dlp Extractor Engine", fontSize = 12.sp)
            }
            if (ytDlpUpdateStatus != null) Text(ytDlpUpdateStatus, color = ElectricIndigoLight, fontSize = 12.sp)
            Spacer(Modifier.height(16.dp))
        }
    }
}
''')

    w(f"{PKG}/ui/ClipPulseStudioScreen.kt", r'''
@file:OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)

package com.clippulse.studio.ui

import android.Manifest
import android.content.Intent
import android.net.Uri
import android.os.Build
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.clippulse.studio.model.*
import com.clippulse.studio.ui.components.*
import com.clippulse.studio.ui.theme.*
import com.clippulse.studio.viewmodel.ClipPulseViewModel

@Composable
fun ClipPulseStudioScreen(viewModel: ClipPulseViewModel) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    val exportState by viewModel.exportState.collectAsStateWithLifecycle()
    val clipboard = LocalClipboardManager.current
    val ctx = LocalContext.current
    val picker = rememberLauncherForActivityResult(ActivityResultContracts.GetContent()) { uri -> if (uri != null) viewModel.analyzeLocalVideoUri(uri) }
    val cookiesPicker = rememberLauncherForActivityResult(ActivityResultContracts.GetContent()) { uri -> if (uri != null) viewModel.importCookiesUri(uri) }
    val notifPerm = rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()) { viewModel.exportSelectedClips() }

    var showManualDialog by remember { mutableStateOf(false) }

    val res = state.analysisResult
    val visible = res?.clips?.filter { state.activeSignalFilter == null || state.activeSignalFilter in it.signals }.orEmpty()
    val selectedCount = res?.clips?.count { it.selected } ?: 0
    val dl = state.downloadSettings

    Scaffold(
        containerColor = ObsidianBg,
        topBar = {
            Surface(color = ObsidianBg, modifier = Modifier.fillMaxWidth().statusBarsPadding()) {
                Column {
                    Row(Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            ClipPulseLogo(); Spacer(Modifier.width(10.dp))
                            Column {
                                Text("ClipPulse", color = TextPrimary, fontSize = 18.sp, fontWeight = FontWeight.Bold)
                                Text("Zero-Download Clip Studio", color = TextMuted, fontSize = 11.sp)
                            }
                        }
                        val (pillTxt, pillCol) = when {
                            state.aiConfig.offlineNoAiMode -> "Offline Mode" to TextSecondary
                            state.aiConnectionState is AiConnectionState.Connected -> "\u2713 ${(state.aiConnectionState as AiConnectionState.Connected).latencyMs}ms" to ColorEmerald
                            state.aiConnectionState is AiConnectionState.Error -> "AI Error" to ColorCrimson
                            state.aiConfig.primaryKey.isNotBlank() -> state.aiConfig.preset.displayName to ElectricIndigoLight
                            else -> "Setup AI" to ColorGold
                        }
                        Surface(onClick = { viewModel.setAiSheetOpen(true) }, color = pillCol.copy(alpha = 0.14f), shape = RoundedCornerShape(20.dp), border = BorderStroke(1.dp, pillCol.copy(alpha = 0.45f))) {
                            Text(pillTxt, color = pillCol, fontSize = 12.sp, fontWeight = FontWeight.SemiBold, modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp))
                        }
                    }

                    Row(Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 4.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        StudioTab.entries.forEach { tab ->
                            val selected = state.activeTab == tab
                            val badge = if (tab == StudioTab.DOWNLOADS) {
                                if (exportState is ExportJobState.Running) " (Active)" else " (${state.downloadHistory.size})"
                            } else ""
                            FilterChip(
                                selected = selected, onClick = { viewModel.selectTab(tab) },
                                leadingIcon = {
                                    Icon(if (tab == StudioTab.STUDIO) Icons.Rounded.AutoAwesome else Icons.Rounded.DownloadForOffline, tab.label, Modifier.size(16.dp))
                                },
                                label = { Text("${tab.label}$badge", fontSize = 12.sp, fontWeight = FontWeight.SemiBold) },
                                colors = FilterChipDefaults.filterChipColors(selectedContainerColor = ElectricIndigo, selectedLabelColor = TextPrimary, containerColor = MatteSlate, labelColor = TextSecondary),
                                modifier = Modifier.weight(1f)
                            )
                        }
                    }
                }
            }
        },
        bottomBar = {
            if (state.activeTab == StudioTab.STUDIO && res != null) {
                Surface(color = MatteSlate, border = BorderStroke(1.dp, HairlineBorder), modifier = Modifier.fillMaxWidth().navigationBarsPadding()) {
                    Column(Modifier.padding(horizontal = 16.dp, vertical = 10.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        Row(Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                            FilterChip(selected = dl.exportMode == ExportMode.FAST_COPY, onClick = { viewModel.setExportMode(ExportMode.FAST_COPY) }, label = { Text("Fast Cut", fontSize = 11.sp) })
                            FilterChip(selected = dl.exportMode == ExportMode.VERTICAL_CROP, onClick = { viewModel.setExportMode(ExportMode.VERTICAL_CROP) }, label = { Text("9:16 Crop", fontSize = 11.sp) })
                            FilterChip(selected = dl.burnSuperChatOverlay, onClick = viewModel::toggleBurnSuperChatOverlay, label = { Text("SC Overlay", fontSize = 11.sp) })
                            FilterChip(selected = dl.loudnormEnabled, onClick = viewModel::toggleLoudnorm, label = { Text("Audio Level", fontSize = 11.sp) })
                            FilterChip(selected = dl.includeTxtNotes, onClick = viewModel::toggleIncludeTxtNotes, label = { Text("+.TXT", fontSize = 11.sp) })
                        }
                        Button(
                            onClick = { if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) notifPerm.launch(Manifest.permission.POST_NOTIFICATIONS) else viewModel.exportSelectedClips() },
                            enabled = selectedCount > 0 && exportState !is ExportJobState.Running,
                            colors = ButtonDefaults.buttonColors(containerColor = ElectricIndigo), shape = RoundedCornerShape(12.dp),
                            modifier = Modifier.fillMaxWidth().height(46.dp)
                        ) {
                            Icon(Icons.Rounded.FileDownload, "Export", Modifier.size(18.dp)); Spacer(Modifier.width(8.dp))
                            Text("Export Selected Clips (${dl.quality.label}) ($selectedCount)", fontWeight = FontWeight.SemiBold, fontSize = 13.sp)
                        }
                    }
                }
            }
        }
    ) { pad ->
        if (state.activeTab == StudioTab.DOWNLOADS) {
            DownloadsControlCenter(
                modifier = Modifier.fillMaxSize().padding(pad),
                settings = dl, exportState = exportState, history = state.downloadHistory,
                onSelectQuality = viewModel::setDownloadQuality, onSelectMode = viewModel::setExportMode,
                onToggleBurnSc = viewModel::toggleBurnSuperChatOverlay,
                onToggleLoudnorm = viewModel::toggleLoudnorm, onToggleTxt = viewModel::toggleIncludeTxtNotes,
                onCancelExport = viewModel::cancelActiveExport, onDismissExport = viewModel::dismissExportStatus,
                onClearHistory = viewModel::clearDownloadHistory,
                onPlayRecord = { rec ->
                    runCatching {
                        ctx.startActivity(Intent(Intent.ACTION_VIEW).apply {
                            setDataAndType(Uri.parse(rec.contentUriString), "video/mp4")
                            addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                        })
                    }
                },
                onShareRecord = { rec ->
                    runCatching {
                        ctx.startActivity(Intent.createChooser(Intent(Intent.ACTION_SEND).apply {
                            type = "video/mp4"
                            putExtra(Intent.EXTRA_STREAM, Uri.parse(rec.contentUriString))
                            putExtra(Intent.EXTRA_TEXT, rec.title)
                            addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                        }, "Share Clip"))
                    }
                }
            )
        } else {
            LazyColumn(modifier = Modifier.fillMaxSize().padding(pad), contentPadding = PaddingValues(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
                item {
                    Surface(modifier = Modifier.fillMaxWidth(), color = MatteSlate, shape = RoundedCornerShape(18.dp), border = BorderStroke(1.dp, HairlineBorder)) {
                        Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                            OutlinedTextField(value = state.sourceInput, onValueChange = viewModel::updateSourceInput, placeholder = { Text("YouTube URL, Live VOD, or Facebook Video...", fontSize = 13.sp) }, singleLine = true, modifier = Modifier.fillMaxWidth())
                            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                OutlinedButton(onClick = { clipboard.getText()?.text?.let(viewModel::pasteAndNormalize) }, modifier = Modifier.weight(1f)) {
                                    Icon(Icons.Rounded.ContentPaste, "Paste", Modifier.size(16.dp)); Spacer(Modifier.width(6.dp)); Text("Paste Link", fontSize = 12.sp)
                                }
                                OutlinedButton(onClick = { picker.launch("video/*") }, modifier = Modifier.weight(1f)) {
                                    Icon(Icons.Rounded.VideoLibrary, "Local", Modifier.size(16.dp)); Spacer(Modifier.width(6.dp)); Text("Local Video", fontSize = 12.sp)
                                }
                            }
                            Row(Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                                DetectionMode.entries.forEach { m -> FilterChip(selected = state.detectionMode == m, onClick = { viewModel.setDetectionMode(m) }, label = { Text(m.label, fontSize = 11.sp) }) }
                            }
                            if (state.detectionMode == DetectionMode.AI_CUSTOM || state.detectionMode == DetectionMode.SMART_ALL) {
                                OutlinedTextField(value = state.customAiPrompt, onValueChange = viewModel::setCustomAiPrompt, placeholder = { Text("Optional AI prompt (e.g., \"every rage moment\")", fontSize = 12.sp) }, singleLine = true, modifier = Modifier.fillMaxWidth())
                            }
                            Row(Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.CenterVertically) {
                                Text("Super Chat:", color = TextMuted, fontSize = 11.sp)
                                SuperChatThreshold.entries.forEach { t -> FilterChip(selected = state.superChatThreshold == t, onClick = { viewModel.setSuperChatThreshold(t) }, label = { Text(t.label, fontSize = 11.sp) }) }
                            }
                            Row(Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.CenterVertically) {
                                Text("Padding:", color = TextMuted, fontSize = 11.sp)
                                PaddingPreset.entries.forEach { p -> FilterChip(selected = state.paddingPreset == p, onClick = { viewModel.setPaddingPreset(p) }, label = { Text(p.label, fontSize = 11.sp) }) }
                            }
                            Button(onClick = viewModel::analyzeRemoteUrl, enabled = !state.isAnalyzing, colors = ButtonDefaults.buttonColors(containerColor = ElectricIndigo), shape = RoundedCornerShape(12.dp), modifier = Modifier.fillMaxWidth().height(46.dp)) {
                                if (state.isAnalyzing) { CircularProgressIndicator(color = TextPrimary, modifier = Modifier.size(18.dp), strokeWidth = 2.dp); Spacer(Modifier.width(8.dp)); Text("Scanning Signals...") }
                                else { Icon(Icons.Rounded.AutoAwesome, "Analyze", Modifier.size(18.dp)); Spacer(Modifier.width(8.dp)); Text("Analyze Video (Zero-Download)", fontWeight = FontWeight.SemiBold) }
                            }
                            if (state.isAnalyzing) {
                                LinearProgressIndicator(progress = { state.analysisProgress }, color = ElectricIndigo, modifier = Modifier.fillMaxWidth())
                                Text(state.analysisStatus, color = ElectricIndigoLight, fontSize = 12.sp)
                            }
                            if (state.analysisError != null) Text(state.analysisError.orEmpty(), color = ColorCrimson, fontSize = 12.sp)
                        }
                    }
                }

                // Saved Scan History Bar (instant reload of past scans)
                if (state.scanHistory.isNotEmpty()) {
                    item {
                        Surface(modifier = Modifier.fillMaxWidth(), color = MatteSlate, shape = RoundedCornerShape(14.dp), border = BorderStroke(1.dp, HairlineBorder)) {
                            Column(Modifier.padding(10.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                    Text("RECENT SCANS (${state.scanHistory.size})", color = TextSecondary, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                                    Text("Tap to reload", color = TextMuted, fontSize = 10.sp)
                                }
                                Row(Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                                    state.scanHistory.forEach { past ->
                                        FilterChip(
                                            selected = res?.sourceUrlOrUri == past.sourceUrlOrUri,
                                            onClick = { viewModel.loadCachedScan(past) },
                                            label = { Text("${past.videoTitle.take(22)} (${past.clips.size})", fontSize = 11.sp) }
                                        )
                                    }
                                }
                            }
                        }
                    }
                }

                if (res != null) {
                    item {
                        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                            Surface(modifier = Modifier.fillMaxWidth(), color = MatteSlate, shape = RoundedCornerShape(14.dp), border = BorderStroke(1.dp, HairlineBorder)) {
                                Column(Modifier.padding(12.dp)) {
                                    Text(res.videoTitle, color = TextPrimary, fontSize = 15.sp, fontWeight = FontWeight.Bold, maxLines = 2, overflow = TextOverflow.Ellipsis)
                                    Text("${res.channelName} • ${res.analysisSummary}", color = TextSecondary, fontSize = 12.sp)
                                }
                            }
                            InteractiveHeatmapTimeline(res.durationSec, res.heatmap, res.clips, state.focusedClipId, viewModel::focusClipAtTime)
                            Row(Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                                FilterChip(selected = state.activeSignalFilter == null, onClick = { viewModel.setSignalFilter(null) }, label = { Text("All (${res.clips.size})", fontSize = 11.sp) })
                                SignalSource.entries.forEach { sig ->
                                    val cnt = res.clips.count { sig in it.signals }
                                    if (cnt > 0) FilterChip(selected = state.activeSignalFilter == sig, onClick = { viewModel.setSignalFilter(if (state.activeSignalFilter == sig) null else sig) }, label = { Text("${sig.label} ($cnt)", fontSize = 11.sp) })
                                }
                            }
                            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                Text("CLIPS ($selectedCount/${res.clips.size})", color = TextSecondary, fontSize = 11.sp, fontWeight = FontWeight.SemiBold)
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    TextButton(onClick = { showManualDialog = true }) { Text("+ Custom", color = ColorCyan, fontSize = 12.sp, fontWeight = FontWeight.Bold) }
                                    TextButton(onClick = { viewModel.selectAllClips(true) }) { Text("All", color = ElectricIndigoLight, fontSize = 12.sp) }
                                    TextButton(onClick = { viewModel.selectAllClips(false) }) { Text("Clear", color = TextSecondary, fontSize = 12.sp) }
                                }
                            }
                        }
                    }
                    items(items = visible, key = { it.id }) { clip ->
                        ClipCard(
                            clip = clip, totalDurationSec = res.durationSec,
                            isExpanded = state.expandedClipId == clip.id, isFocused = state.focusedClipId == clip.id,
                            localVideoPath = res.localFilePath, resolvedStreamInfo = state.resolvedStreamInfo,
                            isResolvingPreview = state.isResolvingPreview, previewError = state.previewError,
                            onToggleSelect = { viewModel.toggleClipSelected(clip.id) }, onToggleExpand = { viewModel.toggleClipExpanded(clip.id) },
                            onNudgeStart = { viewModel.nudgeClipStart(clip.id, it) }, onNudgeEnd = { viewModel.nudgeClipEnd(clip.id, it) },
                            onRangeDragged = { s, e -> viewModel.updateClipRange(clip.id, s, e) }
                        )
                    }
                }
            }
        }
    }

    if (showManualDialog) {
        var startTxt by remember { mutableStateOf("00:10") }
        var endTxt by remember { mutableStateOf("00:40") }
        var labelTxt by remember { mutableStateOf("") }
        AlertDialog(
            onDismissRequest = { showManualDialog = false },
            containerColor = MatteSlate,
            title = { Text("Add Custom Timestamp Clip", color = TextPrimary) },
            text = {
                Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    OutlinedTextField(value = startTxt, onValueChange = { startTxt = it }, label = { Text("Start (mm:ss or hh:mm:ss)") }, singleLine = true)
                    OutlinedTextField(value = endTxt, onValueChange = { endTxt = it }, label = { Text("End (mm:ss or hh:mm:ss)") }, singleLine = true)
                    OutlinedTextField(value = labelTxt, onValueChange = { labelTxt = it }, label = { Text("Clip Title (optional)") }, singleLine = true)
                }
            },
            confirmButton = { Button(onClick = { viewModel.addManualClip(startTxt, endTxt, labelTxt); showManualDialog = false }) { Text("Add Clip") } },
            dismissButton = { TextButton(onClick = { showManualDialog = false }) { Text("Cancel") } }
        )
    }

    if (state.isAiSheetOpen) {
        AiManagerSheet(
            state.aiConfig, state.aiConnectionState, state.isFetchingModels, state.modelFetchError,
            state.hasCookiesLoaded, state.isUpdatingYtDlp, state.ytDlpUpdateStatus,
            { viewModel.setAiSheetOpen(false) }, viewModel::selectAiPreset, viewModel::updateAiBaseUrl,
            viewModel::updatePrimaryApiKey, viewModel::addBackupApiKey, viewModel::removeBackupApiKey,
            viewModel::selectAiModel, viewModel::fetchAvailableModels, viewModel::testAiConnection,
            viewModel::setSmartPeakOnly, viewModel::setOfflineNoAiMode,
            { cookiesPicker.launch("*/*") }, viewModel::clearCookies, viewModel::updateYtDlpBinary
        )
    }
}

@Composable
private fun DownloadsControlCenter(
    modifier: Modifier,
    settings: com.clippulse.studio.data.DownloadSettings,
    exportState: ExportJobState,
    history: List<ExportedClipRecord>,
    onSelectQuality: (DownloadQuality) -> Unit,
    onSelectMode: (ExportMode) -> Unit,
    onToggleBurnSc: () -> Unit,
    onToggleLoudnorm: () -> Unit,
    onToggleTxt: () -> Unit,
    onCancelExport: () -> Unit,
    onDismissExport: () -> Unit,
    onClearHistory: () -> Unit,
    onPlayRecord: (ExportedClipRecord) -> Unit,
    onShareRecord: (ExportedClipRecord) -> Unit
) {
    LazyColumn(modifier = modifier, contentPadding = PaddingValues(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        item {
            Surface(modifier = Modifier.fillMaxWidth(), color = MatteSlate, shape = RoundedCornerShape(16.dp), border = BorderStroke(1.dp, HairlineBorder)) {
                Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("ACTIVE DOWNLOAD & EXPORT QUEUE", color = TextSecondary, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                    when (exportState) {
                        is ExportJobState.Running -> {
                            LinearProgressIndicator(progress = { exportState.progressFraction }, color = ElectricIndigo, modifier = Modifier.fillMaxWidth())
                            Text("Downloading & rendering ${exportState.currentIndex} of ${exportState.total}: ${exportState.currentTitle}", color = ElectricIndigoLight, fontSize = 13.sp)
                            OutlinedButton(onClick = onCancelExport, border = BorderStroke(1.dp, ColorCrimson)) {
                                Icon(Icons.Rounded.Stop, "Cancel", tint = ColorCrimson, modifier = Modifier.size(16.dp))
                                Spacer(Modifier.width(6.dp))
                                Text("Cancel Export", color = ColorCrimson, fontSize = 12.sp)
                            }
                        }
                        is ExportJobState.Completed -> {
                            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                Text("\u2713 Exported ${exportState.exportedCount} clip(s) to Movies/ClipPulse", color = ColorEmerald, fontSize = 13.sp, fontWeight = FontWeight.SemiBold, modifier = Modifier.weight(1f))
                                TextButton(onClick = onDismissExport) { Text("OK", color = ColorEmerald) }
                            }
                        }
                        is ExportJobState.Failed -> {
                            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                Text(exportState.error, color = ColorCrimson, fontSize = 12.sp, modifier = Modifier.weight(1f))
                                TextButton(onClick = onDismissExport) { Text("Dismiss", color = ColorCrimson) }
                            }
                        }
                        ExportJobState.Idle -> {
                            Text("No active downloads. Select clips in Clip Studio and tap Export to queue section downloads.", color = TextMuted, fontSize = 12.sp)
                        }
                    }
                }
            }
        }

        item {
            Surface(modifier = Modifier.fillMaxWidth(), color = MatteSlate, shape = RoundedCornerShape(16.dp), border = BorderStroke(1.dp, HairlineBorder)) {
                Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    Text("DOWNLOAD & ENCODING CONTROLS", color = TextSecondary, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                    Text("Max Video Resolution", color = TextPrimary, fontSize = 12.sp, fontWeight = FontWeight.Medium)
                    Row(Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                        DownloadQuality.entries.forEach { q ->
                            FilterChip(selected = settings.quality == q, onClick = { onSelectQuality(q) }, label = { Text(q.label, fontSize = 11.sp) })
                        }
                    }
                    Text("Framing & Cut Mode", color = TextPrimary, fontSize = 12.sp, fontWeight = FontWeight.Medium)
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        ExportMode.entries.forEach { m ->
                            FilterChip(selected = settings.exportMode == m, onClick = { onSelectMode(m) }, label = { Text(m.label, fontSize = 11.sp) })
                        }
                    }
                    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                        Column(Modifier.weight(1f)) {
                            Text("Burned-In Super Chat Card Overlay", color = TextPrimary, fontSize = 13.sp)
                            Text("Stamps donor name, tier color & message onto Super Chat clips", color = TextMuted, fontSize = 11.sp)
                        }
                        Switch(checked = settings.burnSuperChatOverlay, onCheckedChange = { onToggleBurnSc() })
                    }
                    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                        Column(Modifier.weight(1f)) {
                            Text("Broadcast Audio Leveling (loudnorm)", color = TextPrimary, fontSize = 13.sp)
                            Text("Normalizes volume to -16 LUFS for Shorts & Reels", color = TextMuted, fontSize = 11.sp)
                        }
                        Switch(checked = settings.loudnormEnabled, onCheckedChange = { onToggleLoudnorm() })
                    }
                    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                        Column(Modifier.weight(1f)) {
                            Text("Save Sidecar .TXT Viral Copy Pack", color = TextPrimary, fontSize = 13.sp)
                            Text("Saves title, hashtags & transcript to Documents/ClipPulse", color = TextMuted, fontSize = 11.sp)
                        }
                        Switch(checked = settings.includeTxtNotes, onCheckedChange = { onToggleTxt() })
                    }
                    Text("Gallery Output Folder: Internal Storage / Movies / ClipPulse", color = ColorCyan, fontSize = 11.sp)
                }
            }
        }

        item {
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text("DOWNLOADED CLIPS (${history.size})", color = TextSecondary, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                if (history.isNotEmpty()) {
                    TextButton(onClick = onClearHistory) { Text("Clear List", color = TextMuted, fontSize = 11.sp) }
                }
            }
        }

        if (history.isEmpty()) {
            item {
                Surface(modifier = Modifier.fillMaxWidth(), color = MatteSlate, shape = RoundedCornerShape(14.dp), border = BorderStroke(1.dp, HairlineBorder)) {
                    Text("Exported MP4 clips will appear here with instant Play & Share buttons.", color = TextMuted, fontSize = 12.sp, modifier = Modifier.padding(16.dp))
                }
            }
        } else {
            items(items = history, key = { it.id }) { rec ->
                Surface(modifier = Modifier.fillMaxWidth(), color = MatteSlate, shape = RoundedCornerShape(14.dp), border = BorderStroke(1.dp, HairlineBorder)) {
                    Column(Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                        Text(rec.title, color = TextPrimary, fontSize = 14.sp, fontWeight = FontWeight.SemiBold, maxLines = 2, overflow = TextOverflow.Ellipsis)
                        Text("${rec.qualityLabel} • ${rec.modeLabel} • ${TimeFormatter.formatTimestamp(rec.durationSec)} • ${TimeFormatter.formatFileSize(rec.sizeBytes)}", color = ElectricIndigoLight, fontSize = 11.sp)
                        Text(rec.displayPath, color = TextMuted, fontSize = 11.sp)
                        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            Button(onClick = { onPlayRecord(rec) }, colors = ButtonDefaults.buttonColors(containerColor = ElectricIndigo), contentPadding = PaddingValues(horizontal = 14.dp, vertical = 4.dp), modifier = Modifier.height(34.dp)) {
                                Icon(Icons.Rounded.PlayArrow, "Play", modifier = Modifier.size(16.dp)); Spacer(Modifier.width(4.dp)); Text("Play", fontSize = 12.sp)
                            }
                            OutlinedButton(onClick = { onShareRecord(rec) }, contentPadding = PaddingValues(horizontal = 14.dp, vertical = 4.dp), modifier = Modifier.height(34.dp)) {
                                Icon(Icons.Rounded.Share, "Share", modifier = Modifier.size(16.dp)); Spacer(Modifier.width(4.dp)); Text("Share", fontSize = 12.sp)
                            }
                        }
                    }
                }
            }
        }
    }
}
''')


def main() -> None:
    write_gradle_and_manifest()
    write_core_kotlin()
    write_network_and_engines()
    write_exporter_service_and_ui()
    print("\nClipPulse v2.0.0 Android project generated successfully!")


if __name__ == "__main__":
    main()
    sys.exit(0)


plugins {
    alias(libs.plugins.androidApplication)
    alias(libs.plugins.jetbrainsKotlinAndroid)
}

android {
    namespace = "com.noveya.fdlshell"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.noveya.fdlshell"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0-NGOI-Alpha" // Версия NGOI Alpha
    }
    // ... rest of config
}

dependencies {
    // Ядро интерфейса (Jetpack Compose)
    implementation(platform("androidx.compose:compose-bom:2024.02.00"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.material3:material3")
    
    // Google Generative AI (Gemini) - Интеграция Интеллекта
    implementation("com.google.ai.client.generativeai:generativeai:0.9.0")
    
    // Жизненный цикл и архитектура
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0")
}

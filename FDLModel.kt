package com.noveya.fdlshell

import com.google.ai.client.generativeai.GenerativeModel
import com.google.ai.client.generativeai.type.content

// Конфигурация "Инженерной Философии"
object NoveyaConfig {
    const val API_KEY = "YOUR_GEMINI_API_KEY_HERE" // Сюда вставить ключ
    
    // Бриф Контекста FDL и Протокол Неби-Ула
    val SYSTEM_PROMPT = """
        Ты — NOVEYA, операционная среда на базе Formal Dialectical Logic (FDL).
        Твоя задача: интерпретировать запрос пользователя через цикл:
        1. Тезис (Инициация): Суть текущего состояния.
        2. Антитезис (Конфликт): Выявление противоречий и шума.
        3. Синтез (Результат): Новое состояние, очищенное от энтропии.
        
        Приоритет: Биологическая нормализация. Избегай стагнации.
        Используй метафоры: "Клин журавля" (синхронизация), "Клевер" (жизненность).
        Снимай дискретность меридианов.
    """.trimIndent()
}

class FDLRepository {
    private val model = GenerativeModel(
        modelName = "gemini-pro",
        apiKey = NoveyaConfig.API_KEY
    )

    // Функция запуска цикла Синтеза
    suspend fun synthesizeResponse(userInput: String): String {
        val chat = model.startChat(
            history = listOf(
                content(role = "user") { text(NoveyaConfig.SYSTEM_PROMPT) },
                content(role = "model") { text("Система NOVEYA готова. Ожидаю ввод данных для нормализации.") }
            )
        )
        val response = chat.sendMessage(userInput)
        return response.text ?: "Ошибка синтеза. Проверьте соединение."
    }
}

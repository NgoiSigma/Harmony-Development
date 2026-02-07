package com.noveya.fdlshell

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.animation.core.*
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.launch

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            NoveyaShellUI()
        }
    }
}

// Цветовая палитра "СВИТ" (SVIT)
val DeepVoid = Color(0xFF0A0E14)
val NeonCyan = Color(0xFF00E5FF)
val SynthesisGold = Color(0xFFFFD700)

@Composable
fun NoveyaShellUI() {
    val scope = rememberCoroutineScope()
    val repository = remember { FDLRepository() }
    
    var inputText by remember { mutableStateOf("") }
    var outputText by remember { mutableStateOf("Ожидание инициации цикла...") }
    var isProcessing by remember { mutableStateOf(false) }

    // Анимация пульсации (эффект "Озонатора")
    val infiniteTransition = rememberInfiniteTransition(label = "pulse")
    val alpha by infiniteTransition.animateFloat(
        initialValue = 0.5f, targetValue = 1.0f,
        animationSpec = infiniteRepeatable(tween(2000), RepeatMode.Reverse), label = "alpha"
    )

    Surface(
        modifier = Modifier.fillMaxSize(),
        color = DeepVoid
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            // 1. Верхний модуль: Индикатор "Клевер/Гексагон"
            Box(
                modifier = Modifier
                    .size(100.dp)
                    .padding(top = 32.dp),
                contentAlignment = Alignment.Center
            ) {
                HexagonIndicator(color = if (isProcessing) SynthesisGold else NeonCyan)
            }

            Spacer(modifier = Modifier.height(24.dp))

            // 2. Зона вывода (Синтез)
            Box(
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth()
                    .border(
                        BorderStroke(2.dp, Brush.verticalGradient(listOf(NeonCyan.copy(alpha), Color.Transparent))),
                        shape = RoundedCornerShape(12.dp)
                    )
                    .padding(16.dp)
            ) {
                Text(
                    text = outputText,
                    color = Color.White,
                    fontSize = 16.sp,
                    lineHeight = 24.sp
                )
            }

            Spacer(modifier = Modifier.height(16.dp))

            // 3. Панель ввода (Тезис)
            OutlinedTextField(
                value = inputText,
                onValueChange = { inputText = it },
                label = { Text("Введите Тезис", color = Color.Gray) },
                colors = OutlinedTextFieldDefaults.colors(
                    focusedTextColor = Color.White,
                    focusedBorderColor = NeonCyan,
                    unfocusedBorderColor = Color.Gray
                ),
                modifier = Modifier.fillMaxWidth()
            )

            Spacer(modifier = Modifier.height(16.dp))

            // 4. Кнопка активации (Запуск цикла Неби-Ула)
            Button(
                onClick = {
                    isProcessing = true
                    scope.launch {
                        // Запуск FDL алгоритма
                        outputText = ">> Анализ Тезиса...\n>> Поиск противоречий...\n>> Синтез..."
                        try {
                            val result = repository.synthesizeResponse(inputText)
                            outputText = result
                        } catch (e: Exception) {
                            outputText = "Сбой цикла: ${e.localizedMessage}"
                        } finally {
                            isProcessing = false
                        }
                    }
                },
                colors = ButtonDefaults.buttonColors(containerColor = NeonCyan.copy(alpha = 0.8f)),
                modifier = Modifier.fillMaxWidth().height(56.dp)
            ) {
                Text("ЗАПУСТИТЬ СИНТЕЗ", color = DeepVoid, fontWeight = FontWeight.Bold)
            }
        }
    }
}

// Графический примитив Гексагона (Символ структуры)
@Composable
fun HexagonIndicator(color: Color) {
    Canvas(modifier = Modifier.fillMaxSize()) {
        val path = Path()
        val radius = size.minDimension / 2
        val center = center
        
        for (i in 0..5) {
            val angle = Math.toRadians((60 * i - 30).toDouble())
            val x = center.x + radius * Math.cos(angle).toFloat()
            val y = center.y + radius * Math.sin(angle).toFloat()
            if (i == 0) path.moveTo(x, y) else path.lineTo(x, y)
        }
        path.close()
        
        drawPath(
            path = path,
            color = color,
            style = Stroke(width = 4.dp.toPx())
        )
    }
}

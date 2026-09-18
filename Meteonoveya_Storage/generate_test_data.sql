-- ============================================================================
-- MMTD-NGOI :: METANOVEYA TEST DATA GENERATOR (7-DAY TIME-SERIES)
-- Моделирование суточного волнового лада и регенерации МГД-мощности
-- ============================================================================

-- Очистка старых тестовых записей перед заливкой новой матрицы
TRUNCATE TABLE zinc_spark_events;

INSERT INTO zinc_spark_events (time, impulse_power_mw, grid_transfer_load, schumann_freq_measured, tectonic_pressure_mpa)
SELECT 
    -- 1. Генерируем временную шкалу за последние 7 дней с шагом в 10 минут
    ts AS time,
    
    -- 2. Кинетическая мощность гидроудара (моделируется случайным всплеском при падении частоты)
    CASE 
        WHEN (7.83 + 0.15 * SIN(EXTRACT(EPOCH FROM ts) / 14400.0) + (RANDOM() - 0.5) * 0.05) < 7.75 
        THEN ROUND((12.0 + RANDOM() * 8.0)::numeric, 2) -- Мощный импульс 12-20 МВт при просадке среды
        ELSE 0.0
    END AS impulse_power_mw,
    
    -- 3. Нагрузка, переброшенная на тяговые фидеры (в МВт) в момент сработки
    CASE 
        WHEN (7.83 + 0.15 * SIN(EXTRACT(EPOCH FROM ts) / 14400.0) + (RANDOM() - 0.5) * 0.05) < 7.75 
        THEN ROUND((15.91 + (RANDOM() - 0.5) * 3.0)::numeric, 2) -- Целевая утилизация ~15.91 МВт
        ELSE 0.0
    END AS grid_transfer_load,
    
    -- 4. Замеренная частота Шумана (базовые 7.83 Гц + гармоника прилива планет + белый шум)
    ROUND((7.83 + 0.12 * SIN(EXTRACT(EPOCH FROM ts) / 43200.0) + (RANDOM() - 0.5) * 0.04)::numeric, 3) AS schumann_freq_measured,
    
    -- 5. Тектоническое давление в известняковом Фаготе (плавный рост и сброс при импульсах)
    ROUND((5.5 + 2.1 * COS(EXTRACT(EPOCH FROM ts) / 86400.0) + RANDOM() * 0.4)::numeric, 2) AS tectonic_pressure_mpa

FROM generate_series(
    NOW() - INTERVAL '7 days', 
    NOW(), 
    INTERVAL '10 minutes'
) AS ts;

-- Анализ и обновление статистики гипертаблицы для оптимизации планировщика TimescaleDB
ANALYZE zinc_spark_events;

-- Вывод контрольной суммы загруженных векторов для АРМ диспетчера
SELECT 
    COUNT(*) as total_generated_records,
    MIN(time) as start_horizon,
    MAX(time) as end_horizon,
    COUNT(NULLIF(impulse_power_mw, 0)) as total_zga_triggers
FROM zinc_spark_events;

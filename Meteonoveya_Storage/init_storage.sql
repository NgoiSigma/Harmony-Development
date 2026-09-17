-- 1. Активация расширения TimescaleDB для работы с непрерывными потоками временных рядов
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- 2. Таблица метрик Спасского холма (высокочастотный лог пульсаций среды)
CREATE TABLE spas_hill_metrics (
    time TIMESTAMPTZ NOT NULL,
    shumann_freq_hz REAL NOT NULL,          -- Текущая частота резонатора (альфа-оптимум)
    voldo_fac_noise REAL NOT NULL,          -- Инфразвуковой тектонический шум разлома (МПа)
    ingul_pressure_mpa REAL NOT NULL,       -- Давление в палео-русле Ингула по Жуковскому
    magnetic_field_nt REAL NOT NULL         -- Геомагнитная индукция в катакомбах
);

-- Превращение базовой таблицы в гипертаблицу TimescaleDB с шагом секционирования в 1 день
SELECT create_hypertable('spas_hill_metrics', 'time', chunk_time_interval => INTERVAL '1 day');

-- 3. Таблица фиксации «Цинк-Спарк» (Журнал «цинковых салютов» / прорывов Зги)
CREATE TABLE zinc_spark_events (
    time TIMESTAMPTZ NOT NULL,
    event_id SERIAL,
    activation_type VARCHAR(32) NOT NULL,   -- AUTOMATIC (порог давления) или MANUAL (кнопка диспетчера)
    discharge_volume_q REAL NOT NULL,       -- Расход компенсационного сброса (м3/с)
    impulse_power_mw REAL NOT NULL,         -- Мгновенная кинетическая мощность гидроудара (МВт)
    grid_transfer_load REAL NOT NULL,       -- Мощность, переброшенная на фидеры Николаевэлектротранса (МВт)
    PRIMARY KEY (time, event_id)
);

SELECT create_hypertable('zinc_spark_events', 'time', chunk_time_interval => INTERVAL '1 month');

-- 4. Таблица прецессионных выравниваний (астрономический тензор натяжения)
CREATE TABLE precession_alignments (
    time TIMESTAMPTZ NOT NULL,
    alignment_sector_deg REAL NOT NULL,     -- Угловой сектор парада 6 планет относительно меридиана обсерватории
    grav_gradient_total REAL NOT NULL,      -- Кумулятивный гравитационный градиент (d2Phi/dr2)
    target_planet_mask INT NOT NULL,        -- Битовая маска участвующих планет
    PRIMARY KEY (time)
);

SELECT create_hypertable('precession_alignments', 'time', chunk_time_interval => INTERVAL '1 month');

-- 5. Индексация для ускорения работы ГИС-запросов верхнего уровня
CREATE INDEX idx_metrics_freq ON spas_hill_metrics (shumann_freq_hz, time DESC);
CREATE INDEX idx_spark_power ON zinc_spark_events (impulse_power_mw DESC);

-- 6. Настройка политики автоматического сжатия данных (Compression Policy) для экономии диска
ALTER TABLE spas_hill_metrics SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'shumann_freq_hz'
);
SELECT add_compression_policy('spas_hill_metrics', INTERVAL '7 days');

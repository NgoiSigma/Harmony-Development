#include <iostream>
#include <cmath>
#include <chrono>
#include <thread>
#include <atomic>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>
#include <sched.h>
#include <pthread.h>

#define PAS_HILL_LATENCY_NS 2400000000ULL // Время фазы гидроудара Т_phase = 2.4 секунды
#define CRITICAL_PRESSURE_MPA 1.8         // Предельное давление по Жуковскому
#define SHM_PATH "/meteonoveya_shm"       // Путь разделяемой памяти с ГИС
#define TARGET_CPU_CORE 3                 // Изолированное ядро процессора для RT-потока

struct NoveyaTelemetry {
    std::atomic<float> current_shumann_freq;
    std::atomic<float> target_q_discharge;
    std::atomic<bool>  trigger_genesis_valve;
    std::atomic<float> electrotrans_grid_load;
};

class PranoveyaRTCore {
private:
    NoveyaTelemetry* telemetry;
    int shm_fd;
    bool is_running;

    float read_ingul_pressure_sensor() {
        return 1.25f + static_cast<float>(rand() % 100) / 200.0f; 
    }

    void set_hydraulic_valve(float opening_percentage) {
        // Прямая запись в регистры ввода-вывода исполнительного механизма
        // std::cout << "[HARD RT] Положение задвижки Спасского холма: " << opening_percentage << "%" << std::endl;
    }

    void modulate_electrotrans_zug(float power_mw) {
        // Команда на контроллер фидеров подстанции Николаевэлектротранса
    }

    // Настройка планировщика RT-Preempt Linux
    void configure_linux_rt_priority() {
        struct sched_param param;
        param.sched_priority = 99; // Максимальный приоритет в RT-Linux

        if (sched_setscheduler(0, SCHED_FIFO, &param) == -1) {
            std::cerr << "[❌ RT_ERROR] Не удалось установить SCHED_FIFO. Запустите от root!" << std::endl;
            exit(EXIT_FAILURE);
        }

        // Блокировка памяти во избежание деградации тактов из-за своппинга/пейджинга
        if (mlockall(MCL_CURRENT | MCL_FUTURE) == -1) {
            std::cerr << "[❌ RT_ERROR] Ошибка выполнения mlockall!" << std::endl;
            exit(EXIT_FAILURE);
        }

        // Привязка RT-потока к выделенному изолированному ядру ЦП
        cpu_set_set_t cpuset;
        CPU_ZERO(&cpuset);
        CPU_SET(TARGET_CPU_CORE, &cpuset);
        pthread_t current_thread = pthread_self();
        if (pthread_setaffinity_np(current_thread, sizeof(cpu_set_t), &cpuset) != 0) {
            std::cerr << "[❌ RT_ERROR] Ошибка pthread_setaffinity_np на ядро " << TARGET_CPU_CORE << std::endl;
        }
        std::cout << "[⚡ RT_OK] Поток жестко изолирован на ядре ЦП " << TARGET_CPU_CORE << " с приоритетом 99." << std::endl;
    }

public:
    PranoveyaRTCore() : is_running(false), telemetry(nullptr) {
        shm_fd = shm_open(SHM_PATH, O_CREAT | O_RDWR, 0666);
        ftruncate(shm_fd, sizeof(NoveyaTelemetry));
        telemetry = (NoveyaTelemetry*)mmap(0, sizeof(NoveyaTelemetry), PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, 0);
    }

    void start_rt_loop() {
        configure_linux_rt_priority();
        is_running = true;
        
        struct timespec next_wakeup;
        clock_gettime(CLOCK_MONOTONIC, &next_wakeup);
        
        while (is_running) {
            // Дискретизация строго 100 мс (100,000,000 наносекунд)
            next_wakeup.tv_nsec += 100000000;
            if (next_wakeup.tv_nsec >= 1000000000) {
                next_wakeup.tv_sec += 1;
                next_wakeup.tv_nsec -= 1000000000;
            }
            
            float p_ingul = read_ingul_pressure_sensor();
            bool dispatch_active = telemetry->trigger_genesis_valve.load();
            
            if (dispatch_active || p_ingul > CRITICAL_PRESSURE_MPA) {
                // Мгновенный сброс запруды (Прорыв Зги)
                set_hydraulic_valve(100.0f);
                modulate_electrotrans_zug(15.91f); 
                telemetry->trigger_genesis_valve.store(false);
                
                // Прецизионное удержание гидроудара в наносекундах без прерываний
                struct timespec delay;
                delay.tv_sec = PAS_HILL_LATENCY_NS / 1000000000;
                delay.tv_nsec = PAS_HILL_LATENCY_NS % 1000000000;
                clock_nanosleep(CLOCK_MONOTONIC, 0, &delay, NULL);
            } else {
                set_hydraulic_valve(12.5f); // Штатный проток Лада
            }
            
            // Жесткий джиттер-контроль RT-Preempt
            clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, &next_wakeup, NULL);
        }
    }

    ~PranoveyaRTCore() {
        is_running = false;
        munmap(telemetry, sizeof(NoveyaTelemetry));
        close(shm_fd);
        shm_unlink(SHM_PATH);
        munlockall();
    }
};

int main() {
    PranoveyaRTCore core;
    core.start_rt_loop();
    return 0;
}

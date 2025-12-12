from datetime import datetime

from model import (
    Sensor,
    InMemorySensorRepository,
    InMemoryLevelRepository,
    InMemoryStorageRepository,
    InMemoryForecastRepository,
    InMemoryReportRepository,
)
from controllers import (
    JournalManager,
    LevelManager,
    DataCollectionController,
    AnalysisController,
    DecisionSupportController,
    InterfaceController,
)


def run_controller_tests():
    print("===== ТЕСТ КОНТРОЛЛЕРОВ =====")

    # --- Общие компоненты / репозитории ---
    sensor_repo = InMemorySensorRepository()
    level_repo = InMemoryLevelRepository()
    storage_repo = InMemoryStorageRepository()
    forecast_repo = InMemoryForecastRepository()
    report_repo = InMemoryReportRepository()
    journal = JournalManager()

    # --- Наполняем систему тестовыми данными ---
    # Сенсоры
    sensor_repo.add_sensor(
        Sensor(sensor_id=1, type="temperature", unit="C", poll_frequency=5, value=22.5)
    )
    sensor_repo.add_sensor(
        Sensor(sensor_id=2, type="humidity", unit="%", poll_frequency=10, value=60.0)
    )

    # Менеджер уровней и один уровень
    level_manager = LevelManager(level_repo)
    level_data = {
        "id": 1,
        "name": "Тестовый уровень",
        "difficulty": 0.4,
        "parameters": {"enemies": 10, "traps": 3},
        "description": "Уровень для проверки связки контроллеров",
    }
    level = level_manager.create_level(level_data)

    # --- Контроллеры ---
    data_controller = DataCollectionController(sensor_repo, storage_repo, journal)
    analysis_controller = AnalysisController(storage_repo, forecast_repo, journal)
    decision_controller = DecisionSupportController(
        forecast_repo, report_repo, journal
    )
    interface_controller = InterfaceController(
        level_manager, analysis_controller, decision_controller, journal
    )

    # === Сценарий: тестирование уровня ===
    print("[ШАГ] Инициализация сенсоров и сбор данных...")
    data_controller.initialize_sensors()
    data_controller.collect_data(level_id=level.level_id)
    data_controller.finish_collection()

    print("[ШАГ] Пользователь выбирает сценарий 'level_testing'...")
    interface_controller.handle_user_choice("level_testing", level_id=level.level_id)

    # Получаем результаты (отчёты), сформированные через интерфейс
    reports = interface_controller.show_results()
    assert len(reports) >= 1, "Ожидался хотя бы один отчёт"

    last_report = reports[-1]
    print("[OK] Получен отчёт:")
    print("  id:       ", last_report.report_id)
    print("  author:   ", last_report.author)
    print("  summary:  ", last_report.summary)
    print("  created:  ", last_report.created_at)
    print("  content:\n", last_report.content)

    # Показать немного истории журнала
    print("\n===== ФРАГМЕНТ ЖУРНАЛА =====")
    for entry in journal.view_history()[-10:]:  # последние 10 записей
        print(f"[{entry.timestamp:%H:%M:%S}] {entry.level}: {entry.message}")

    print("\n===== ВСЕ ТЕСТЫ КОНТРОЛЛЕРОВ ПРОЙДЕНЫ УСПЕШНО =====")


if __name__ == "__main__":
    run_controller_tests()

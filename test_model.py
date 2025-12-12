from datetime import datetime
from model import (
    Sensor,
    Level,
    StorageRecord,
    Report,
    Forecast,
    InMemorySensorRepository,
    InMemoryLevelRepository,
    InMemoryStorageRepository,
    InMemoryReportRepository,
    InMemoryForecastRepository,
)


def run_tests():
    print("===== ТЕСТ МОДЕЛИ =====")

    # --- Репозитории ---
    sensors = InMemorySensorRepository()
    levels = InMemoryLevelRepository()
    storage = InMemoryStorageRepository()
    reports = InMemoryReportRepository()
    forecasts = InMemoryForecastRepository()

    # --- Сенсор ---
    s = Sensor(sensor_id=1, type="temperature", unit="C", poll_frequency=5, value=22.5)
    sensors.add_sensor(s)

    assert sensors.get_sensor(1) is not None
    print("[OK] Sensor added")

    # --- Уровень ---
    lvl = Level(
        level_id=10,
        name="Лес",
        difficulty=0.3,
        parameters={"trees": 50, "rocks": 10},
        description="Лесной уровень"
    )
    levels.add_level(lvl)

    assert levels.get_level(10).name == "Лес"
    print("[OK] Level added")

    # --- Обновление уровня ---
    lvl.update_parameters({"rocks": 20})
    lvl.calculate_difficulty()
    levels.update_level(lvl)

    assert levels.get_level(10).parameters["rocks"] == 20
    print("[OK] Level updated")

    # --- Запись хранилища ---
    rec = StorageRecord(
        timestamp=datetime.now(),
        sensor_id=1,
        value=22.5,
        event_type="NORMAL"
    )
    storage.save_record(rec)

    assert len(storage.get_history(1)) == 1
    print("[OK] Storage record saved")

    # --- Отчёт ---
    rpt = Report(
        report_id=5,
        created_at=datetime.now(),
        author="Admin",
        summary="Тестовый отчёт",
        content="Содержимое отчёта"
    )
    reports.save_report(rpt)

    assert reports.get_report(5).author == "Admin"
    print("[OK] Report saved")

    # --- Экспорт отчёта ---
    exported = rpt.export("txt")
    assert "[FORMAT=txt]" in exported
    print("[OK] Report exported")

    # --- Прогноз ---
    fr = Forecast.from_level(
        forecast_id=99,
        level=lvl,
        recommendations="Будь осторожен",
    )
    forecasts.save_forecast(fr)

    assert forecasts.get_forecast(99).level_name == "Лес"
    print("[OK] Forecast created")

    print("\n===== ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО =====")


if __name__ == "__main__":
    run_tests()

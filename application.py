from __future__ import annotations

from typing import Optional

from controllers import (
    JournalManager,
    LevelManager,
)
from infrastructure import (
    DependencyContainer,
    SystemConfigurator,
    LevelsView,
    RecommendationsView,
    ReportsView,
)


class Application:
    """
    «Приложение» с диаграммы 3-в-1.

    Методы:
        - initialize()  — инициализировать
        - start()       — запустить (здесь реализован сценарий из диаграммы последовательности)
        - stop()        — остановить
        - show_main_menu() — показать главное "меню"
    """

    def __init__(self) -> None:
        self._container = DependencyContainer()
        self._configurator = SystemConfigurator()
        self._initialized: bool = False

        self._levels_view: Optional[LevelsView] = None
        self._recs_view: Optional[RecommendationsView] = None
        self._reports_view: Optional[ReportsView] = None

    # ------------------------------------------------------------------
    # ИНИЦИАЛИЗАЦИЯ
    # ------------------------------------------------------------------

    def initialize(self) -> None:
        """инициализировать()"""
        # Настраиваем зависимости
        self._configurator.configure(self._container)
        self._container.initialize()
        self._configurator.load_parameters(self._container)

        journal: JournalManager = self._container.resolve(JournalManager)
        level_manager: LevelManager = self._container.resolve(LevelManager)
        interface_ctrl = self._configurator.controller_factory.create("interface")

        # Создаём представления
        self._levels_view = LevelsView(level_manager, journal)
        self._recs_view = RecommendationsView(journal)
        self._reports_view = ReportsView(interface_ctrl, journal)

        self._initialized = True
        journal.add_entry("Приложение инициализировано", level="INFO")

    # ------------------------------------------------------------------
    # ГЛАВНЫЙ СЦЕНАРИЙ (реализация диаграммы последовательности)
    # ------------------------------------------------------------------

    def start(self) -> None:
        """запустить() — внутри реализуем сценарий из диаграммы последовательности."""
        if not self._initialized:
            self.initialize()

        journal: JournalManager = self._container.resolve(JournalManager)
        level_manager: LevelManager = self._container.resolve(LevelManager)

        journal.add_entry("Приложение запущено", level="INFO")

        # 0. Показать главное меню (со стороны UIController)
        self.show_main_menu()

        # ------------------------------------------------------------------
        # ЧАСТЬ 1. ПЕРВОЕ ТЕСТИРОВАНИЕ УРОВНЯ
        # ------------------------------------------------------------------

        # 1. Разработчик игр «запускает тестирование уровня»
        level_data = {
            "id": 1,
            "name": "Проблемный уровень",
            "difficulty": 0.8,
            "parameters": {"enemies": 20, "traps": 8},
            "description": "Уровень с подозрением на низкую проходимость",
        }
        level = level_manager.create_level(level_data)
        journal.add_entry(
            f"Разработчик игр запускает тестирование уровня id={level.level_id}",
            level="INFO",
        )

        # 2. Дизайнер уровней через контроллер интерфейса выбирает сценарий
        ctrl_factory = self._configurator.controller_factory
        interface_ctrl = ctrl_factory.create("interface")
        data_ctrl = ctrl_factory.create("data")
        analysis_ctrl = ctrl_factory.create("analysis")
        decision_ctrl = ctrl_factory.create("decision")

        scenarios = interface_ctrl.show_scenarios()
        chosen_scenario = scenarios[1] if len(scenarios) > 1 else scenarios[0]
        journal.add_entry(
            f"Дизайнер уровней выбирает сценарий '{chosen_scenario}'",
            level="INFO",
        )

        # 3. Контроллер интерфейса инициирует сбор данных
        data_ctrl.initialize_sensors()

        # 4. Контроллер сбора данных считывает значения сенсоров и сохраняет их
        data_ctrl.collect_data(level_id=level.level_id)
        data_ctrl.finish_collection()

        # 5. Контроллер анализа запрашивает данные из хранилища и анализирует их
        stats_first = analysis_ctrl.analyze_data(level)

        # 6. Контроллер анализа создаёт прогноз (аналог модуля рекомендаций)
        forecast_first = analysis_ctrl.create_forecast(level)

        journal.add_entry(
            f"Модуль рекомендаций подготовил советы: {forecast_first.recommendations}",
            level="INFO",
        )

        # 7. Контроллер поддержки решений формирует отчёт по прогнозу
        report_first = decision_ctrl.form_report(forecast_first, author="level_designer")
        decision_ctrl.send_report(report_first, user="level_designer")
        decision_ctrl.check_correctness()

        print("\n--- Первый отчёт ---")
        print(report_first.content)

        # ------------------------------------------------------------------
        # ЧАСТЬ 2. ИЗМЕНЕНИЕ ПАРАМЕТРОВ УРОВНЯ И ПОВТОРНОЕ ТЕСТИРОВАНИЕ
        # ------------------------------------------------------------------

        # 8. Дизайнер запрашивает параметры уровня
        current_level = level_manager.get_levels()[0]
        journal.add_entry(
            f"Дизайнер запрашивает параметры уровня id={current_level.level_id}",
            level="INFO",
        )

        print("\nПараметры ДО изменений:",
              current_level.parameters,
              "сложность:", current_level.difficulty)

        # 9. Дизайнер вносит изменения (уменьшаем сложность и параметры)
        new_params = dict(current_level.parameters)
        if "enemies" in new_params:
            new_params["enemies"] = max(0, int(new_params["enemies"] * 0.7))
        if "traps" in new_params:
            new_params["traps"] = max(0, int(new_params["traps"] * 0.7))

        level_manager.edit_level(
            current_level.level_id,
            {
                "parameters": new_params,
                "difficulty": max(0.0, current_level.difficulty - 0.2),
            },
        )
        updated_level = level_manager.get_levels()[0]

        journal.add_entry(
            f"Дизайнер изменил параметры уровня id={updated_level.level_id}",
            level="INFO",
        )

        print("Параметры ПОСЛЕ изменений:",
              updated_level.parameters,
              "сложность:", updated_level.difficulty)

        # 10. Разработчик запускает повторное тестирование
        journal.add_entry(
            f"Разработчик игр запускает ПОВТОРНОЕ тестирование уровня id={updated_level.level_id}",
            level="INFO",
        )

        # Для имитации улучшения поведения немного меняем показания сенсоров
        from model import SensorRepository  # только для type-hint; не обязательно

        for sensor in self._container.resolve("repo:sensor").get_all():
            if sensor.type == "completion_time":
                sensor.value = max(60.0, sensor.value * 0.8)
            if sensor.type == "load":
                sensor.value = max(0.3, sensor.value * 0.9)

        # 11. Новый сбор данных
        data_ctrl.initialize_sensors()
        data_ctrl.collect_data(level_id=updated_level.level_id)
        data_ctrl.finish_collection()

        # 12. Новый анализ и прогноз
        stats_second = analysis_ctrl.analyze_data(updated_level)
        forecast_second = analysis_ctrl.create_forecast(updated_level)

        # 13. Новый отчёт и проверка
        report_second = decision_ctrl.form_report(
            forecast_second,
            author="level_designer",
        )
        decision_ctrl.send_report(report_second, user="level_designer")
        decision_ctrl.check_correctness()

        print("\n--- Второй отчёт (после изменений уровня) ---")
        print(report_second.content)

        # 14. Итоговое отображение результатов (через отчётное представление)
        journal.add_entry(
            "Отображение итоговых результатов тестирования уровня",
            level="INFO",
        )

    # ------------------------------------------------------------------
    # ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ
    # ------------------------------------------------------------------

    def stop(self) -> None:
        """остановить()"""
        journal: JournalManager = self._container.resolve(JournalManager)
        journal.add_entry("Приложение остановлено", level="INFO")

    def show_main_menu(self) -> None:
        """
        показатьГлавноеМеню()

        Здесь пока нет реального GUI — просто заглушка.
        Главное, что есть точка входа и связка всех уровней приложения.
        """
        journal: JournalManager = self._container.resolve(JournalManager)
        journal.add_entry("Показано главное меню (заглушка)", level="INFO")

        if self._levels_view:
            self._levels_view.show()
        if self._reports_view:
            self._reports_view.show()
        if self._recs_view:
            self._recs_view.show()


# ----------------------------------------------------------------------
# ТОЧКА ВХОДА — здесь же выводим журнал, чтобы было видно сценарий
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app = Application()
    app.start()

    # вывод журнала в консоль
    from controllers import JournalManager  # локальный импорт, чтобы не мешать выше

    journal: JournalManager = app._container.resolve(JournalManager)
    print("\n===== ЖУРНАЛ ПРИЛОЖЕНИЯ =====")
    for entry in journal.view_history():
        print(f"[{entry.timestamp:%H:%M:%S}] {entry.level}: {entry.message}")

    app.stop()

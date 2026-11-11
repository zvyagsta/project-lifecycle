"""Check neutral report templates and bundled font files without a browser."""

from pathlib import Path
import re


ASSETS = Path(__file__).resolve().parents[1] / "assets" / "report-style"
VALUES = {
    "TITLE": "Пример обзора",
    "PROJECT": "Пример проекта",
    "DATE_LABEL": "Период: пример",
    "MAIN": "Работа по проекту продвинулась",
    "LEDE": "Сводка подтверждённых результатов и следующего шага.",
    "SECTIONS": "<section><h2>Результат</h2><p>Подготовлена рабочая схема.</p></section>",
    "DONE_COUNT": "2",
    "DONE_CARDS": "<div class='col'><h3>Схема</h3><p>Подготовлена.</p></div>"
                  "<div class='col wait'><h3>Проверка</h3><p>Ожидается.</p></div>",
    "NEXT_COUNT": "2",
    "NEXT_STEPS": "<li class='stop'><i>1</i><b>Просмотр</b><span>Проверить схему.</span></li>"
                  "<li class='stop later'><i>2</i><b>Решение</b><span>Записать итог.</span></li>",
}


def main() -> None:
    css = (ASSETS / "design.css").read_text(encoding="utf-8")
    assert "Bitter" in css and "Golos Text" in css
    for name in ("bitter-cyrillic", "bitter-latin", "golos-cyrillic", "golos-latin"):
        path = ASSETS / "fonts" / f"{name}.woff2"
        assert path.read_bytes().startswith(b"wOF2"), f"invalid WOFF2 font: {name}"
        assert f"fonts/{name}.woff2" in css
    assert len(list((ASSETS / "icons").glob("*.svg"))) >= 10
    for name in ("report.html", "infographic.html", "plan.html"):
        assert '@import url("design.css")' in (ASSETS / name).read_text(encoding="utf-8"), name
    for name in ("report.html", "infographic.html"):
        content = (ASSETS / name).read_text(encoding="utf-8")
        for key, value in VALUES.items():
            content = content.replace("{{" + key + "}}", value)
        assert "{{" not in content, f"unfilled placeholder in {name}"
        assert "Пример проекта" in content
    plan_css = (ASSETS / "plan.css").read_text(encoding="utf-8")
    assert not re.search(r"#[0-9a-fA-F]{3,6}\b", plan_css), "plan.css must take colors from design.css"
    for token in re.findall(r"var\((--[a-z0-9-]+)\)", plan_css):
        assert token in css or f"{token}:" in plan_css, f"plan.css uses an undefined token {token}"
    plan = (ASSETS / "plan.html").read_text(encoding="utf-8")
    assert '@import url("plan.css")' in plan
    for cls in ("sheet", "explain", "status", "steps", "step key", "decisions", "chain", "who", "tail"):
        assert f'class="{cls}"' in plan, f"plan.html lacks the {cls} block"
    print("PASS: neutral report, infographic and plan templates; four bundled WOFF2 fonts")


if __name__ == "__main__":
    main()

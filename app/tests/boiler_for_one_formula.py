from app.models.one_action_formula import OneActionFormula


async def generate_given_to_bd(session):
    given1 = OneActionFormula(
        formula="m*10*h",
        question=(
            "Тело массой {m} кг, брошенное вертикально вверх, достигло максимальной высоты {h} м."
            "Какой кинетической энергией обладало тело сразу после броска? Сопротивлением воздуха пренебречь."
        ),
        param_ranges={"m": (1, 100), "h": (1, 100)},
    )
    given2 = OneActionFormula(
        formula="Fa/10",
        question=(
            "На лодку, плавающую в воде, действует сила Архимеда величиной {Fa} Н. Чему равна масса лодки?"
        ),
        param_ranges={"Fa": (100, 1000)},
    )
    given3 = OneActionFormula(
        formula="u * 340",
        question=(
            "Человек услышал звук грома через {u} с после вспышки молнии."
            "Считая, что скорость звука в воздухе равна 340 м/с, определите, на каком расстоянии от человека ударила молния."
        ),
        param_ranges={"u": (1, 20)},
    )

    session.add_all([given1, given2, given3])
    await session.commit()

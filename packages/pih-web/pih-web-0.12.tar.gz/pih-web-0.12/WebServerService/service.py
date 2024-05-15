import ipih

from pih import A, PIHThread

from WebServerService.const import SD

SC = A.CT_SC

ISOLATED: bool = False


def start(as_standalone: bool = False) -> None:
    if A.U.for_service(SD, as_standalone=as_standalone):
        from pih.collections import (
            ActionDescription,
        )
        from pih.tools import j, js, n, e, ne, nn, esc, escs

        import uvicorn
        from typing import Any
        from dicttoxml import dicttoxml
        from dataclasses import dataclass
        from fastapi import FastAPI, Request
        from fastapi.responses import Response

        app: FastAPI = FastAPI()

        @app.get("/get_person")
        def get_person() -> None:
            @dataclass
            class Person:

                per_las_name: str = "Караченцев"
                per_fir_name: str = "Никита"
                per_sec_name: str = "Александрович"
                per_birth: str = "03.02.1987"
                per_sex: str = "М"
                scs_number: str = "376544"
                scs_date: str = "09.07.2007"
                scs_se: str = "0507"
                scs_dtps_no: str = "140"
                scs_org_name: str = (
                    "Отделом УФМС России по приморскому краю в Первомайcком районе гор Владивостока"
                )

            return Response(
                content=dicttoxml(
                    vars(Person()),
                    attr_type=False,
                    custom_root="Person",
                    return_bytes=False,
                ),
                media_type="application/xml",
            )

        @app.get("/door/{door_operation}/{door_name}")
        async def on_door_operation_handler(door_operation: str, door_name: str):
            action: A.CT_ACT | None = None
            if A.D.equal("open", door_operation):
                action = A.CT_ACT.DOOR_OPEN
            elif A.D.equal("close", door_operation):
                action = A.CT_ACT.DOOR_CLOSE
            if nn(action):
                A.A_ACT.was_done(action, parameters=[door_name])  # type: ignore
                return js(
                    (
                        "Начат процесс",
                        ["закрытия", "открытия"][action == A.CT_ACT.DOOR_OPEN],
                        "дверей",
                    )
                )

        @app.get("/action/{action_name}")
        async def on_action_handler(action_name: str):
            target_action_description: ActionDescription | None = None
            for action in A.CT_ACT:
                action_description: ActionDescription = A.D.get(action)
                if (
                    ne(action_description.alias)
                    and action_name in action_description.alias
                ):
                    A.A_ACT.was_done(action)
                    target_action_description = action_description
            if n(target_action_description):
                A.A_ACT.was_done(A.CT_ACT.ACTION, parameters=[action_name])
                return js(
                    ("Неспециализированное действие", escs(action_name), "выполняется")
                )
            return js(
                ("Действие", escs(target_action_description.description), "выполняется")
            )

        @app.get("/execute/{file_name}")
        async def on_execute_handler(file_name: str, request: Request):
            parameters: dict[str | int, Any] = {"is_browser": True}
            index: int = 0
            for item in request.query_params:
                if isinstance(item, tuple):
                    if e(item[1]):
                        parameters[index] = item[0]
                        index += 1
                    else:
                        parameters[item[0]] = item[1]
                else:
                    parameters[index] = item
                    index += 1
            result: list[str] | None = A.R_F.execute(file_name, {"parameters": parameters})  # type: ignore
            if n(result):
                return js(("Ошибка: файл", esc(file_name), "не найден!"))
            return js(("Файл", file_name, "выполнен"))

        def fast_api_thread() -> None:
            uvicorn.run(app, host="0.0.0.0", port=A.CT_PORT.HTTP)

        def service_starts_handler() -> None:
            A.SYS.kill_process_by_port(A.CT_PORT.HTTP)
            PIHThread(fast_api_thread)
            A.SRV_A.subscribe_on(SC.heart_beat)

        A.SRV_A.serve(
            SD,
            starts_handler=service_starts_handler,
            isolate=ISOLATED,
            as_standalone=as_standalone,
        )


if __name__ == "__main__":
    start()

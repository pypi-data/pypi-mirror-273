import ipih

from pih import A, PIHThread

from WebServerService.const import SD, ALERT_SOUND
SC = A.CT_SC

ISOLATED: bool = False

def start(as_standalone: bool = False) -> None:
    if A.U.for_service(SD, as_standalone=as_standalone):
        from pih.collections import (
            IndicationDevice,
            ActionDescription,
            CTIndicationsValueContainer,
            ChillerIndicationsValueContainer,
        )
        from pih.tools import j, js, n, e, ne, nn, esc, escs

        import os
        import shutil
        import uvicorn
        from typing import Any
        from datetime import datetime
        from pydantic import BaseModel
        from fastapi import FastAPI, UploadFile, Request
        from fastapi.responses import HTMLResponse, FileResponse

        class IncomeCTIndicationsValue(BaseModel):
            temperature: float | None = None
            humidity: float | None = None

        class IndicationDeviceModel(BaseModel):
            name: str | None = None
            description: str | None = None

        class DH:
            device_map: dict[str, str] = {}

        app: FastAPI = FastAPI()

        @app.get("/ct_stat", response_class=FileResponse)
        async def ct_day():
            return A.PTH_STAT.get_file_path(A.CT_STAT.Types.CT_DAY)

        @app.get("/ct_stat_week", response_class=FileResponse)
        async def ct_week():
            return A.PTH_STAT.get_file_path(A.CT_STAT.Types.CT_WEEK)

        @app.get("/ct_stat_month", response_class=FileResponse)
        async def ct_month():
            return A.PTH_STAT.get_file_path(A.CT_STAT.Types.CT_MONTH)

        @app.get("/")
        def read_root() -> HTMLResponse:
            ct_value: CTIndicationsValueContainer = A.R.get_first_item(
                A.R_IND.last_ct_value_containers(True)
            )
            chiller_value: ChillerIndicationsValueContainer = A.R.get_first_item(
                A.R_IND.last_chiller_value_containers(True)
            )
            chiller_is_on: bool = A.C_IND.chiller_on()
            chiller_temperature_good: bool = A.C_IND.chiller_temperature_good()
            ct_day_image_content: str = j(
                (
                    '<img alt="День" src="data:image/jpeg;base64,',
                    A.D_CO.file_to_base64(
                        A.PTH_STAT.get_file_path(A.CT_STAT.Types.CT_DAY)
                    ),
                    '" id="image" loading="lazy" class="lazyload"/>',
                )
            )
            ct_week_image_content: str = j(
                (
                    '<img alt="Неделя" src="data:image/jpeg;base64,',
                    A.D_CO.file_to_base64(
                        A.PTH_STAT.get_file_path(A.CT_STAT.Types.CT_WEEK)
                    ),
                    '" id="image" loading="lazy" class="lazyload"/>',
                )
            )
            ct_month_image_content: str = j(
                (
                    '<img alt="Месяц" src="data:image/jpeg;base64,',
                    A.D_CO.file_to_base64(
                        A.PTH_STAT.get_file_path(A.CT_STAT.Types.CT_MONTH)
                    ),
                    '" id="image" loading="lazy" class="lazyload"/>',
                )
            )
            chiller_image_content: str = j(
                (
                    '<img alt="Изображение дисплея" src="data:image/jpeg;base64,',
                    A.D_CO.file_to_base64(A.PTH_IND.CHILLER_DATA_IMAGE_LAST_RESULT),
                    '" id="image" loading="lazy" class="lazyload"/>',
                )
            )
            chiller_display_container: str = (
                """<div class="row">
                                            <div class="current-c">Дисплей чиллера</div>
                                            <div id="refreshF" class="current-c chiller">"""
                + chiller_image_content
                + """</div>
                                            <div class="current-c info-small">[ """
                + js(
                    (
                        str(A.S.get(A.CT_S.CHILLER_MIN_TEMPERATURE)),
                        "-",
                        str(A.S.get(A.CT_S.CHILLER_MAX_TEMPERATURE)),
                    )
                )
                + """ ] °C</div>
                                            </div>"""
                if chiller_is_on
                else """<div class="row">
                                            <div id="refreshF" class="current-c chiller_red">"""
                + "Чиллер ВЫКЛЮЧЕН"
                + """</div>
                                            </div>"""
            )
            sound_content: str = ""
            # not chiller_is_on or
            if not chiller_temperature_good:
                sound_content = f"<audio autoplay loop src='{ALERT_SOUND}'></audio>"
            content: str = (
                """<!DOCTYPE html>
                <html lang="ru-ru" dir="ltr">"""
                + sound_content
                + """<head>
                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                    <meta charset="utf-8">
                    <title>Показания датчиков</title>
                    <meta http-equiv="refresh" content="60">
            <style>
            *, :after, :before {box-sizing:border-box;}
            * {-webkit-scroll-behavior:smooth;scroll-behavior: smooth;}
            body {font-family:Arial,sans-serif;margin:0;text-transform:uppercase;}
            body.opengeimer {color:#444;}

            .general-page.area {background:#fff;overflow-x: hidden;}
            a {text-decoration: none;}
            h1,h2 {text-align:center;margin:0;}
            h1.diag {font-weight:900;font-size:22px;margin-top: 5px;}
            .CT,.MRI {width:47.2%;margin:10px; float:left; border-radius:5px; background:#fff; position:relative; border: 1px solid #eee;}
            .CT h2,.MRI h2 {background:#f6f6f6;padding:5px;font-weight:700;margin-bottom:1px;border-radius:5px 5px 0 0;border-bottom: 1px solid #f1f1f1;}
            .oops-6712854923 {position:relative;min-height: 150px;}
            h2 > span {font-weight:900;}
            .row {}
            .current-c {text-align:center;font-weight:700;}
            .current-c.chiller {font-weight: 700; font-size: 54px; padding: 5px; margin: auto; letter-spacing: 1px; color: #777; display: flex; align-content: center; justify-content: center; align-items: center; flex-wrap: wrap; position: relative;}
            .current-c.chiller_red {font-weight: 700; font-size: 54px; padding: 5px; margin: auto; letter-spacing: 1px; color: red; display: flex; align-content: center; justify-content: center; align-items: center; flex-wrap: wrap; position: relative;}
            .current-c span {font-size:32px;font-weight:700;width:100%;display:inline-block;}
            .itstime {display:block;font-weight:700;font-size:16px;}
            .progressbar p {font-weight: 700; font-size: 14px; padding: 5px; margin: auto; letter-spacing: 1px; color: #777; display: flex; align-content: center; height: 32px; justify-content: center; align-items: center; flex-wrap: wrap; position: relative;}
            .couple {display: flex;flex-direction: row;justify-content: center;align-items: center;z-index: 1; position: absolute;bottom: 0;top: 0;margin: 40px auto;padding: 0 40px;width: 100%;}
            .container {width:1080px;margin:auto;}
            .info-small {font-weight:700;font-size:12px;}
            .humidity img {width: 100%;}
            .chiller img {border-radius:5px;filter: invert(1);max-width:300px;}
            .MRI .oops-6712854923 {margin: 10px;}
            @media (max-width: 565px) {
                .container,.CT,.MRI {width: auto;}
                .CT,.MRI {float: none;}
            }

            .clock {width: 100%;display: flex;flex-direction: row;justify-content: center;align-items: center;background: #424558;}
            .time {padding: 0 10px;font-size: 50px;font-weight: bold;color: #fff;}
            .date-time {padding: 0 10px;text-align: center;font-size: 18px;color: #fff;}

            .progressbar {position: relative;margin: 0 auto;background: #eee;}
            /*span.progress {position: absolute;left: 0;top: 0;bottom: 0; background: #ccc;opacity: .9;animation: animate 60s linear 1;}
            @keyframes animate { 
                0%  {
                    width: 0%;
                } 
                100% { 
                    width: 100%;
                }
            }*/

            .time span.dots {animation: animateTime 1s ease-out infinite;}
            @keyframes animateTime { 
                0%  {
                    opacity: 0;
                } 
                50% {
                    opacity: 0.9;
                }
                100% { 
                    opacity: 0;
                }
            }
            .tabs {position: relative;display: flex;min-height: 390px;overflow: hidden;}
            .tabby-tab {flex: 1;}
            .tabby-tab label {display: block;box-sizing: border-box;height: auto; padding: 5px; text-align: center;  background: #f6f6f6; cursor: pointer;font-size: 10px;}
            .tabby-tab label:hover {background: #ddd;}
            .tabby-content {position: absolute; left: 0; bottom: 0; right: 0; top: 22px; transition: opacity 2s ease, transform 2s ease; opacity: 0;}
            .tabby-tab [type=radio] { display: none; }
            [type=radio]:checked ~ label {background: #eee;}
            [type=radio]:checked ~ label ~ .tabby-content {opacity: 1;}
            @media (max-width: 390px) {
            .tabs {
                min-height: 300px;
                }
            }
            @media (min-width: 391px) and (max-width: 451px) {
            .tabs {
                min-height: 335px;
                }
            }

            @property --progress-value {
            syntax: '<integer>';
            inherits: true;
            initial-value: 0;
            }
            :root {
            --progress-bar-color: #cfd8dc;
            --progress-value-color: #2196f3;
            --progress-empty-color-h: 4.1;
            --progress-empty-color-s: 89.6;
            --progress-empty-color-l: 58.4;
            --progress-filled-color-h: 122.4;
            --progress-filled-color-s: 39.4;
            --progress-filled-color-l: 49.2;
            }
            progress[value] {
            display: block;
            position: relative;
            appearance: none;
            width: 100%;
            height: 6px;
            border: 0;
            counter-reset: progress var(--progress-value);
            --progress-value-string: counter(progress) '';
            --progress-max-decimal: calc(var(--value, 0) / var(--max, 0));
            --progress-value-decimal: calc(var(--progress-value, 0) / var(--max, 0));
            @supports selector(::-moz-progress-bar) {
                --progress-value-decimal: calc(var(--value, 0) / var(--max, 0));
            }
            --progress-value-percent: calc(var(--progress-value-decimal) * 100%);
            --progress-value-color: hsl(
                calc((var(--progress-empty-color-h) + (var(--progress-filled-color-h) - var(--progress-empty-color-h)) * var(--progress-value-decimal)) * 1deg)
                calc((var(--progress-empty-color-s) + (var(--progress-filled-color-s) - var(--progress-empty-color-s)) * var(--progress-value-decimal)) * 1%)
                calc((var(--progress-empty-color-l) + (var(--progress-filled-color-l) - var(--progress-empty-color-l)) * var(--progress-value-decimal)) * 1%)
            );
            animation: calc(60s * var(--progress-max-decimal)) linear 0s 1 normal both progress;
            }

            progress[value]::-webkit-progress-bar {
            background-color: var(--progress-bar-color);
            border-radius: var(--border-radius);
            overflow: hidden;
            }

            progress[value]::-webkit-progress-value {
            width: var(--progress-value-percent) !important;
            background-color: var(--progress-value-color);
            border-radius: var(--border-radius);
            }

            progress[value]::-moz-progress-bar {
            width: var(--progress-value-percent) !important;
            background-color: var(--progress-value-color);
            border-radius: var(--border-radius);
            }
            progress[value]::after {
            display: flex;
            align-items: center;
            justify-content: center;
            --size: 28px;
            width: var(--size);
            height: var(--size);
            position: absolute;
            left: var(--progress-value-percent);
            top: 50%;
            transform: translate(-50%, -50%);
            background-color: var(--progress-value-color);
            border-radius: 50%;
            content: attr(value);
            content: var(--progress-value-string, var(--value));
            font-size: 14px;
            font-weight: 700;
            color: #fff;
            transition: all 0.5s linear;
            }
            @keyframes progress {
                from {
                    --progress-value: 0;
                } to {
                    --progress-value: var(--value);
                }
            }

            </style>
                </head>
                    <body class="opengeimer">
                        <div class="general-page area">
                            <div class="clock">
                                <div class="time"></div>
                                <div class="date-time"></div>
                            </div>
                            <div class="progressbar"><span class="progress"></span><p>Показания обновляются раз в минуту</p></div>
                            <progress value="100" max="100" style="--value: 60; --max: 60;"></progress>
                            <div class="container">
                                <h1 class="diag">Показания датчиков</h1>
                            </div>
                            <div class="container">
                                <div class="CT">
                                    <h2>Помещение <span>КТ</span><span id="refreshA" class="itstime">"""
                + A.D_F.datetime(ct_value.timestamp)
                + """</span></h2>
                                    <div class="oops-6712854923">
                                        <div class="couple">
                                        <div class="row">
                                            <div class="current-c">Влажность <span id="refreshB">"""
                + str(ct_value.humidity)
                + """ %</span></div>
                                            <div class="current-c info-small">[ """
                + js(
                    (
                        str(A.S.get(A.CT_S.CT_ROOM_MIN_HUMIDITY)),
                        "-",
                        str(A.S.get(A.CT_S.CT_ROOM_MAX_HUMIDITY)),
                    )
                )
                + """ ] %</div>
                                        </div>
                                        <div class="row">
                                            <div class="current-c">Температура <span id="refreshC">"""
                + str(ct_value.temperature)
                + """ °C</span></div>
                                            <div class="current-c info-small">[ """
                + js(
                    (
                        str(A.S.get(A.CT_S.CT_ROOM_MIN_TEMPERATURE)),
                        "-",
                        str(A.S.get(A.CT_S.CT_ROOM_MAX_TEMPERATURE)),
                    )
                )
                + """ ] °C</div>
                                        </div>
                                        </div>
                                        <!-- Изображение влажности и температуры -->
                                        <div id="refreshD" class="current-c humidity">
                                            <div class="tabs">
                                                <div class="tabby-tab">
                                                <input type="radio" id="tab-1" name="tabby-tabs" checked>
                                                <label for="tab-1">День</label>
                                                <div class="tabby-content">"""
                + ct_day_image_content
                + """</div>
                                                </div>

                                                <div class="tabby-tab">
                                                <input type="radio" id="tab-2" name="tabby-tabs">
                                                <label for="tab-2">Неделя</label>
                                                <div class="tabby-content">"""
                + ct_week_image_content
                + """</div>
                </div>
                <div class="tabby-tab">
                <input type="radio" id="tab-3" name="tabby-tabs">
                <label for="tab-3">Месяц</label>
                <div class="tabby-content">"""
                + ct_month_image_content
                + """</div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="MRI">
                                    <h2>Помещение <span>МРТ</span><span id="refreshE" class="itstime">"""
                + A.D_F.datetime(chiller_value.timestamp)
                + """</span></h2>
                                    <div class="oops-6712854923">"""
                + chiller_display_container
                + """</div>
                                </div>
                            </div>
                        </div>
            <script>
            // Day/Night style switcher 
            var h = new Date().getHours()
            var ds = h > 6 && h < 22
            if (ds){ dayStyle();console.log("Day style") }
            if (!ds){ nightStyle();console.log("Night style") }
                        
            function nightStyle(){
            document.body.style += ";filter:invert(1);background:#000"
            }
            function dayStyle(){
            document.body.style += ";filter:invert(0)"
            }
            </script>

            <script type="text/javascript">
            /* Click Clack */
            var time = document.querySelector('.time');
            var dateTime = document.querySelector('.date-time');

            function updateClock() {
            // Get the current time, day , month and year
            var now = new Date();
            var hours = now.getHours();
            var minutes = now.getMinutes();
            //      var seconds = now.getSeconds();
            var day = now.getDay();
            var date = now.getDate();
            var month = now.getMonth();
            var year = now.getFullYear();

            // store day and month name in an array
            var dayNames = ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'];
            var monthNames = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'];

            // format date and time
            hours = hours % 24 || 24;
            minutes = minutes < 10 ? '0' + minutes : minutes;
            //      seconds = seconds < 10 ? '0' + seconds : seconds;
            date = date < 10 ? '0' + date : date;

            // display date and time
            var period = hours < 24 ? '' : '';
            time.innerHTML = hours + '<span class="dots">:</span>' + minutes ;
            dateTime.innerHTML = dayNames[day] + ' / ' + monthNames[month] + ' ' + date + ' / ' + year;
            }

            updateClock();
            setInterval(updateClock, 1000);
            </script>

            <script>
            var id = localStorage.checked;
            if(id) document.getElementById(id).checked = true
            var input = document.getElementsByName('tabby-tabs');
                for (var i=0; i<input.length; i++)  {
                input[i].onclick = function() {
                localStorage.checked =  this.id ;
                } }
            </script>

                    </body>
            </html>
            """
            )

            return HTMLResponse(content)

        def get_autoupdate_page(title: str, content: str, time: int) -> str:
            return f'<!DOCTYPE html><html><head><title>{title}</title><meta http-equiv="refresh" content="{time}"></head><body>{content}</body></html>'

        def get_ct_content(value: CTIndicationsValueContainer) -> str:
            return f'<h2><span style="font-family: Verdana,Geneva,sans-serif;"><span style="color: #ffffff;"><strong><span style="background-color: #3498db;">&nbsp;Показания в помещении КТ *&nbsp;</span></strong></span></span></h2>\
                        <table style="width: 100%;" border="0" cellspacing="0" cellpadding="0">\
                            <tbody>\
                                <tr>\
                                    <td style="width: 240px;">\
                                        <ul>\
                                            <li><span style="color: #ffffff;"><strong><span style="font-family: Verdana,Geneva,sans-serif;"><span style="background-color: #27ae60;">&nbsp;Время измерения&nbsp;</span></span></strong></span></li>\
                                        </ul>\
                                    </td>\
                                    <td><span style="font-family: Verdana,Geneva,sans-serif;"><span\
                                                style="font-size: 16px;"><strong>{A.D_F.datetime(value.timestamp)}</strong>&nbsp;</span></span></td>\
                                </tr>\
                                <tr>\
                                    <td style="width: 240px;">\
                                        <ul>\
                                            <li><span style="font-family: Verdana,Geneva,sans-serif;"><span\
                                                        style="background-color: #27ae60;">&nbsp;<span\
                                                            style="color: #ffffff;"><strong>Температура</strong>&nbsp;</span></span></span></li>\
                                        </ul>\
                                    </td>\
                                    <td style="width: 240px;"><span style="font-family: Verdana,Geneva,sans-serif;"><span\
                                                style="font-size: 18px;"><strong>{value.temperature}{A.CT_V.TEMPERATURE_SYMBOL}</strong>&nbsp;</span></span></td>\
                                </tr>\
                                <tr>\
                                    <td style="width: 240px;">\
                                        <ul>\
                                            <li><span style="font-family: Verdana,Geneva,sans-serif;"><span\
                                                        style="background-color: #27ae60;">&nbsp;<span style="color: #ffffff;"><strong>Влажность\
                                                                &nbsp;</strong></span></span></span></li>\
                                        </ul>\
                                    </td>\
                                    <td style="width: 240px;"><span style="font-size: 18px;"><strong><span\
                                                    style="font-family: Verdana,Geneva,sans-serif;">{value.humidity}%</span></strong></span></td>\
                                </tr>\
                            </tbody>\
                        </table>'

        def create_indications_table(value: list[str]) -> str:
            table_content: str = (
                '<table style="width: 100%; border-collapse: collapse; border-style: solid;" border="0"><tbody>'
            )
            for index, item in enumerate(value):
                if (index + 1) % 2 == 1:
                    table_content += '<tr style="vertical-align: top">'
                table_content += f'<td style="width: 50%;">{item}</td>'
                if (index + 1) % 2 == 0:
                    table_content += "</tr>"
            table_content += "</tbody></table>"
            return (
                table_content
                + '<p style="width:100%;display:block;"><span style="width:100%;display:block;color: #ffffff;"><span style="font-family: Verdana,Geneva,sans-serif;"><strong><span style="background-color: #000000;">&nbsp;* Страница с показаниями обновляется автоматически каждую минуту&nbsp;</span></strong></span></span></p>'
            )

        def get_mri_content(value: ChillerIndicationsValueContainer) -> str:
            path: str = A.PTH_IND.CHILLER_DATA_IMAGE_LAST
            modification_timstamp: float = os.path.getmtime(path)
            modification_datetime: datetime | None = datetime.fromtimestamp(
                modification_timstamp
                if modification_timstamp > 0
                else os.path.getctime(path)
            )
            indicators_string_list: list[str] = (
                A.D_F.by_formatter_name(
                    A.CT_D.FORMATTER.CHILLER_INDICATIONS_VALUE_INDICATORS,
                    value.indicators,
                )
                .strip()
                .splitlines()
            )
            indicators_string: str = ""
            for indicatior_string in indicators_string_list:
                indicators_string += f'<span style="font-size: 14px;"><strong><span\
                                                    style="font-family: Verdana,Geneva,sans-serif;">{indicatior_string}</span></strong></span><br/>'
            return f'<h2><span style="font-family: Verdana, Geneva, sans-serif; background-color: #3498db;"><span style="color: #ffffff;"><strong>&nbsp;Показания в техническом помещении МРТ *&nbsp;</strong></span></span></h2>\
                <p><span style="background-color: #333333; color: #ffffff;"><span style="font-family: Verdana,Geneva,sans-serif;"><strong>&nbsp;Показания чиллера&nbsp;</strong></span></span></p>\
                <table style="width: 100%;" border="0" cellspacing="0" cellpadding="0">\
                    <tbody>\
                        <tr style="height: 46px;">\
                            <td style="width: 240px; height: 46px;">\
                                <ul>\
                                    <li><span style="font-family: Verdana,Geneva,sans-serif;"><span\
                                                style="font-size: 16px; background-color: #27ae60;">&nbsp;<span\
                                                    style="color: #ffffff;"><strong>Время измерения</strong>&nbsp;</span></span></span></li>\
                                </ul>\
                            </td>\
                            <td style="width: 240px; height: 46px;"><span style="font-family: Verdana,Geneva,sans-serif;"><strong>{A.D_F.datetime(value.timestamp)}</strong></strong></span></td>\
                        </tr>\
                        <tr style="height: 46px;">\
                            <td style="width: 240px; height: 46px;">\
                                <ul>\
                                    <li><span style="font-family: Verdana,Geneva,sans-serif;"><span\
                                                style="background-color: #27ae60;">&nbsp;<span\
                                                    style="color: #ffffff;"><strong>Температура</strong>&nbsp;</span></span></span></li>\
                                </ul>\
                            </td>\
                            <td style="width: 240px; height: 46px;"><span style="font-family: Verdana,Geneva,sans-serif;"><span\
                                        style="font-size: 18px;"><strong>{value.temperature}{A.CT_V.TEMPERATURE_SYMBOL}</strong></span></span></td>\
                        </tr>\
                        <tr style="height: 65px;">\
                            <td style="width: 240px; height: 65px;">\
                                <ul>\
                                    <li><span style="font-family: Verdana,Geneva,sans-serif;"><span\
                                                style="background-color: #27ae60;">&nbsp;<span\
                                                    style="color: #ffffff;"><strong>Индикаторы&nbsp;</strong></span></span></span></li>\
                                </ul>\
                            </td>\
                            <td style="width: 400px; height: 65px;">\
                                {indicators_string}\
                            </td>\
                        </tr>\
                    </tbody>\
                </table>\
                <p><span style="color: #ffffff;"><span style="font-family: Verdana,Geneva,sans-serif;"><strong><span style="background-color: #333333;">&nbsp;Изображение дисплея\
                                чиллера&nbsp;</span></strong></span></span></p>\
            <p><img alt="Изображение дисплея" src="data:image/jpeg;base64,{A.D_CO.file_to_base64(A.PTH.INDICATIONS.CHILLER_DATA_IMAGE_LAST_RESULT)}"/></p>\
            <table border="0" cellspacing="0" cellpadding="0">\
                    <tbody>\
                    <tr>\
                    <td>\
                    <ul>\
                    <span style="color: #ffffff;"><strong><span style="font-family: Verdana,Geneva,sans-serif;"><span style="background-color: #27ae60;">&nbsp;Время снятия изображения&nbsp;</span></span></strong></span>\
                    </ul>\
                    </td>\
                    <td><span style="font-family: Verdana,Geneva,sans-serif;">&nbsp;&nbsp;<strong>{A.D_F.datetime(modification_datetime)}</span></td>\
                    </tr>\
                    </tbody>\
                        </table>'

        @app.get("/ct")
        def get_ct() -> None:
            return HTMLResponse(
                get_autoupdate_page(
                    "Показания",
                    get_ct_content(
                        A.R.get_first_item(A.R_IND.last_ct_value_containers(True))
                    ),
                    A.CT.HEART_BEAT_PERIOD,
                )
            )

        @app.get("/mri")
        def get_ch() -> None:
            return HTMLResponse(
                get_autoupdate_page(
                    "Показания",
                    get_mri_content(
                        A.R.get_first_item(A.R_IND.last_chiller_value_containers(True))
                    ),
                    A.CT.HEART_BEAT_PERIOD,
                )
            )

        @app.get("/hello")
        def get_hello() -> None:
            return HTMLResponse("hello")

        @app.post("/register_device")
        def register_device_handler(
            device: IndicationDeviceModel, request: Request
        ) -> None:
            A.E.send(
                *A.E_B.indication_device_was_registered(
                    A.D.fill_data_from_source(
                        IndicationDevice(
                            ip_address=(request.client.host, request.client.port)
                        ),
                        device,
                    )
                )
            )

        """@app.post("/ict")
        def ict_handler(income_indications_value: IncomeCTIndicationsValue) -> None:
            income_indications_value.temperature = (
                ceil(
                    (
                        income_indications_value.temperature
                        + float(A.S.get(A.CT_S.CT_INDICATIONS_VALUE_TEMPERATURE_CORRECTION))
                    )
                    * 100
                )
                / 100
            )
            A.A_IND_CT.register(
                CTIndicationsValue(
                    income_indications_value.temperature, income_indications_value.humidity
                )
            )"""

        @app.post("/ich")
        def ich_handler(value: UploadFile = UploadFile(...)) -> None:
            path: str = A.PTH_IND.CHILLER_DATA_IMAGE_LAST
            with open(path, "wb+") as file:
                shutil.copyfileobj(value.file, file)
            # A.A_IND_CH.register(ChillerIndicationsValue())

        @app.get("/door/{door_operation}/{door_name}")
        async def on_door_action(door_operation: str, door_name: str):
            action: A.CT_ACT | None = None
            if A.D.equal("open", door_operation):
                action = A.CT_ACT.DOOR_OPEN
            elif A.D.equal("close", door_operation):
                action = A.CT_ACT.DOOR_CLOSE
            if nn(action):
                A.A_ACT.was_done(action, parameters=[door_name])
                return js(
                    (
                        "Начат процесс",
                        ["закрытия", "открытия"][action == A.CT_ACT.DOOR_OPEN],
                        "дверей",
                    )
                )

        @app.get("/action/{action_name}")
        async def on_action(action_name: str):
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
        async def on_execute(file_name: str, request: Request):
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
            result: list[str] | None = A.R_F.execute(
                file_name, {"parameters": parameters}
            )
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
            SD, starts_handler=service_starts_handler, isolate=ISOLATED, as_standalone=as_standalone
        )


if __name__ == "__main__":
    start()

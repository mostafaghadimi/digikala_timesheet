from enum import Enum


class WebElements(Enum):
    TYPE = "_easyui_textbox_input3"
    STATUS = "_easyui_textbox_input2"
    DAILY_END_DATE = "_easyui_textbox_input6"
    HOURLY_TO_HOUR = "_easyui_textbox_input7"
    HOURLY_END_DATE = "_easyui_textbox_input6"
    DAILY_START_DATE = "_easyui_textbox_input4"
    HOURLY_FROM_HOUR = "_easyui_textbox_input5"
    HOURLY_START_DATE = "_easyui_textbox_input4"
    SAVE_BUTTON = "sg-LeaveRequestBoard-ib0-ref6-idun"


class RowDetails(Enum):
    DAILY = "روزانه"
    HOURLY = "ساعتی"
    REMOTE = "کارکرد ریموت"
    SICK_LEAVE = "مرخصی استعلاجی"
    ELIGIBLE_LEAVE = "مرخصی استحقاقی"
    CONSENSUAL_LEAVE = "مرخصی توافقی"


class ExcelColNames(Enum):
    DATE = "Date"
    TYPE = "Type"
    STATUS = "Status"
    TO_HOUR = "To Hour"
    FROM_HOUR = "From Hour"





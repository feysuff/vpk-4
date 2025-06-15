import base64

VERIFIER_SEAL = "verifier_seal"
LICENSE_SIGNATURE = "license_signature"


def check_operation(id, details):
    authorized = False

    src = details["source"]
    dst = details["destination"]
    operation = details["operation"]

    if dst == 'comm_infra':
        authorized = True

    # Коммуникационная инфраструктура может отправлять данные брокеру
    if src == 'comm_infra' and dst == 'message_broker':
        authorized = True

    # Брокер может отправить данные обратно в коммуникационную инфраструктуру
    if src == 'message_broker' and dst == 'comm_infra':
        authorized = True

    # Коммуникационная инфраструктура может передать данные АСУ ТЭЦ
    if src == 'comm_infra' and dst == 'asu_teс':
        authorized = True
        # Коммуникационная инфраструктура может передать данные Оператору ARM
    if src == 'comm_infra' and dst == 'operator_arm':
        authorized = True

    if src == 'operator_arm' and dst == 'message_broker' : 
        authorized = True 
    if src == 'message_broker' and dst == 'operator_arm' : 
        authorized = True 

    if src == 'message_broker' and dst == 'asu_teс' \
            and operation == 'control_command_from_operator':
        authorized = True  # Команда оператора на управление

    if src == 'asu_teс' and dst == 'message_broker' : 
        authorized = True

    if src == 'operator_arm' and dst == 'asu_teс':
        authorized = True
    
    if src == 'asu_teс' and dst == 'plc' \
            and operation == 'validated_command_from_asu':
        authorized = True

    if src == 'plc' and dst == 'pmessage_broker' :
        authorized = True

    if src == 'message_broker' and dst == 'plc' :
        authorized = True
        

    # ПЛК управляет оборудованием 
    if src == 'plc' and dst == 'equipment' \
            and operation == 'execute_command':
        authorized = True

    if src == 'equipment' and dst == 'message_broker': 
        authorized = True
    if src == 'message_broker' and dst == 'equipment': 
        authorized = True

    # Оборудование отправляет статус ПЛК 
    if src == 'equipmen' and dst == 'plc' \
            and operation == 'equipment_status_update':
        authorized = True

    # ПЛК отправляет статус АСУ ТЭЦ
    if src == 'plc' and dst == 'asu_teс' \
            and operation == 'status_to_asu':
        authorized = True

    # Брокер сообщений → Наблюдатель 
    if src == 'message_broker' and dst == 'observer' \
            and operation == 'incident_notification':
        authorized = True

    # АСУ ТЭЦ → Наблюдатель 
    if src == 'asu_teс' and dst == 'observer' \
            and operation == 'status_for_observer':
        authorized = True

    # АСУ ТЭЦ отображает статус оператору 
    if src == 'asu_teс' and dst == 'operator_arm' \
            and operation == 'status_display':
        authorized = True

    # ПЛК отправляет диагностические данные в систему диагностики 
    if src == 'plc' and dst == 'diagnostic_system' \
            and operation == 'plc_diagnostic_data':
        authorized = True

    if src == 'diagnostic_system' and dst == 'message_broker' : 
        authorized = True

    if src == 'message_broker' and dst == 'diagnostic_system' : 
        authorized = True

    # Система диагностики передаёт результат в АСУ ТЭЦ 
    if src == 'diagnostic_system' and dst == 'asu_teс' \
            and operation == 'diagnostic_to_asu':
        authorized = True

    # АСУ ТЭЦ передает данные инженеру по автоматизации 
    if src == 'asu_teс' and dst == 'automation_engineer' \
            and operation == 'asu_to_engineer_update':
        authorized = True

    if src == 'automation_engineer' and dst == 'message_broker' : 
        authorized = True

    if src == 'message_broker' and dst == 'automation_engineer' : 
        authorized = True

    # Инженер по автоматизации обновляет прикладную программу 
    if src == 'automation_engineer' and dst == 'app_program' \
            and operation == 'send_update':
        authorized = True

    if src == 'app_program' and dst == 'message_broker' : 
        authorized = True

    if src == 'message_broker' and dst == 'app_program' : 
        authorized = True

    # Прикладная программа запрашивает проверку лицензии на режим 
    if src == 'app_program' and dst == 'license_for_mode' \
            and operation == 'request_license_validation':
        authorized = True

     # Система верификации → Прикладная программа ===
    if src == '	verification_system' and dst == 'app_program' \
            and operation == 'verification_result':
        authorized = True

    # Проверка обновления в системе верификации 
    if src == 'message_broker' and dst == 'verification_system' \
            and operation == 'verify_app_update':
        authorized = True 
    if src == 'verification_system' and dst == 'message_broker' : 
        authorized = True


     # Система верификации → Система диагностики 
    if src == '	verification_system' and dst == 'diagnostic_system' \
            and operation == 'verification_status_to_diagnostics':
        authorized = True
     # Система верификации → Лицензия на режимы ПП 
    if src == '	verification_system' and dst == 'license_for_mode' \
            and operation == 'license_check_request':
        authorized = True

    # Проверка лицензии на режим ПП 
    if src == 'message_broker' and dst == 'license_for_mode' \
            and operation == 'verify_license_for_mode':
        authorized = True

    # Система лицензий разрешает запуск ПП 
    if src == 'license_for_mode' and dst == 'app_program' \
            and operation == 'license_confirmed':
        authorized = True

    if src == 'license_for_mode' and dst == 'message_broker' : 
        authorized = True

    if src == 'message_broker' and dst == 'license_for_mode' : 
        authorized = True

    # Лицензия на режимы ПП → Система диагностики 
    if src == 'license_for_mode' and dst == 'diagnostic_system' \
            and operation == 'license_status_to_diagnostics':
        authorized = True

    # Система мониторинга безопасности получает данные от всех 
    if src == 'message_broker' and dst == 'security_monitor' \
            and operation == 'collect_security_data':
        authorized = True

    if src == 'security_monitor' and dst == 'message_broker' \
            and operation == 'report_security_status':
        authorized = True
    

    return authorized



def check_payload_seal(payload):
    try:
        p = base64.b64decode(payload).decode()
        if p.endswith(VERIFIER_SEAL) or p.endswith(LICENSE_SIGNATURE):
            print('[info] payload seal is valid')
            return True
    except Exception as e:
        print(f'[error] seal check error: {e}')
    return False
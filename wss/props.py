TC = {
    "TC_000_BOOT" : [
        ["BootNotification", {}],
        ["StatusNotification", {"status": "Available"}],
        ["Authorize", {"idTag": "1031040000069641"}]
    ],
    # "TC_003" : [
    #     ["BootNotification", {}],
    #     ["StatusNotification", {"status": "Available"}],
    #     ["Authorize", {"idTag": "1031040000069641"}],
    #     ["StartTransaction", {"idTag": "1031040000069641"}],
    #     ["StatusNotification", {"status": "Charging"}],
    #     ["MeterValues", {"transactionId":None}],
    #     ["StopTransaction", {"transactionId": None}],
    #     ["StatusNotification", {"status": "Finishing"}],
    #     ["StatusNotification", {"status": "Available"}],
    # ],
    # "TC_004_1" : [
    #     ["BootNotification", {}],
    #     ["Authorize", {"idTag": "1031040000069641"}],
    #     ["StatusNotification", {"status": "Preparing"}],
    #     ["StartTransaction", {"idTag": "1031040000069641"}],
    #     ["StatusNotification", {"status": "Charging"}],
    #     ["MeterValues", {"transactionId":None}],
    #     ["StopTransaction", {"transactionId": None}],
    #     ["StatusNotification", {"status": "Finishing"}],
    #     ["StatusNotification", {"status": "Available"}],
    # ],
    # "TC_004_2": [
    #     ["BootNotification", {}],
    #     ["Authorize", {"idTag": "1031040000069641"}],
    #     ["StatusNotification", {"status": "Preparing"}],
    #     ["StatusNotification", {"status": "Available"}],
    # ],
    # "TC_005_1": [
    #     ["BootNotification", {}],
    #     ["StatusNotification", {"status": "Preparing"}],
    #     ["Authorize", {"idTag": "1031040000069641"}],
    #     ["StartTransaction", {"idTag": "1031040000069641"}],
    #     ["StatusNotification", {"status": "Charging"}],
    #     ["MeterValues", {"transactionId":None}],
    #     ["StatusNotification", {"status": "SuspendedEV"}],
    #     ["StopTransaction", {"transactionId": None}],
    #     ["StatusNotification", {"status": "Finishing"}],
    #     ["StatusNotification", {"status": "Available"}],
    # ],
    # "TC_061": [
    #     ["BootNotification", {}],
    #     ["Wait", "Reset"],
    #     ["Reply", "Reset"],
    # ],
    # "TC_010": [
    #     ["BootNotification", {}],
    #     ["StatusNotification", {"status": "Preparing"}],
    #     ["Wait", "RemoteStartTransaction"],
    #     ["Reply", "RemoteStartTransaction"],
    #     ["Authorize", {"idTag": "1031040000069641"}],
    #     ["StartTransaction", {"idTag": "1031040000069641"}],
    #     ["StatusNotification", {"status": "Charging"}],
    #     ["StopTransaction", {"transactionId": None}],
    #     ["StatusNotification", {"status": "Finishing"}],
    #     ["StatusNotification", {"status": "Available"}],
    # ],
    # "TC_011_1": [
    #     ["BootNotification", {}],
    #     ["Wait", "RemoteStartTransaction"],
    #     ["Reply", "RemoteStartTransaction"],
    #     ["Authorize", {"idTag": "1031040000069641"}],
    #     ["StatusNotification", {"status": "Preparing"}],
    #     ["StartTransaction", {"idTag": "1031040000069641"}],
    #     ["StatusNotification", {"status": "Charging"}],
    #     ["Wait", "RemoteStopTransaction"],
    #     ["Reply", "RemoteStopTransaction"],
    #     ["StopTransaction", {"transactionId": None}],
    #     ["StatusNotification", {"status": "Finishing"}],
    #     ["StatusNotification", {"status": "Available"}],
    # ],
    # "TC_011_2": [
    #     ["BootNotification", {}],
    #     ["Wait", "RemoteStartTransaction"],
    #     ["Reply", "RemoteStartTransaction"],
    #     ["Authorize", {"idTag": "1031040000069641"}],
    #     ["StatusNotification", {"status": "Preparing"}],
    #     ["StatusNotification", {"status": "Available"}],
    # ],
    # "TC_012": [
    #     ["BootNotification", {}],
    #     ["StatusNotification", {"status": "Preparing"}],
    #     ["Wait", "RemoteStartTransaction"],
    #     ["Reply", "RemoteStartTransaction"],
    #     ["Authorize", {"idTag": "1031040000069641"}],
    #     ["StartTransaction", {"idTag": "1031040000069641"}],
    #     ["StatusNotification", {"status": "Charging"}],
    #     ["Wait", "RemoteStopTransaction"],
    #     ["Reply", "RemoteStopTransaction"],
    #     ["StopTransaction", {"transactionId": None}],
    #     ["StatusNotification", {"status": "Finishing"}],
    #     ["StatusNotification", {"status": "Available"}],
    # ],
    # "TC_013": [
    #     ["BootNotification", {}],
    #     ["Wait", "Reset"],
    #     ["Reply", "Reset"],
    #     ["BootNotification", {}],
    #     ["StatusNotification", {"status": "Available"}],
    # ],
    # "TC_014": [
    #     ["Wait", "Reset"],
    #     ["Reply", "Reset"],
    #     ["BootNotification", {}],
    #     ["StatusNotification", {"status": "Available"}],
    # ],
    # "TC_017_1": [
    #     ["Wait", "Reset"],
    #     ["Reply", "Reset"],
    #     ["BootNotification", {}],
    #     ["StatusNotification", {"status": "Available"}],
    # ],
    # "TC_018": [
    #     ["BootNotification", {}],
    #     ["StatusNotification", {"status": "Preparing"}],
    #     ["Wait", "RemoteStartTransaction"],
    #     ["Reply", "RemoteStartTransaction"],
    #     ["Authorize", {"idTag": "1031040000069641"}],
    #     ["StartTransaction", {"idTag": "1031040000069641"}],
    #     ["StatusNotification", {"status": "Charging"}],
    #     ["Wait", "UnlockConnector"],
    #     ["Reply", "UnlockConnector"],
    #     ["StatusNotification", {"status": "Finishing"}],
    #     ["StopTransaction", {"transactionId": None, "reason":"UnlockCommand"}],
    #     ["StatusNotification", {"status": "Available"}],
    # ],
    # "TC_019": [
    #     ["Wait", "GetConfiguration"],
    #     ["Reply", "GetConfiguration"],
    #     ["StatusNotification", {"status": "Available"}],
    # ],
    # "TC_021": [
    #     ["BootNotification", {}],
    #     ["Wait", "ChangeConfiguration"],
    #     ["Reply", "ChangeConfiguration"],
    # ],
    # "TC_023": [
    #     ["BootNotification", {}],
    #     ["Authorize", {"idTag": "1031040000069642"}], # 없는 번호
    #     ["Authorize", {"idTag": "1031040000069642"}],  # Expired 카드상태02 카드변호 변경 필요
    #     ["Authorize", {"idTag": "1031040000069642"}],  # Blocked 카드변호 변경 필요
    # ],
    # "TC_024": [
    #     ["BootNotification", {}],
    #     ["Authorize", {"idTag": "1031040000069641"}],
    #     ["StatusNotification", {"status": "Preparing"}],
    #     ["StatusNotification", {"status": "Faulted"}],
    # ],
    # "TC_026": [
    #     ["BootNotification", {}],
    #     ["Wait", "RemoteStartTransaction"],
    #     ["Reply", "RemoteStartTransaction", {"status":"Rejected"}],
    # ],
    # "TC_028": [
    #     ["BootNotification", {}],
    #     ["Wait", "RemoteStopTransaction"],
    #     ["Reply", "RemoteStopTransaction", {"status": "Rejected"}],
    # ],
    # "TC_030": [
    #     ["BootNotification", {}],
    #     ["Wait", "UnlockConnector"],
    #     ["Reply", "UnlockConnector", {"status": "UnlockFailed"}],
    # ],
    # "TC_032": [
    #     ["BootNotification", {}],
    #     ["StatusNotification", {"status": "Preparing"}],
    #     ["Wait", "RemoteStartTransaction"],
    #     ["Reply", "RemoteStartTransaction"],
    #     ["Authorize", {"idTag": "1031040000069641"}],
    #     ["StartTransaction", {"idTag": "1031040000069641"}],
    #     ["StatusNotification", {"status": "Charging"}],
    #     ["BootNotification", {}],
    #     ["StatusNotification", {"status": "Unavailable"}],
    #     ["StopTransaction", {"idTag": "1031040000069641",
    #         "meterStop": 29000,
    #         "timestamp": "2023-02-24T07:26:57.512Z",
    #         "transactionId": 120531947,
    #         "reason": "PowerLoss",
    #         "transactionData": [
    #           {
    #             "sampledValue": [
    #               {
    #                 "value": "29000",
    #                 "measurand": "Energy.Active.Import.Register",
    #                 "unit": "Wh"
    #               }
    #             ],
    #             "timestamp": "2023-02-24T07:26:57.512Z"
    #           }
    #         ]}
    #      ],
    #     ["StatusNotification", {"status": "Finishing"}],
    # ],
    # "TC_037": [
    #     ["BootNotification", {}],
    #     ["StatusNotification", {"status": "Preparing"}],
    #     ["Authorize", {"idTag": "1031040000069641"}],
    #     ["StartTransaction", {"idTag": "1031040000069641"}],
    #     ["StatusNotification", {"status": "Charging"}],
    #     ["StopTransaction", {"transactionId": None, "reason": "Local"}],
    #     ["StatusNotification", {"status": "Finishing"}],
    #     ["StatusNotification", {"status": "Available"}],
    # ],
    # "TC_037_3": [
    #     ["BootNotification", {}],
    #     ["StatusNotification", {"status": "Preparing"}],
    #     ["Authorize", {"idTag": "1031040000069641"}],
    #     ["StartTransaction", {"idTag": "1031040000069641"}],
    #     ["StatusNotification", {"status": "Charging"}],
    #     ["StopTransaction", {"transactionId": None, "reason": "DeAuthorized"}],
    #     ["StatusNotification", {"status": "Finishing"}],
    #     ["StatusNotification", {"status": "Available"}],
    # ],
    # "TC_039": [
    #     ["BootNotification", {}],
    #     ["StatusNotification", {"status": "Preparing"}],
    #     ["StartTransaction", {
    #         "idTag": "1031040000069641",
    #         "meterStart": 0,
    #         "timestamp": "2023-02-24T07:26:57.512Z"
    #         }
    #      ],
    #     ["StatusNotification", {"status": "Charging"}],
    #     ["StopTransaction", {"transactionId": None, "meterStop": 29000,"reason": "Local", "timestamp": "2023-02-24T07:26:57.512Z"}],
    #     ["StatusNotification", {"status": "Finishing"}],
    #     ["StatusNotification", {"status": "Available"}],
    # ],
    "TC_040_1": [
        ["BootNotification", {}],
        ["Wait", "ChangeConfiguration", {"UnknownConfigurationKey":"300"}],
        ["Reply", "ChangeConfiguration", {"status":"NotSupported"}],
    ],
    # "TC_040_2": [
    #     ["BootNotification", {}],
    #     ["Wait", "ChangeConfiguration",{"key": "MeterValueSampleInterval", "value": "-1"}],
    #     ["Reply", "ChangeConfiguration", {"status": "Rejected"}],
    # ],
    "TC_042_1": [
        ["BootNotification", {}],
        ["Wait", "GetLocalListVersion"],
        ["Reply", "GetLocalListVersion", {"listVersion":-1}],
    ],
    "TC_042_2": [
        ["BootNotification", {}],
        ["Wait", "GetLocalListVersion"],
        ["Reply", "GetLocalListVersion", {"listVersion":0}],
    ],
    "TC_043": [
        ["BootNotification", {}],
        ["Wait", "SendLocalList", {
              "listVersion": 1,
              "localAuthorizationList": [
                {
                  "idTag": "1031040000069641",
                  "idTagInfo": {
                    "expiryDate": "2023-05-31T23:59:59Z",
                    "status": "Accepted"
                  }
                },
                {
                  "idTag": "1031040000072645",
                  "idTagInfo": {
                    "expiryDate": "2023-05-31T23:59:59Z",
                    "status": "Accepted"
                  }
                },
                {
                  "idTag": "1031040000054551",
                  "idTagInfo": {
                    "expiryDate": "2023-05-31T23:59:59Z",
                    "status": "Accepted"
                  }
                }
              ],
              "updateType": "Full"
            }],
        ["Reply", "SendLocalList", {"status": "NotSupported"}],
    ],
    "TC_044_1": [
        ["BootNotification", {}],
        ["Wait", "UpdateFirmware", {"location": "https://s3~~~~", "retrieveDate": "2023-04-15T10:15:00Z" }],
        ["Reply", "UpdateFirmware"],
        ["StatusNotification", {"status": "Unavailable"}],
        ["FirmwareStatusNotification", {"status": "Downloading"}],
        ["FirmwareStatusNotification", {"status": "Downloaded"}],
        ["FirmwareStatusNotification", {"status": "Installing"}],
        ["StatusNotification", {"status": "Unavailable"}],
        ["FirmwareStatusNotification", {"status": "Installed"}],
        ["BootNotification", {}],
        ["StatusNotification", {"status": "Available"}],
    ],
    "TC_045": [
        ["BootNotification", {}],
        ["Wait", "GetDiagnostics"],
        ["Reply", "GetDiagnostics"],
    ],
}
ocppDocs = {
    "BootNotification": [
        2,
        "19223201",
        "BootNotification",
        {
            "chargePointModel": "ELA007C01",
            "chargePointVendor": "EVAR",
            "chargePointSerialNumber": "EVSCA070007",
            "firmwareVersion": "0.0.13",
            "imsi": "450061222990181"
        }
    ],
    "StatusNotification": [
        2,
        "19223201",
        "StatusNotification",
        {
            "connectorId": 1,
            "errorCode": "NoError",
            "status": "Available"
        }
    ],
    "HeartBeat": [
        2,
        "19223201",
        "DataTransfer",
        {
            "vendorId": "EVAR",
            "messageId": "heartbeat",
            "data": {}
        }
    ],
    "Authorize": [
        2,
        "19223201",
        "Authorize",
        {
            "idTag": ""
        }
    ],
    "StartTransaction": [
        2,
        "1677223618",
        "StartTransaction",
        {
            "connectorId": 1,
            "idTag": "",
            "meterStart": 24000,
            "timestamp": "2023-02-24T07:26:57.512Z"
        }
    ],
    "MeterValues": [
        2,
        "1677228049",
        "MeterValues",
        {
            "connectorId": 1,
            "transactionId": 120532006,
            "meterValue": [
                {
                    "timestamp": "2023-02-24T08:40:48.839Z",
                    "sampledValue": [
                        {
                            "value": "25000",
                            "measurand": "Energy.Active.Import.Register",
                            "unit": "Wh"
                        }
                    ]
                }
            ]
        }
    ],
    "StopTransaction": [
        2,
        "1677228103",
        "StopTransaction",
        {
            "meterStop": 29000,
            "timestamp": "2023-02-24T08:41:42.615Z",
            "transactionId": 120532006
        }
    ],
    "ClearCacheResponse": [
        3,
        "2023-02-24T08:41:42.615Z",
        {
            "status": "Accepted"
        }
    ],
    "ResetResponse": [
        3,
        "2023-02-24T08:41:42.615Z",
        {
            "status": "Accepted"
        }
    ],
    "UnlockConnectorResponse": [
        3,
        "2023-02-24T08:41:42.615Z",
        {
            "status": "Unlocked"
        }
    ],
    "GetConfigurationResponse": [
        3,
        "123214123123",
        {
            "configurationKey": [{
                "key": "heartbeatInterval",
                "readonly": "true",
                "value":300
            }
            ]
        }
    ],
    "RemoteStartTransaction": [
        2,
        "321312312",
        "RemoteStartTransaction",
        {
          "idTag": "1031040000069641"
        }
    ],
    "RemoteStopTransaction": [
        2,
        "321312312",
        "RemoteStopTransaction",
        {
            "transactionId": 12321
        }
    ],
    "RemoteStopTransactionResponse": [
        3,
        "321312312",
        {
            "status":"Accepted"
        }
    ],
    "RemoteStartTransactionResponse": [
        3,
        "2023-02-24T08:41:42.615Z",
        {
            "status": "Accepted"
        }
    ],
    "Reset": [
        2,
        "321312312",
        "Reset",
        {
            "type": "Hard"
        }
    ],
    "UnlockConnector": [
        2,
        "321312312",
        "UnlockConnector",
        {
            "connectorId": 1
        }
    ],
    "GetConfiguration": [
        2,
        "321312312",
        "GetConfiguration",
        {
            "key": ["key1"]
        }
    ],
    "GetLocalListVersion": [
        2, "321312312", "GetLocalListVersion",
        {}
    ],
    "GetLocalListVersionResponse": [
        3, "321312312", {"listVersion": -1}
    ],
    "ChangeConfiguration": [
        2,
        "321312312",
        "ChangeConfiguration",
        {
            "key": "UnknownConfigurationKey",
            "value": "300"
        }
    ],
    "ChangeConfigurationResponse": [
        3, "321312312", {"status":"Accepted"}
    ],
    "SendLocalList": [
        2,
        "321312312",
        "SendLocalList",
        {
            "listVersion":0,
            "updateType":"Full"
        }
    ],
    "SendLocalListResponse": [
        3,
        "321312312",
        {
            "status":""
        }
    ],
    "UpdateFirmware": [
        2,
        "321312312",
        "UpdateFirmware",
        {
            "location": "https://s3~~~~",
            "retrieveDate": "2023-04-15T10:15:00Z"
        }
    ],
    "UpdateFirmwareResponse": [
        3,
        "321312312",
        {
        }
    ],
    "FirmwareStatusNotification": [
        2,
        "321312312",
        "FirmwareStatusNotification",
        {
            "status":"Downloading"
        }
    ],
    "GetDiagnostics": [
        2,
        "321312312",
        "GetDiagnostics",
        {
            "location": "s3://~~"
        }
    ],
    "GetDiagnosticsResponse": [
        3,
        "321312312",
        {
            "filename": "filename_diagnostics"
        }
    ],
}
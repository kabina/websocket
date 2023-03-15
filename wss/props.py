TC = {
    # "TC_000_BOOT" : [
    #     ["BootNotification", {}],
    #     ["StatusNotification", {"status": "Available"}],
    #     ["Authorize", {"idTag": "1031040000069641"}]
    # ],
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
    # ],
    "TC_010": [
        ["BootNotification", {}],
        ["StatusNotification", {"status": "Preparing"}],
        ["Wait", "RemoteStartTransaction"],
        ["Authorize", {"idTag": "1031040000069641"}],
        ["StartTransaction", {"idTag": "1031040000069641"}],
        ["StatusNotification", {"status": "Charging"}],
        ["StopTransaction", {"transactionId": None}],
        ["StatusNotification", {"status": "Finishing"}],
        ["StatusNotification", {"status": "Available"}],
    ],
    "TC_011_1": [
        ["BootNotification", {}],
        ["Wait", "RemoteStartTransaction"],
        ["Authorize", {"idTag": "1031040000069641"}],
        ["StatusNotification", {"status": "Preparing"}],
        ["StartTransaction", {"idTag": "1031040000069641"}],
        ["StatusNotification", {"status": "Charging"}],
        ["StopTransaction", {"transactionId": None}],
        ["StatusNotification", {"status": "Finishing"}],
        ["StatusNotification", {"status": "Available"}],
    ],
    "TC_011_2": [
        ["BootNotification", {}],
        ["Wait", "RemoteStartTransaction"],
        ["Authorize", {"idTag": "1031040000069641"}],
        ["StatusNotification", {"status": "Preparing"}],
        ["StatusNotification", {"status": "Available"}],
    ],
    "TC_012": [
        ["BootNotification", {}],
        ["StatusNotification", {"status": "Preparing"}],
        ["Wait", "RemoteStartTransaction"],
        ["Authorize", {"idTag": "1031040000069641"}],
        ["StartTransaction", {"idTag": "1031040000069641"}],
        ["StatusNotification", {"status": "Charging"}],
        ["Wait", "RemoteStopTransaction"],
        ["StopTransaction", {"transactionId": None}],
        ["StatusNotification", {"status": "Finishing"}],
        ["StatusNotification", {"status": "Available"}],
    ],
    "TC_013": [
        ["BootNotification", {}],
        ["Wait", "Reset"],
        ["BootNotification", {}],
        ["StatusNotification", {"status": "Available"}],
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
    "ClearCacheResponse": [
        3,
        "2023-02-24T08:41:42.615Z",
        {
            "status": "Accepted"
        }
    ],
}
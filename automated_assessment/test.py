from azext_mlclassicextension.workspace import MLClassicWorkspace

ws = MLClassicWorkspace('800c1fcc64d446f18d1cc53471fd76e3', 'japaneast', 'https://japaneast.studioapi.azureml.net', '4xXA7Pj5CqNRU8+FM3EaOegUxQabFwenAmwrQLZEMi7n3Xqs2lmCOgFLAfqOmURDuzUpFN12mxzvCObpdKVcEA==', trace=True)

ws.get_details()

ws.get_experiment_details('c8247daf39d94cc48d8a99d068dc8715.f-id.f73ffd5c502347058ecd398ab939280a')



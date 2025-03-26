from celery_app import celery_app
res = celery_app.AsyncResult("81bc904e-cfc2-4b2e-ad26-788e7fd43c7a")
print(res.status, res.result)


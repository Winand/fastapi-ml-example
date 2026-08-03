"Additional application metrics."
from prometheus_client import Histogram

INFERENCE_TIME = Histogram(
    "ml_inference_duration_seconds",
    "Time spent running model inference",
    labelnames=["model"],
)

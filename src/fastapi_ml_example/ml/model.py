import logging

log = logging.getLogger(__name__)


class Model:
    def __init__(self) -> None:
        log.info("New model instance")

    def predict(self, feature_a: float, feature_b: str) -> float:
        # TODO: implement prediction
        return .0


def load_model() -> Model:
    return Model()

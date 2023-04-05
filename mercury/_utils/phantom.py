from dagster import OpDefinition, get_dagster_logger, op

from mercury.base.base_op import BaseCategorizedOp
from mercury.base.config.providers import Provider


class PhantomOp(BaseCategorizedOp):
    """
    Phantom operation is not expected to be produced
    """

    def __init__(self) -> None:
        super().__init__("phantom", Provider.PHANTOM)

    def build(self) -> OpDefinition:
        @op()
        def _op():
            # Main log to fetch data from data srouce goes here
            data = ""
            get_dagster_logger().log(data)

        return _op

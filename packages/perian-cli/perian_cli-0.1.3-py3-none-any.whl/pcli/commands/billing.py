from datetime import datetime, timezone
from pcli import PerianTyper
from typing import Annotated
import typer
from pcli.api.billing import generate_bill
from decimal import Decimal

from pcli.responses import DefaultApiException, handle_exception, ExceptionLevel, BillingTimeOrderException, BothBillingTimesNeededException
from pcli.util.formatter import print_billing_information

billing_command = PerianTyper(
    no_args_is_help=True,
    rich_markup_mode="rich",
    help="Managed and interact with billing information",
)


@billing_command.command("get", help="Get billing information for a given time")
@handle_exception(DefaultApiException, exit=True, level=ExceptionLevel.ERROR)
@handle_exception(BillingTimeOrderException, exit=True, level=ExceptionLevel.WARNING)
@handle_exception(BothBillingTimesNeededException, exit=True, level=ExceptionLevel.WARNING)
def get_bill(
    start_time: Annotated[datetime, typer.Option(help="Start time for the billing information. Defaults to the beginning of the last month")] = None,
    end_time: Annotated[datetime, typer.Option(help="End time for the billing information. Defaults to the end of the last month")] = None,
):
    if start_time and not end_time:
        raise BothBillingTimesNeededException()

    # adding timezone information to the datetime objects
    if start_time:
        if start_time.tzinfo is None:
            start_time = start_time.replace(tzinfo=timezone.utc)
    if end_time:
        if end_time.tzinfo is None:
            end_time = end_time.replace(tzinfo=timezone.utc)

    billing_information = generate_bill(start_time, end_time)

    # adding perian margin to total price
    billing_information.total_price = str(Decimal(billing_information.total_price) * Decimal(billing_information.margin_multiplier))

    print_billing_information(billing_information)


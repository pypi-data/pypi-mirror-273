from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Dict, Optional, Union

from great_expectations.compatibility.typing_extensions import override
from great_expectations.core.suite_parameters import (
    SuiteParameterDict,  # noqa: TCH001
)
from great_expectations.expectations.expectation import (
    BatchExpectation,
    render_suite_parameter_string,
)
from great_expectations.render import LegacyRendererType, RenderedStringTemplateContent
from great_expectations.render.renderer.renderer import renderer
from great_expectations.render.renderer_configuration import (
    RendererConfiguration,
    RendererValueType,
)
from great_expectations.render.util import (
    handle_strict_min_max,
    substitute_none_for_missing,
)

if TYPE_CHECKING:
    from great_expectations.core import (
        ExpectationValidationResult,
    )
    from great_expectations.execution_engine import ExecutionEngine
    from great_expectations.expectations.expectation_configuration import (
        ExpectationConfiguration,
    )
    from great_expectations.render.renderer_configuration import AddParamArgs


class ExpectTableColumnCountToBeBetween(BatchExpectation):
    """Expect the number of columns to be between two values.

    expect_table_column_count_to_be_between is a \
    [Batch Expectation](https://docs.greatexpectations.io/docs/guides/expectations/creating_custom_expectations/how_to_create_custom_batch_expectations).

    BatchExpectations are one of the most common types of Expectation.
    They are evaluated for an entire Batch, and answer a semantic question about the Batch itself.

    Args:
        min_value (int or None): \
            The minimum number of columns, inclusive.
        max_value (int or None): \
            The maximum number of columns, inclusive.

    Other Parameters:
        result_format (str or None): \
            Which output mode to use: BOOLEAN_ONLY, BASIC, COMPLETE, or SUMMARY. \
            For more detail, see [result_format](https://docs.greatexpectations.io/docs/reference/expectations/result_format).
        catch_exceptions (boolean or None): \
            If True, then catch exceptions and include them as part of the result object. \
            For more detail, see [catch_exceptions](https://docs.greatexpectations.io/docs/reference/expectations/standard_arguments/#catch_exceptions).
        meta (dict or None): \
            A JSON-serializable dictionary (nesting allowed) that will be included in the output without \
            modification. For more detail, see [meta](https://docs.greatexpectations.io/docs/reference/expectations/standard_arguments/#meta).

    Returns:
        An [ExpectationSuiteValidationResult](https://docs.greatexpectations.io/docs/terms/validation_result)

        Exact fields vary depending on the values passed to result_format, catch_exceptions, and meta.

    Notes:
        * min_value and max_value are both inclusive.
        * If min_value is None, then max_value is treated as an upper bound, and the number of acceptable columns \
          has no minimum.
        * If max_value is None, then min_value is treated as a lower bound, and the number of acceptable columns \
          has no maximum.

    See Also:
        [expect_table_column_count_to_equal](https://greatexpectations.io/expectations/expect_table_column_count_to_equal)

    Supported Datasources:
        [Snowflake](https://docs.greatexpectations.io/docs/application_integration_support/)
        [PostgreSQL](https://docs.greatexpectations.io/docs/application_integration_support/)

    Data Quality Category:
        Schema

    Example Data:
                test 	test2
            0 	1.00 	2
            1 	2.30 	5
            2 	4.33 	0

    Code Examples:
        Passing Case:
            Input:
                ExpectTableColumnCountToBeBetween(
                    min_value=1
                    max_value=3
            )

            Output:
                {
                  "exception_info": {
                    "raised_exception": false,
                    "exception_traceback": null,
                    "exception_message": null
                  },
                  "result": {
                    "observed_value": 2
                  },
                  "meta": {},
                  "success": true
                }

        Failing Case:
            Input:
                ExpectTableColumnCountToBeBetween(
                    min_value=3
            )

            Output:
                {
                  "exception_info": {
                    "raised_exception": false,
                    "exception_traceback": null,
                    "exception_message": null
                  },
                  "result": {
                    "observed_value": 2
                  },
                  "meta": {},
                  "success": false
                }
    """  # noqa: E501

    min_value: Union[float, SuiteParameterDict, datetime, None]
    max_value: Union[float, SuiteParameterDict, datetime, None]

    library_metadata = {
        "maturity": "production",
        "tags": ["core expectation", "table expectation"],
        "contributors": [
            "@great_expectations",
        ],
        "requirements": [],
        "has_full_test_suite": True,
        "manually_reviewed_code": True,
    }

    metric_dependencies = ("table.column_count",)
    success_keys = (
        "min_value",
        "max_value",
    )
    args_keys = (
        "min_value",
        "max_value",
    )

    @classmethod
    @override
    def _prescriptive_template(
        cls,
        renderer_configuration: RendererConfiguration,
    ) -> RendererConfiguration:
        add_param_args: AddParamArgs = (
            ("min_value", [RendererValueType.NUMBER, RendererValueType.DATETIME]),
            ("max_value", [RendererValueType.NUMBER, RendererValueType.DATETIME]),
            ("strict_min", RendererValueType.BOOLEAN),
            ("strict_max", RendererValueType.BOOLEAN),
        )
        for name, param_type in add_param_args:
            renderer_configuration.add_param(name=name, param_type=param_type)

        params = renderer_configuration.params

        if not params.min_value and not params.max_value:
            template_str = "May have any number of columns."
        else:
            at_least_str: str = "greater than or equal to"
            if params.strict_min:
                at_least_str = cls._get_strict_min_string(
                    renderer_configuration=renderer_configuration
                )
            at_most_str: str = "less than or equal to"
            if params.strict_max:
                at_most_str = cls._get_strict_max_string(
                    renderer_configuration=renderer_configuration
                )

            if params.min_value and params.max_value:
                template_str = (
                    f"Must have {at_least_str} $min_value and {at_most_str} $max_value columns."
                )
            elif not params.min_value:
                template_str = f"Must have {at_most_str} $max_value columns."
            else:
                template_str = f"Must have {at_least_str} $min_value columns."

        renderer_configuration.template_str = template_str

        return renderer_configuration

    @classmethod
    @override
    @renderer(renderer_type=LegacyRendererType.PRESCRIPTIVE)
    @render_suite_parameter_string
    def _prescriptive_renderer(  # type: ignore[override] # TODO: Fix this type ignore
        cls,
        configuration: ExpectationConfiguration,
        result: Optional[ExpectationValidationResult] = None,
        runtime_configuration: Optional[dict] = None,
        **kwargs,
    ):
        runtime_configuration = runtime_configuration or {}
        _ = runtime_configuration.get("include_column_name") is not False
        styling = runtime_configuration.get("styling")
        params = substitute_none_for_missing(
            configuration.kwargs,
            ["min_value", "max_value", "strict_min", "strict_max"],
        )
        if params["min_value"] is None and params["max_value"] is None:
            template_str = "May have any number of columns."
        else:
            at_least_str, at_most_str = handle_strict_min_max(params)
            if params["min_value"] is not None and params["max_value"] is not None:
                template_str = (
                    f"Must have {at_least_str} $min_value and {at_most_str} $max_value columns."
                )
            elif params["min_value"] is None:
                template_str = f"Must have {at_most_str} $max_value columns."
            elif params["max_value"] is None:
                template_str = f"Must have {at_least_str} $min_value columns."

        return [
            RenderedStringTemplateContent(
                content_block_type="string_template",
                string_template={
                    "template": template_str,
                    "params": params,
                    "styling": styling,
                },
            )
        ]

    @override
    def _validate(
        self,
        metrics: Dict,
        runtime_configuration: Optional[dict] = None,
        execution_engine: Optional[ExecutionEngine] = None,
    ):
        return self._validate_metric_value_between(
            metric_name="table.column_count",
            metrics=metrics,
            runtime_configuration=runtime_configuration,
            execution_engine=execution_engine,
        )

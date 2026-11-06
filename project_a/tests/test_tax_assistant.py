from project_a.parser.tax_assistant import process_tax_query


def test_missing_residential_status():
    result = process_tax_query(
        "My salary is 12 lakh under new regime"
    )

    assert result["status"] == "needs_clarification"


def test_successful_tax_calculation():
    result = process_tax_query(
        "My salary is 12 lakh under new regime",
        is_resident=True
    )

    assert result["status"] == "success"
    assert "tax_result" in result
    assert result["tax_result"]["gross_salary"] == 1200000
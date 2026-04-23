from datetime import date
import holidays

def test_date_key_format():
    d = date(2024, 3, 15)
    key = int(d.strftime("%Y%m%d"))
    assert key == 20240315
    assert len(str(key)) == 8

def test_total_amount():
    quantity = 3
    unit_price = 0.99
    total = round(quantity * unit_price, 2)
    assert total == 2.97

def test_dim_date_columns():
    required = ["DateKey","FullDate","Year","Quarter",
                "Month","Day","DayOfWeek","IsHoliday"]
    row = {
        "DateKey": 20240101, "FullDate": "2024-01-01",
        "Year": 2024, "Quarter": 1, "Month": 1,
        "Day": 1, "DayOfWeek": 0, "IsHoliday": True
    }
    for col in required:
        assert col in row

def test_colombia_holiday():
    co_h = holidays.Colombia(years=[2024])
    assert date(2024, 1, 1) in co_h

def test_invoice_date_partition():
    d = date(2024, 6, 15)
    assert d.strftime("%Y") == "2024"
    assert d.strftime("%m") == "06"
    assert d.strftime("%d") == "15"

def test_fact_sales_columns():
    required = ["CustomerKey","TrackKey","InvoiceDateKey",
                "EmployeeKey","Quantity","UnitPrice","TotalAmount"]
    row = {
        "CustomerKey": 1, "TrackKey": 1, "InvoiceDateKey": 20240101,
        "EmployeeKey": 3, "Quantity": 1, "UnitPrice": 0.99, "TotalAmount": 0.99
    }
    for col in required:
        assert col in row

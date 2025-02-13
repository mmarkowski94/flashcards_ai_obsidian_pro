**📝 3. Pytest Fixtures**

  

**🔹 Co to jest fixture?**

• fixture to mechanizm pozwalający na **przygotowanie i czyszczenie środowiska testowego**.

• Można używać ich do **inicjalizacji obiektów**, **tworzenia bazy danych** czy **mockowania zależności**.

  

**🔹 Przykład fixture w pytest**

```python

import pytest

@pytest.fixture
def sample_data():
    return {"name": "Alice", "age": 30}

def test_user(sample_data):
    assert sample_data["name"] == "Alice"

```

**🔹 Wykonywanie kodu przed i po teście (yield)**


```python

@pytest.fixture
def setup_teardown():
    print("🔧 Setup przed testem")
    yield
    print("🗑 Cleanup po teście")

```

#fixtures #pytest #unit_tests 
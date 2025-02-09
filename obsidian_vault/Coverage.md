**📝 2. Coverage – Pokrycie Testami**

  

**🔹 Co to jest Coverage?**

• Pokazuje, **które linie kodu zostały przetestowane**, a które nie.

• Pomaga znaleźć **nieprzetestowane fragmenty** kodu.

  

**🔹 Instalacja pytest-cov**

```sh

pip install pytest-cov

```

**🔹 Sprawdzenie pokrycia kodu testami**

```sh

pytest --cov=moj_modul  # Pokrycie kodu w module
pytest --cov=.          # Pokrycie całego projektu

```

**🔹 Generowanie raportów HTML**

```sh

pytest --cov=. --cov-report=html

```


#pytest #coverage
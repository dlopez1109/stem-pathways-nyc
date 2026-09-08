"""Offline contracts for catalog caching, lazy admin work, and slow UI feedback."""

from pathlib import Path


SOURCE = (Path(__file__).resolve().parent / "app.py").read_text(encoding="utf-8")

assert "@st.cache_data(show_spinner=False)\ndef load_stem_college_catalog" in SOURCE
assert "@st.cache_data(show_spinner=False)\ndef load_local_csv_dataset" in SOURCE
assert '"data/opportunities.csv"' in SOURCE
assert '"data/careers.csv"' in SOURCE
assert "large_dataset_cache()" in SOURCE
assert 'measure_slow_action("prepare_opportunity_catalog")' in SOURCE

admin_branch = SOURCE.index('elif page == "Admin Dashboard":')
admin_metrics_call = SOURCE.index("initial_admin_data = load_admin_metrics()")
admin_auth_call = SOURCE.index("initial_auth_users, initial_auth_error")
assert admin_metrics_call > admin_branch
assert admin_auth_call > admin_branch
assert "Loading private administrator data…" in SOURCE

assert "Searching opportunities…" in SOURCE
assert "Finding your best-fit colleges…" in SOURCE
assert "if elapsed_ms >= 1000" in SOURCE
assert 'logger.info("slow_action action=%s ms=%s"' in SOURCE

print("PASS: catalogs cached, admin lazy, searches visible, slow actions measured")

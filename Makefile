.PHONY: run-eml-smoke run-eml clean-eml-artifacts

run-eml-smoke:
	python scripts/run_eml_experiment.py \
		--x-max 20000 \
		--modulus 360 \
		--log-grid-points 64 \
		--window 15 \
		--depth 3 \
		--restarts 2 \
		--steps 200 \
		--data-dir data_smoke \
		--runs-dir runs_smoke

run-eml:
	python scripts/run_eml_experiment.py \
		--x-max 1000000 \
		--modulus 360 \
		--log-grid-points 256 \
		--window 31 \
		--depth 3 \
		--restarts 10 \
		--steps 4000 \
		--data-dir data \
		--runs-dir runs

clean-eml-artifacts:
	python -c "import shutil,pathlib; [shutil.rmtree(p, ignore_errors=True) for p in ['data_smoke','runs_smoke','data','runs'] if pathlib.Path(p).exists()]; print('cleaned')"

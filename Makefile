.PHONY: all test clean

all: rfc reno

data:
	@if [ ! -d "./data" ]; then \
		echo "Creating data folder... 📊"; \
		mkdir -p ./data; \
	fi

images:
	@if [ ! -d "./images" ]; then \
		echo "Creating images folder... 📷"; \
		mkdir -p ./images; \
	fi

rfc-images:
	@if [ ! -d "./images/rfc-793" ]; then \
		echo "Creating images/rfc-793 folder... 📷"; \
		mkdir -p ./images/rfc-793; \
	fi

reno-images:
	@if [ ! -d "./images/reno" ]; then \
		echo "Creating images/reno folder... 📷"; \
		mkdir -p ./images/reno; \
	fi

ns-rfc:
	@cd network-simulator && make rfc && cd ..
	@echo "Executing program for RFC-793 ⚡"

ns-rfc-fixup:
	@cd network-simulator && make rfc-fix && cd ..
	@echo "Executing program for RFC-793 (fixed) ⚡"

rfc: data images rfc-images ns-rfc
	@python main.py --file ./data/trace_file_rfc793.res --timeout-file ./data/timeout_rfc793.res --congestion-file ./data/congestion_window_rfc793.res --node 1 --implementation rfc793 --save-folder ./images/rfc-793


rfc-fix: data images rfc-images ns-rfc-fixup
	@python main.py --file ./data/trace_file_rfc793.res --timeout-file ./data/timeout_rfc793.res --congestion-file ./data/congestion_window_rfc793.res --node 1 --implementation rfc793 --save-folder ./images/rfc-793

ns-reno:
	@cd network-simulator && make reno && cd ..
	@echo "Executing program for Reno ⚡"

ns-reno-fixup:
	@cd network-simulator && make reno-fix && cd ..
	@echo "Executing program for Reno ⚡"

reno: data images reno-images ns-reno
	@python main.py --file ./data/trace_file_reno.res --timeout-file ./data/timeout_reno.res --congestion-file ./data/congestion_window_reno.res --node 1 --implementation reno --save-folder ./images/reno

reno-fix: data images reno-images ns-reno-fixup
	@python main.py --file ./data/trace_file_reno.res --timeout-file ./data/timeout_reno.res --congestion-file ./data/congestion_window_reno.res --node 1 --implementation reno --save-folder ./images/reno

fix: rfc-fix reno-fix
	@echo "Executing fixed versions for RENO and RFC... 🛠️"

test:
 	ifeq (, $(shell which pytest))
 	$(error "No pytest in $(PATH), consider doing pip install pytest")
 	endif
	@echo "Testing...🧪"
	@pytest .


clean:
	@echo "Cleaning up... 🧹"
	@rm -rf ./data
	@rm -rf ./images
	@cd network-simulator && make clean && cd ..

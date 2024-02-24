
all: rfc reno

rfc:
	echo "Running RFC-793 simulation  1️⃣"
	ns cw1.tcl rfc false
	echo "Moving files to the data folder... 📦"
	mv congestion_window.res ../data/congestion_window_rfc793.res
	mv timeout.res ../data/timeout_rfc793.res
	mv trace_file.res ../data/trace_file_rfc793.res

rfc-fix:
	echo "Running RFC-793 simulation (fixed!) 1️⃣"
	ns cw1.tcl rfc true
	echo "Moving files to the data folder... 📦"
	mv congestion_window.res ../data/congestion_window_rfc793.res
	mv timeout.res ../data/timeout_rfc793.res
	mv trace_file.res ../data/trace_file_rfc793.res

reno:
	echo "Running Reno simulation 🦏"
	docker run --rm -v .:/home/builduser/ ghcr.io/pablito2020/ns-for-everyone:main bash -c "cd /home/builduser && ns cw1.tcl reno false 2> timeout-reno.res && chown $(id -u):$(id -g) timeout-reno.res && chmod 666 timeout-reno.res"
	echo "Moving files to the data folder... 📦"
	mv congestion_window.res ../data/congestion_window_reno.res
	mv timeout-reno.res ../data/timeout_reno.res
	mv trace_file.res ../data/trace_file_reno.res

reno-fix:
	echo "Running Reno simulation (fixed) 🦏"
	docker run --rm -v .:/home/builduser/ ghcr.io/pablito2020/ns-for-everyone:main bash -c "cd /home/builduser && ns cw1.tcl reno true 2> timeout-reno.res && chown $(id -u):$(id -g) timeout-reno.res && chmod 666 timeout-reno.res"
	echo "Moving files to the data folder... 📦"
	mv congestion_window.res ../data/congestion_window_reno.res
	mv timeout-reno.res ../data/timeout_reno.res
	mv trace_file.res ../data/trace_file_reno.res

clean:
	@echo "Cleaning up... 🧹"
	@rm -rf *.res

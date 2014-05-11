# Copy the most recent calibration plot in system
cp -r ../../out/`ls -t ../../out/ | head -n 1`/calibration evaluation/$1
cp eval-resu* evaluation/$1/
# cp -r output evaluation/$1/
cp application.conf evaluation/$1/configuration.conf
cp pick-result.eps evaluation/$1/

# # Copy the most recent calibration plot in system
# cp -r ../../out/`ls -t ../../out/ | head -n 1`/calibration evaluation/$1
# cp eval-resu* evaluation/$1/
# # cp -r output evaluation/$1/
# cp application.conf evaluation/$1/configuration.conf
# cp pick-result.eps evaluation/$1/

DATE=`ls -t ../../out/ | head -n 1`
mkdir -p experiments/${DATE}-$1
cp -r application.conf experiments/${DATE}-$1/configuration.conf
cp pick-result.eps eval-results.txt experiments/${DATE}-$1/
psql -d $DBNAME -c "select * 
from dd_inference_result_variables_mapped_weights 
order by weight desc" > experiments/${DATE}-$1/weights.txt

cp result-errred.txt experiments/${DATE}-$1/

echo "Results saved to: experiments/${DATE}-$1/"
echo "Saving calibration plots:"
cp -r ../../out/${DATE}/calibration experiments/${DATE}-$1/calibration  # comment in $1

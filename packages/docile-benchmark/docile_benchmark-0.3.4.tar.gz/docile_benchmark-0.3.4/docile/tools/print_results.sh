set -euo pipefail

PREDICTIONS_DIR=$1
group="${2:-main}"
tablefmt="${3:-csv}"
splits="${4:-test,val}"

  highlight=""
if [[ $tablefmt == "github" ]]; then
  highlight="--highlight-best-numbers"
fi

if [[ $group == "main" ]]; then
  models="roberta_base,roberta_ours,layoutlmv3_base,layoutlmv3_ours,roberta_base_detr_table,roberta_base_detr_tableLI,roberta_base_with_2d_embedding"
elif [[ $group == "synthetic" ]]; then
  models="roberta_base_with_synthetic_pretraining,roberta_ours_with_synthetic_pretraining,layoutlmv3_ours_with_synthetic_pretraining"
elif [[ $group == "all" ]]; then
  models="roberta_base,roberta_ours,layoutlmv3_base,layoutlmv3_ours,roberta_base_detr_table,roberta_base_detr_tableLI,roberta_base_with_2d_embedding,roberta_base_with_synthetic_pretraining,roberta_ours_with_synthetic_pretraining,layoutlmv3_ours_with_synthetic_pretraining"
elif [[ $group == "all-tmp" ]]; then
  models="roberta_base,roberta_ours,layoutlmv3_base,layoutlmv3_ours,roberta_base_detr_table,roberta_base_detr_tableLI,roberta_base_with_synthetic_pretraining,roberta_ours_with_synthetic_pretraining,layoutlmv3_ours_with_synthetic_pretraining"
else
  echo "unknown group of models ${models}"
  exit 1
fi


# print for github readme
# python /app/docile/tools/print_results.py \
#     --predictions-dir ${PREDICTIONS_DIR} \
#       --split "val,test" \
#         --highlight-best-numbers \
#           --models "roberta_base,roberta_ours,layoutlmv3_ours,roberta_base_with_synthetic_pretraining,roberta_ours_with_synthetic_pretraining,layoutlmv3_ours_with_synthetic_pretraining,roberta_base_detr_table,roberta_base_detr_tableLI"

# print for baselines spreadsheet
python /app/docile/tools/print_results.py \
  --predictions-dir ${PREDICTIONS_DIR} \
  --split ${splits} \
  --models ${models} \
  --tablefmt ${tablefmt} \
  $highlight

#   --models "roberta_base,roberta_ours,roberta_base_with_synthetic_pretraining,roberta_ours_with_synthetic_pretraining,layoutlmv3_base,layoutlmv3_ours,layoutlmv3_ours_with_synthetic_pretraining,roberta_base_detr_table,roberta_base_detr_tableLI" \

# task=$1
# split=$2
# if [ $# -ge 3 ]; then
#   shift ; shift
#   models=$@
# else
#   models=$(ls inference)
# fi
# 
# for subdir in ${models}; do
#   results="inference/${subdir}/${split}_results_${task}.json"
#   if [ -f $results ]; then
#     echo $subdir
#     # docile_print_evaluation_report --evaluation-result-path ${results}
#     --evaluate-x-shot-subsets "" 2> /dev/null | head -n9 | tail -n3
#     docile_print_evaluation_report --evaluation-result-path ${results} --evaluate-x-shot-subsets
#     "" --evaluate-also-text 2> /dev/null | head -n17 | tail -n11
#     echo;echo
#   fi
# done


#!/bin/sh

# unset CUDA_VISIBLE_DEVICES
# python -m paddle.distributed.launch --servers 0 --workers 0 run_syn_ant.py \
#     --pos adjective \
#     --model_type ernie \
#     --model_name_or_path ernie \
#     --max_seq_length 384 \
#     --batch_size 12 \
#     --learning_rate 3e-5 \
#     --num_train_epochs 2 \
#     --logging_steps 200 \
#     --save_steps 1000 \
#     --warmup_proportion 0.1 \
#     --weight_decay 0.01 \
#     --output_dir ./tmp/dureader-yesno/ \
#     --device gpu \
    

python run_syn_ant.py \
    --pos adjective \
    --model_type ernie \
    --model_name_or_path ernie-2.0-en \
    --max_seq_length 384 \
    --batch_size 12 \
    --learning_rate 3e-5 \
    --num_train_epochs 2 \
    --logging_steps 200 \
    --save_steps 1000 \
    --warmup_proportion 0.1 \
    --weight_decay 0.01 \
    --output_dir ./tmp/dureader-yesno/ \
    --device gpu \
    

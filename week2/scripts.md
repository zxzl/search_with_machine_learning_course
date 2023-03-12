# Level 1
```
~/fastText-0.9.2/fasttext supervised -input /workspace/datasets/fasttext/training_data.txt -output product_classifier -epoch 25 -lr 1.0 -wordNgrams 2
```

```
cat /workspace/datasets/fasttext/shuffled_labeled_products.txt |sed -e "s/\([.\!?,'/()]\)/ \1 /g" | tr "[:upper:]" "[:lower:]" | sed "s/[^[:alnum:]_]/ /g" | tr -s ' ' > /workspace/datasets/fasttext/normalized_labeled_products.txt
```

```sh
head -n 10000 /workspace/datasets/fasttext/normalized_labeled_products.txt > /workspace/datasets/fasttext/training_data.txt

tail -n 10000 /workspace/datasets/fasttext/normalized_labeled_products.txt > /workspace/datasets/fasttext/test_data.txt
```

```sh
# Extract
python week2/createContentTrainingData.py --output /workspace/datasets/fasttext/labeled_products_min500.txt. --min_products 500
# Shuffle 
shuf /workspace/datasets/fasttext/labeled_products_min500.txt --random-source=<(seq 99999) > /workspace/datasets/fasttext/min500/shuffled_labeled_products.txt
# Normalize
cat /workspace/datasets/fasttext/min500/shuffled_labeled_products.txt |sed -e "s/\([.\!?,'/()]\)/ \1 /g" | tr "[:upper:]" "[:lower:]" | sed "s/[^[:alnum:]_]/ /g" | tr -s ' ' > /workspace/datasets/fasttext/min500/normalized_labeled_products.txt
# Split
head -n 10000 /workspace/datasets/fasttext/min500/normalized_labeled_products.txt > /workspace/datasets/fasttext/min500/training_data.txt
tail -n 10000 /workspace/datasets/fasttext/min500/normalized_labeled_products.txt > /workspace/datasets/fasttext/min500/test_data.txt
# Train
~/fastText-0.9.2/fasttext supervised -input /workspace/datasets/fasttext/min500/training_data.txt -output product_classifier_min500 -epoch 25 -lr 1.0 -wordNgrams 2
# Test
~/fastText-0.9.2/fasttext test product_classifier_min500.bin /workspace/datasets/fasttext/min500/test_data.txt 
```
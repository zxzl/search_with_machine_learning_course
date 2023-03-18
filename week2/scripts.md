# Level 3
```sh
cat /workspace/datasets/fasttext/normalized_products.txt | tr " " "\n" | grep "...." | sort | uniq -c | sort -nr | head -1000 | grep -oE '[^ ]+$' > /workspace/datasets/fasttext/top_words.txt
```
```sh
python week2/appendNearestNeighbor.py \
    --input /workspace/datasets/fasttext/top_words.txt \
    --output /workspace/datasets/fasttext/synonyms.csv \
    --model /workspace/datasets/fasttext/title_model.bin \
    --threshold 0.75
```
```sh
docker cp /workspace/datasets/fasttext/synonyms.csv opensearch-node1:/usr/share/opensearch/config/synonyms.csv
./delete-indexes.sh
 ./index-data.sh -r -p /workspace/search_with_machine_learning_course/week2/conf/bbuy_products.json
```

# Level 2
```sh
# Extract
python week2/createContentTrainingData.py --output /workspace/datasets/fasttext/products.txt --label name
# Normalize
cat /workspace/datasets/fasttext/products.txt |  cut -c 10- | sed -e "s/\([.\!?,'/()]\)/ \1 /g" | tr "[:upper:]" "[:lower:]" | sed "s/[^[:alnum:]]/ /g" | tr -s ' ' > /workspace/datasets/fasttext/normalized_products.txt
# Train
~/fastText-0.9.2/fasttext skipgram -input /workspace/datasets/fasttext/normalized_products.txt -output /workspace/datasets/fasttext/title_model -minCount 100 -epoch 25 
# Explore
~/fastText-0.9.2/fasttext nn /workspace/datasets/fasttext/title_model.bin
```


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
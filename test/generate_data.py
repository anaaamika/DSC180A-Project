def create_test_data(num_tweets):
    lines = 0
    with open("data/tweets.jsonl", "r") as full_data:
        with open("test/testdata/test_tweets.jsonl", "a") as test_data:
                for line in full_data:
                    if lines < int(num_tweets):
                        test_data.write(line)
                        lines += 1
                    else:
                        break
        
   
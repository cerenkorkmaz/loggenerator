import os
import random
import datetime

class Format4j2:
    @staticmethod
    def generate4j2(num_sentences, model_instance):
        unique_id = random.randint(0, 1000)
        filename = os.path.join("logs", f"log4j2-{datetime.datetime.now().strftime('%d-%m-%Y')}-{unique_id}.log")
        with open(filename, 'w') as file:
            i = 0
            generated_sentences = set()
            date_time = datetime.datetime.now()
            date_time_str = date_time.strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]
            while i < num_sentences:
                sentence = model_instance.model.make_sentence()
                
                if sentence and sentence not in generated_sentences:
                    generated_sentences.add(sentence)
                    text = sentence[:99] # Generating a random sentence that does not exceed 100 chars
                    log = f'{date_time_str} \t {text}'
                    file.write(log)
                    i += 1
                    if i != num_sentences:
                        file.write('\n')

                random_seconds = random.randint(0, 3)
                random_microseconds = random.randint(0, 999)
                date_time += datetime.timedelta(seconds=random_seconds, microseconds=random_microseconds)
                date_time_str = date_time.strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]
            
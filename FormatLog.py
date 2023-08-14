import os
import random
import datetime

class FormatLog:
    system_names = ['System1', 'System2', 'System3', 'System4', 'System5']
    subsystem_names = ['Subsys1', 'Subsys2', 'Subsys3', 'Subsys4', 'Subsys5']
    sources = ['Source1', 'Source2', 'Source3', 'Source4', 'Source5']
    levels = ['Information', 'Warning', 'Error']
    users = ['User1', 'User2', 'User3', 'User4', 'User5', 'Aselsan Designer', 'Test', 'Aselsan Tasarimci']
    
    @staticmethod
    def generateLog(num_sentences, model_instance):
        # Open a file to write the logs to
        filename = os.path.join("logs", f"log-{datetime.datetime.now().strftime('%y%m%d%H%M')}-000.log")
        with open(filename, 'w') as file:
            # Write the header line
            header = 'Date/Time\tSystem Name\tSubsystem Name\tSource\tCode\tLevel\tUser\tText\n'
            file.write(header)
            # Generate N random logs
            i = 0
            generated_sentences = set()
            date_time = datetime.datetime.now()
            date_time_str = date_time.strftime('%d.%m.%y %H:%M:%S')
            while i < num_sentences:
                system_name = random.choice(FormatLog.system_names)
                subsystem_name = random.choice(FormatLog.subsystem_names)
                source = random.choice(FormatLog.sources)
                code = random.randint(0, 10)
                level = random.choice(FormatLog.levels)
                user = random.choice(FormatLog.users)
                sentence = model_instance.model.make_sentence()
                if sentence and sentence not in generated_sentences:
                    generated_sentences.add(sentence)
                    text = sentence[:100] # Generating a random sentence that does not exceed 100 chars
                    log = f'{date_time_str}\t{system_name}\t{subsystem_name}\t{source}\t{code}\t{level}\t{user}\t{text}'
                    file.write(log)
                    i += 1
                    if i != num_sentences:
                        file.write('\n')

                random_seconds = random.randint(0, 3)
                date_time += datetime.timedelta(seconds=random_seconds)
                date_time_str = date_time.strftime('%d.%m.%y %H:%M:%S')
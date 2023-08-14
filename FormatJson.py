import os
import random
import datetime
import json

class FormatJson:
     # List of values to use for generating random logs
    sources = ['REHIS', 'JETHA', 'FESOM', 'PODRI', 'BACOL', 'NIRLU', 'LOJEM', 'ZELGA', 'QOVIX', 'DUNIK']
    levels = ['INFO', 'WARN', 'ERROR']
    first_names = ['Aylin', 'Berk', 'Cemre', 'Deniz', 'Elif', 'Firat', 'Gul', 'Hakan', 'Irem', 'Jale']
    last_names = ['Yilmaz', 'Kaya', 'Celik', 'Ozturk', 'Demir', 'Sahin', 'Yildirim', 'Acar', 'Turan', 'Gunes']
    usernames = ['admin', 'uretici', 'tester', 'sistemci', 'muhendis', 'musteri']
    loggers = ['tr.com.aselsan.scope.common.business.logging.thread.WriteToConsoleThread',
                   'com.example.project.module.utility.logging.thread.WriteToDatabaseThread',
                   'tr.com.aselsan.scope.common.business.logging.thread.ReadFromConsoleThread',
                   'org.acme.application.service.mail.sendgrid.SendGridMailerService',
                   'com.company.project.util.logging.handler.LogFileHandler',
                   'io.github.user.project.database.repository.PostgreSQLRepository',
                   'net.example.app.module.security.authentication.JwtAuthenticationProvider']
    log_types = ['BUSINESS_LOG', 'Aselsan', 'TEST_LOG']
    services = ['GPY', 'VYX', 'KUZ', 'JAS', 'ZEN', 'FIZ', 'NOX', 'HUV', 'PYT', 'QEV', 'LOK']
    categories = ['GPY', 'TEST','ABC', 'XYZ', 'DEV', 'PROD', 'QA', 'UI', 'BACKEND', 'FRONTEND', 'MOBILE', 'DATABASE']

    @staticmethod
    def generateJson(num_sentences, model_instance):
        filename = os.path.join("logs", f"logjson-{datetime.datetime.now().strftime('%y%m%d%H%M')}-000.json")
        with open(filename, 'w') as file:

            # Generate N random logs
            i = 0
            generated_sentences = set()
            date_time = datetime.datetime.now()
            date_time_str = date_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            while i < num_sentences:
                sentence = model_instance.model.make_sentence()
                
                if sentence and sentence not in generated_sentences:
                    generated_sentences.add(sentence)
                    text = sentence[:100] # Generating a random sentence that does not exceed 100 chars
                    log = {
                    "time":date_time_str,
                    "logger":random.choice(FormatJson.loggers),
                    "level":random.choice(FormatJson.levels),
                    "thread":f'scheduling-{random.randint(1, 100)}',
                    "log.time":date_time_str,
                    "log.type":random.choice(FormatJson.log_types),
                    "user.name":random.choice(FormatJson.first_names),
                    "user.username":random.choice(FormatJson.usernames),
                    "user.surname":random.choice(FormatJson.last_names),
                    "source":random.choice(FormatJson.sources),
                    "service":random.choice(FormatJson.services),
                    "category":random.choice(FormatJson.categories),
                    "message":text
                    }
                    json.dump(log, file, separators=(",", ":"))
                    i += 1
                    if i != num_sentences:
                        file.write('\n')

                random_seconds = random.randint(0, 3)   
                random_microseconds = random.randint(0, 999)
                date_time += datetime.timedelta(seconds=random_seconds, microseconds=random_microseconds)
                date_time_str = date_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

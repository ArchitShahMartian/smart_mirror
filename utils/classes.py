import csv
import os
import logging

tmp_path = "/home/archit0994/misc/gitwork/tmp/"
log_path = "/home/archit0994/misc/gitwork/log"

# Initialize the logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(process)d - %(levelname)s - %(filename)s - %(message)s',
    handlers=[
        logging.FileHandler('{}/telegraminfo.log'.format(log_path)),
        logging.StreamHandler()
    ]
)

class TodoManager:

    filename = "todo.csv"
    ADD = "add"
    VIEW = "view"
    DELETE = "delete"
    UPDATE = "update"
    

    def __init__(self):
        self.file = "{}{}".format(tmp_path, self.filename)
        if not os.path.exists(self.file):
            with open(self.file, mode='w', newline="") as f:
                writer = csv.writer(f)
                writer.writerow(['name', 'priority', 'deadline'])
                # Replace print with logs 
                logging.info("csv file created successfully")
    
    # Should it be a classmethod or otherwise?
    def add_task(self, task=None):
        task = task.strip()
        if len(task.split(",")) == 3:
            with open(self.file, mode='a', newline="") as f:
                writer = csv.writer(f)
                writer.writerow(task.split(","))
                logging.info("task added successfully")
                return "task added successfully"
        else:
            logging.info("add format incorrect")
            return "task not added: format incorrect"

    def view_task(self):
        reply = ""
        with open(self.file, mode='r', newline="") as f:
            reader = csv.DictReader(f)
            number = 1
            for row in reader:
                reply = reply + "{0:<2} {1:<15} |{2:<8} | {3}".format(
                    number, row['name'], row['priority'], row['deadline']) + "\n"
                number +=1 
        logging.info("list sent")
        return reply

    def delete_task(self, task_number=None):
        number = task_number.strip()
        if number.isdigit():
            number = int(number)
            # Read the original CSV file and store rows in a list
            with open(self.file, mode='r', newline='') as file:
                reader = csv.reader(file)
                rows = list(reader)
            # Remove the row at the specified index 
            # (row_number - 1 to adjust for 0-indexing)
            if 1 <= number <= len(rows):
                del rows[number]
            else:
                logging.info("row does not exist in the csv")
                return False, "Row {} does not exist in the CSV file.".format(number)

            # Write the modified data back to the CSV file
            with open(self.file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
            logging.info("deletion successful")
            return True, "Row {} removed successfully.".format(number)
        else:
           logging.info("input is not an integer")
           return False, "give me a number"

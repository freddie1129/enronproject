import sys
# Add the ptdraft folder path to the sys.path list
# sys.path.append('../')

from enron.models import Question

print(Question.objects.count())
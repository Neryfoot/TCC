import re

a = ">>>12344++34456.++23))"
a
data = re.sub("[^0-9^.]", "", a)
data

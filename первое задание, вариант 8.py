import os
import numpy as np
import matplotlib.pyplot as plt
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
A = 9.66459
x_start = -10
x_end = 10
step = 0.1
if not os.path.exists('results'):
    os.makedirs('results')
x_values = np.arange(x_start, x_end + step, step)
y_values = -np.sin(x_values) * np.cos(A) * np.exp(1 - np.sqrt(x_values**2 + A**2)/np.pi)
data = Element('data')
xdata = SubElement(data, 'xdata')
ydata = SubElement(data, 'ydata')
for x, y in zip(x_values, y_values):
    x_elem = SubElement(xdata, 'x')
    x_elem.text = str(x)
    y_elem = SubElement(ydata, 'y')
    y_elem.text = str(y)
xml_str = minidom.parseString(tostring(data)).toprettyxml(indent="    ")
with open('results/function_values.xml', 'w') as f:
    f.write(xml_str)
plt.figure(figsize=(10, 6))
plt.plot(x_values, y_values, label=f'y = -sin(x)cos(A)exp(1-√(x²+A²)/π)\nA = {A}')
plt.title('График функции')
plt.xlabel('x')
plt.ylabel('y')
plt.xticks(np.arange(x_start, x_end + 1, 1))
plt.yticks(np.arange(min(y_values), max(y_values) + 0.1, 0.1))
plt.grid(True)
plt.legend()
plt.savefig('results/function_plot.png', dpi=300)
plt.show()
